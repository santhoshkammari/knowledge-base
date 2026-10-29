"""Stream a 16 kHz wav through Phonon-2 using fermion's LiveSession (pause-cut segments, <=30 s each).
Partials are off: only final segment decodes run. usage: stream_asr.py in.wav out.txt"""
import sys, time
import fermion._speech.live as live_impl
from fermion._speech import backends, fetch, live
from fermion.transcribe import _resolve

def load():
    repo, key, pin, local_dir = _resolve("phonon-2")
    d = local_dir if local_dir is not None else fetch.ensure(repo, key, pin)
    return backends.load(backends.resolve("ptt"), d, profile=key, backend=pin["backend"], quiet=True)

def main(src, dst, model=None):
    model = model or load()
    # Classroom lectures pause between sentences. Keep enough context across
    # those pauses; still force a decode at fermion's 30-second segment cap.
    live_impl.SILENCE_CLOSE_S = 1.5
    s = live.LiveSession(model)
    s._next_partial = 1 << 60                      # no partial decodes
    orig = s._reset_segment
    def reset():
        orig(); s._next_partial = 1 << 60
    s._reset_segment = reset
    s._reset_segment()
    t = time.time()
    s.on_final = lambda txt: print(f"[{time.time()-t:6.0f}s] {txt[:70]}", flush=True)
    live.run_wav(s, src, realtime=False)
    open(dst, "w").write("\n".join(s.finals) + "\n")
    print(dst, len(s.finals), "segments", round(time.time()-t), "s")

if __name__ == "__main__":
    main(*sys.argv[1:3])

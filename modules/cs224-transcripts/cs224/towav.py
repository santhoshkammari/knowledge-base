import sys,av,numpy as np,soundfile as sf
src,dst=sys.argv[1:3]
c=av.open(src); rs=av.AudioResampler(format="flt",layout="mono",rate=16000); out=[]
for f in c.decode(audio=0):
    for r in rs.resample(f): out.append(r.to_ndarray().reshape(-1))
for r in rs.resample(None): out.append(r.to_ndarray().reshape(-1))
a=np.concatenate(out); sf.write(dst,a,16000); print(dst,round(len(a)/16000),"s")

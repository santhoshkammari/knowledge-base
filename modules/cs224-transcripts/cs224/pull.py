import re,sys,time
from youtube_transcript_api import YouTubeTranscriptApi
import os,urllib.request
PL='https://www.youtube.com/playlist?list=PL2SOU6wwxB0uP4rJgf5ayhHWgw7akUWSf&hl=en'
if not os.path.exists('/tmp/pl.html'): open('/tmp/pl.html','wb').write(urllib.request.urlopen(urllib.request.Request(PL,headers={'User-Agent':'Mozilla/5.0'})).read())
h=open('/tmp/pl.html',errors='ignore').read()
# pair ids with titles in page order
items=[(i,t) for t,i in re.findall(r'"lockupMetadataViewModel":\{"title":\{"content":"([^"]*)".*?"contentId":"([A-Za-z0-9_-]{11})"',h,re.S)]
seen={};
for i,t in items: seen.setdefault(i,t)
out=sys.argv[1]; api=YouTubeTranscriptApi()
for i,t in seen.items():
    n=re.search(r'Lecture (\d+)',t); n=n.group(1) if n else i
    import os,glob
    if glob.glob(f"{out}/lecture_{int(n):02d}_*"): continue
    try:
        txt=" ".join(x['text'] for x in api.fetch(i).to_raw_data())
        open(f"{out}/lecture_{int(n):02d}_{i}.txt","w").write(txt); print("ok",n,i,len(txt))
    except Exception as e:
        print("FAIL",n,i,str(e)[:100].replace("\n"," "))
        if "blocking" in str(e): break
    time.sleep(8)

import re,subprocess,time,os
h=open('/tmp/pl.html',errors='ignore').read(); items=re.findall(r'"lockupMetadataViewModel":\{"title":\{"content":"([^"]*)".*?"contentId":"([A-Za-z0-9_-]{11})"',h,re.S)
PY='/home/ng6355/envs/py3_12_env/bin/python'
for t,i in items:
 n=int(re.search(r'Lecture (\d+)',t).group(1))
 if n<15: continue
 out=f'lecture_{n:02d}_%(id)s.%(ext)s'
 r=subprocess.run([PY,'-m','yt_dlp','--no-progress','--force-overwrites','-f','bestaudio[language^=en]','-o',out,f'https://www.youtube.com/watch?v={i}'],capture_output=True,text=True)
 if r.returncode:
  r=subprocess.run([PY,'-m','yt_dlp','--no-progress','--force-overwrites','-f','bestaudio','-o',out,f'https://www.youtube.com/watch?v={i}'],capture_output=True,text=True)
 print(('ok' if r.returncode==0 else 'FAIL'),n,r.stderr[-200:].replace('\n',' '),flush=True)
 time.sleep(5)

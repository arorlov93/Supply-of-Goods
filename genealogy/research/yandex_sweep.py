import json,re,subprocess,urllib.parse,sys,time
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
def page(text,pn=0,**kw):
    q={"text":text}; q.update({k:v for k,v in kw.items() if v}); 
    if pn: q["pageNum"]=pn
    url="https://yandex.ru/archive/search?"+urllib.parse.urlencode(q)
    out=subprocess.run(["curl","-s","--max-time","45","-A",UA,url],capture_output=True).stdout.decode("utf-8","replace")
    m=re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>',out,re.S)
    if not m: return []
    try: return json.loads(m.group(1))["props"]["pageProps"].get("items") or []
    except Exception: return []
def sweep(queries,pages=6,years=(1917,1918,1919),must=(r"Евдоки|Авдоть",r"Прокоф|Прокоп")):
    seen={}
    for q in queries:
        for pn in range(pages):
            it=page(q,pn,dateFrom="1917",dateTo="1919")
            if not it: break
            for x in it:
                sn=" ".join((x.get("snippet") or "").split())
                yr=(x.get("dateFrom") or "")[-4:]
                key=x.get("namepath") or x.get("id")
                if key in seen: continue
                try: y=int(yr)
                except: y=0
                if years and not (years[0]<=y<=years[-1]): continue
                if all(re.search(p,sn,re.I) for p in must):
                    seen[key]=(y,key,sn,q)
            time.sleep(0.2)
    return seen

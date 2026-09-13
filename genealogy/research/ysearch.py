import json,re,sys,urllib.parse,subprocess,time

UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"

def fetch(text,dateFrom=None,dateTo=None,page=0):
    q={"text":text}
    if dateFrom: q["dateFrom"]=dateFrom
    if dateTo: q["dateTo"]=dateTo
    if page: q["pageNum"]=page
    url="https://yandex.ru/archive/search?"+urllib.parse.urlencode(q)
    out=subprocess.run(["curl","-s","--max-time","45","-A",UA,url],capture_output=True).stdout.decode("utf-8","replace")
    m=re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>',out,re.S)
    if not m: return None,url,out[:200]
    return json.loads(m.group(1)),url,None

def items(js):
    pp=js.get("props",{}).get("pageProps",{}) if "props" in js else js.get("pageProps",{})
    return pp.get("items") or [], pp

def show(text,dateFrom=None,dateTo=None,limit=12,filt=None):
    js,url,err=fetch(text,dateFrom,dateTo)
    print(f"\n### «{text}» {dateFrom or ''}-{dateTo or ''}")
    if js is None: print("  ERR",err); return []
    it,pp=items(js)
    total=pp.get("total") or pp.get("itemsCount") or len(it)
    print(f"  url: {url}\n  результатов на странице: {len(it)} (total={total})")
    hits=[]
    for x in it[:limit]:
        sn=" ".join((x.get("snippet") or "").split())
        if filt and not re.search(filt,sn,re.I): continue
        print(f"  - [{x.get('dateFrom','')[-4:]}] {x.get('namepath','')} :: {sn[:230]}")
        hits.append(x)
    return hits

import os, urllib.request, urllib.parse, xml.etree.ElementTree as ET, sys
NS={'a':'http://www.w3.org/2005/Atom'}
def q(name, query, n=40):
    url=("http://export.arxiv.org/api/query?search_query="+urllib.parse.quote(query)
         +"&sortBy=submittedDate&sortOrder=descending&max_results=%d"%n)
    print("### %s\nQUERY: %s\nURL: %s"%(name,query,url), file=sys.stderr)
    raw=urllib.request.urlopen(url, timeout=60).read()
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"%s.xml"%name),"wb").write(raw)
    root=ET.fromstring(raw)
    out=[]
    for e in root.findall('a:entry',NS):
        t=e.find('a:title',NS).text.replace('\n',' ').strip()
        s=e.find('a:summary',NS).text.replace('\n',' ').strip()
        d=e.find('a:published',NS).text
        l=e.find('a:id',NS).text
        out.append((d,t,l,s))
    return out
sweep=q("sweep",'ti:"Riemann hypothesis"',40)
tgt=q("targeted",'abs:"Riemann hypothesis" AND (abs:"verified" OR abs:"verification")',40)
print("=== SWEEP (title:Riemann hypothesis, newest 40) ===")
for d,t,l,s in sweep: print("%s | %s\n    %s\n    ABS: %s\n"%(d,t,l,s[:400]))
print("=== TARGETED (abs:Riemann hypothesis AND verified/verification, newest 40) ===")
for d,t,l,s in tgt: print("%s | %s\n    %s\n    ABS: %s\n"%(d,t,l,s[:400]))

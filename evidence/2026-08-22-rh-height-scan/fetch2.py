import os, urllib.request, urllib.parse, xml.etree.ElementTree as ET, sys
NS={'a':'http://www.w3.org/2005/Atom'}
def q(name, query, n=30):
    url=("http://export.arxiv.org/api/query?search_query="+urllib.parse.quote(query)
         +"&sortBy=submittedDate&sortOrder=descending&max_results=%d"%n)
    print("### %s\nQUERY: %s"%(name,query), file=sys.stderr)
    raw=urllib.request.urlopen(url, timeout=60).read()
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"%s.xml"%name),"wb").write(raw)
    root=ET.fromstring(raw)
    nres=0
    for e in root.findall('a:entry',NS):
        nres+=1
        t=e.find('a:title',NS).text.replace('\n',' ').strip()
        s=e.find('a:summary',NS).text.replace('\n',' ').strip()
        d=e.find('a:published',NS).text
        l=e.find('a:id',NS).text
        print("%s | %s\n    %s\n    ABS: %s\n"%(d,t,l,s[:350]))
    if nres==0: print("(no results)\n")
# direct height searches
q("height13",'abs:"Riemann hypothesis" AND (abs:"10^{13}" OR abs:"10^13" OR abs:"10,000,000,000,000")',30)
q("height12",'abs:"Riemann hypothesis" AND (abs:"10^{12}" OR abs:"10^12")',30)

"""Public metadata only: discover lawful author/repository full-text locations.

No credentials, access-control workaround, author messaging or paywall bypass.
Metadata is not evidence of having read the algorithms.
"""
import json
import hashlib
import urllib.request
import urllib.parse
from scripts.classify_p5_lifts import ROOT, save


def main():
    out=ROOT/'results/p7_positive_control/literature_metadata'
    out.mkdir(exist_ok=True); records=[]
    for label,doi in [('fast_spectral','10.1016/j.laa.2025.01.010'),
                      ('pq_squared','10.1016/j.jsc.2026.102606')]:
        for provider,url in [
            ('openalex','https://api.openalex.org/works?'+urllib.parse.urlencode({'filter':'doi:'+doi,'select':'id,title,locations,open_access'})),
            ('crossref','https://api.crossref.org/works/'+urllib.parse.quote(doi,safe=''))]:
            record={'label':label,'provider':provider,'url':url,'date':'2026-10-09'}
            try:
                with urllib.request.urlopen(url,timeout=10) as response:
                    data=json.load(response); record['http_status']=response.status
                save(out/f'{label}_{provider}.json',data)
                record['status']='metadata_retrieved'
                if provider=='openalex':
                    record['locations']=[{'landing_page_url':l.get('landing_page_url'),
                       'pdf_url':l.get('pdf_url'),'is_oa':l.get('is_oa')} for r in data['results'] for l in r['locations']]
                else: record['links']=data.get('message',{}).get('link',[])
            except Exception as e:
                record.update(status='unavailable',error=str(e))
            records.append(record)
            print(json.dumps(record),flush=True)
    publisher_records=[]
    for label,pii in [('fast_spectral','S0024379525000102'),('pq_squared','S0747717126000544')]:
        for view in ('default','FULL'):
            url='https://api.elsevier.com/content/article/PII:'+pii+'?httpAccept=text/xml'
            if view=='FULL': url+='&view=FULL'
            record={'label':label,'view':view,'url':url,'date':'2026-10-09','scope':'Official Crossref-advertised publisher text-mining endpoint, unauthenticated GET; no access workaround.'}
            try:
                with urllib.request.urlopen(url,timeout=10) as response:
                    payload=response.read(5_000_000); record['http_status']=response.status
                directory=ROOT/'tmp/p7_literature'; directory.mkdir(exist_ok=True)
                path=directory/f'{label}_{view}.xml'; path.write_bytes(payload)
                record.update(status='payload_retrieved',bytes=len(payload),sha256=hashlib.sha256(payload).hexdigest(),
                              local_untracked_path=path.relative_to(ROOT).as_posix())
            except Exception as e: record.update(status='unavailable',error=str(e))
            publisher_records.append(record); print(json.dumps(record),flush=True)
    save(out/'access.json',{'records':records,'scope':'Metadata only; no full-text audit inferred.'})
    save(out/'publisher_access.json',{'records':publisher_records,'interpretation':'A success must be inspected for algorithm text; HTTP success alone is not full-text access.'})


if __name__=='__main__': main()

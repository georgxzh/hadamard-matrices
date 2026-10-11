"""Bounded unauthenticated public access probes; no author requests or bypasses."""
import hashlib
import json
import urllib.request
from pathlib import Path
from scripts.publication_gap_replication import OUT, TMP, save

def main():
    urls = [
        ('fast_publisher','https://www.sciencedirect.com/science/article/pii/S0024379525000102'),
        ('fast_pdf','https://www.sciencedirect.com/science/article/pii/S0024379525000102/pdfft?isDTMRedir=true&download=true'),
        ('pq_publisher','https://www.sciencedirect.com/science/article/pii/S0747717126000544'),
        ('pq_pdf','https://www.sciencedirect.com/science/article/pii/S0747717126000544/pdfft?isDTMRedir=true&download=true'),
        ('fast_locations','https://api.openalex.org/works/https://doi.org/10.1016/j.laa.2025.01.010'),
        ('pq_locations','https://api.openalex.org/works/https://doi.org/10.1016/j.jsc.2026.102606'),
        ('historical_journal','https://ajc.maths.uq.edu.au/pdf/23/ocr-ajc-v23-p75.pdf'),
        ('historical_author','https://documents.uow.edu.au/~jennie/WEBPDF/2001_02.pdf'),
    ]
    records=[]
    for label,url in urls:
        r={'label':label,'url':url,'date':'2026-10-10'}
        try:
            with urllib.request.urlopen(url,timeout=12) as response:
                data=response.read(5_000_001)
                assert len(data)<=5_000_000, '5 MB retrieval cap'
                r.update(http_status=response.status,bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),
                         content_type=response.headers.get('Content-Type'))
            if label.endswith('locations'):
                v=json.loads(data)
                r['locations']=[{k:l.get(k) for k in ('landing_page_url','pdf_url','is_oa')} for l in v['locations']]
                r['interpretation']='Metadata only, not algorithm text.'
            else:
                p=TMP/(label+('.pdf' if data.startswith(b'%PDF') else '.txt'))
                p.write_bytes(data)
                r['local_untracked_copy']=p.relative_to(OUT.parents[1]).as_posix()
        except Exception as e:
            r['error']=str(e)
        records.append(r)
        save(OUT/'access_probes.json',{'records':records,'authorization':'Public read-only endpoints. No contacts, credentials, paywall bypass or full-text request sent.'})
        print(label,r.get('http_status'),r.get('error'),flush=True)

if __name__=='__main__': main()

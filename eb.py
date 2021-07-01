#!/bin/env python
import requests,bs4,argparse,json
import pathlib
from svglib.svglib import svg2rlg
from reportlab.pdfgen import canvas

parser = argparse.ArgumentParser()

parser.add_argument('login')
parser.add_argument('password')
parser.add_argument('book')
args = parser.parse_args()

session = requests.Session()

BOOK = args.book

sign_in_data = '{"type":"UserCredentials","login":"'+args.login+'","password":"'+args.password+'"}'
session.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0'
session.get('https://e.lanbook.com/auth/signin?redirect=%2F')
session.headers['Referer'] = 'https://e.lanbook.com/auth/signin?redirect=%2F'
print(sign_in_data)
r = session.post("https://e.lanbook.com/api/v2/signin", data=sign_in_data)
print(r.request.headers)
r.raise_for_status()
print(r.json())
resp = session.get(f"https://e.lanbook.com/reader/book/{BOOK}/").text
soup = bs4.BeautifulSoup(resp,features='html5lib')
page_urls = [img['data-src'] for img in soup.select('#pagesContainer .page>img')]
bookdir_path = pathlib.Path(f'book{BOOK}')
bookpdf_path = pathlib.Path(f'book{BOOK}.pdf')
if not bookdir_path.exists():
    bookdir_path.mkdir()
cnvs = canvas.Canvas(str(bookpdf_path))
session.headers['Referer'] = f'https://e.lanbook.com/reader/book/{BOOK}/'

print("Downloading svg book pages")
for i,url in enumerate(page_urls):
    page_path = bookdir_path/f'page-{i:04}.svg'
    if not page_path.exists():
        print(f'Downloadading {url} \t {i+1} out of {len(page_urls)}')
        resp = session.get(url)
        resp.raise_for_status()
        svg_content = resp.text
        page_path.write_text(svg_content)
    else:
        pass
        print(f'Skipping {url} because {page_path} exists!')
print("Stitching svg files into pdf")
print("This will probably take a long time.\nThere will be error messages on the screen that IDK how to fix, so please ignore them.")
for i in range(len(page_urls)):
    page_path = bookdir_path/f'page-{i:04}.svg'
    print(f"Drawing page {page_path} \t {i+1} out of {len(page_urls)}")
    drawing = svg2rlg(page_path)
    cnvs.setPageSize([drawing.width,drawing.height])
    drawing.drawOn(cnvs,0,0)
    cnvs.showPage()
print(f'Saving pdf to {bookpdf_path}...')
cnvs.save()
    

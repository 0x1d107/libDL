#!/bin/env python
import requests,bs4,argparse,json
import base64
import pathlib
import subprocess

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
resp = r.json()
TOKEN=resp['jwt']['access_token']

resp = session.get(f"https://reader.lanbook.com/api/v2/book/{BOOK}/documentFile?base64=1&lms=&jwtToken={TOKEN}").json()['data']
bookdir_path = pathlib.Path(f'book{BOOK}')
bookpdf_path = pathlib.Path(f'book{BOOK}.pdf')
if not bookdir_path.exists():
    bookdir_path.mkdir()
#cnvs = canvas.Canvas(str(bookpdf_path))

bookpdf_path.write_bytes(base64.b64decode(resp))


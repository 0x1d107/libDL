# libDL
Tools to download books for http://e.lanbook.com and RBooks reader
## eb.py
### Installation
```
pip install -r requirements.txt
```
Preferably you should do it in a virtual environment to avoid 
conflicting depenencies.
### Usage
```
./eb.py <login> <password> <book_id> 
```
book_id is the id after `https://e.lanbook.com/book/` in the url

It starts downloading svg files and then combines them into a pdf document.
## fuckRBooks.js
### Installation
Create a bookmark in your web browser with
```
javascript:(function()%7Bdocument.getElementById('rBooks').contentWindow.PDFViewerApplication.findController._pdfDocument.mAllowPrint%20%3D%20true%3B%0Adocument.getElementById('rBooks').contentDocument.getElementById('print').click()%3B%7D)()%3B
```
in the 'URL' field.
### Usage
Open the web page with the RBooks reader. Click on the bookmark.
The 'print' dialog will pop up. Use it to print to PDF or on a real paper.

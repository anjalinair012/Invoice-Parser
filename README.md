
Included:
Sample invoices (invoice\{month_name}\)
InvoiceParser.py
Output excel (payments.xlsx) 

Python Version 3.7.6
OS: Windows

To install Invoice Parser:
run install.cmd 
install tesseract from "https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w32-setup-v5.0.0-alpha.20200328.exe" and add the location for "Tesseract-OCR" folder to you System PATH variable
packages "poppler" and "tesseract" must be added to your system Path variable. 
	"poppler" is at "C:\Program Files\poppler-0.68.0_x86\poppler-0.68.0\bin" 
	Please check your "tesseract" location as this was installed manually. It would usually be "C:\Program Files (x86)\Tesseract-OCR".

To run the parser:
Double click run.cmd

Adding new Invoices:
The new invoices may be added to the "invoices" folder
Once the user runs "run.cmd", they are prompted to enter the invoice or the folder path. Assuming the below structure for "invoices" folder, the user has two options of input

invoices
	->July
		->1.pdf
		->2.pdf

If the user wishes to parse only "1.pdf", input- invoices\July\1.pdf
If the user wishes to parse all invoices in "July" folder, input - invoices\July


Adding templates for new invoice:
Add a yml file containing regex for fields to be extracted under "$HOME\env2\Lib\site-packages\invoice2data\extract\templates\max"



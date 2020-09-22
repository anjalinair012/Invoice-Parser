import invoice2data
import pdfkit
import os
import sys
import csv
from win32com import client
import win32api
import pathlib
from httplib2 import Http
from datetime import datetime
import openpyxl

def get_filenames(path):
	filenames=list()
	with os.scandir(path) as entries:
		for entry in entries:
			name=path+"\\"+entry.name
			filenames.append(name)
	return filenames

def convert_to_pdf(filename):
	print(filename)
	if filename.casefold().endswith('.xlsx'):
		new_file=from_excel(filename)
	elif filename.casefold().endswith('.html'):
		new_file=from_html(filename)
	elif filename.casefold().endswith('.pdf'):
		new_file=filename
	else:
		print("file type not handled")
		return 0
	return extract_invoice(new_file)

def from_html(filename):
	filename_split=os.path.splitext(filename)[0]
	pdf_file=filename_split+"_temp.pdf"
	config=pdfkit.configuration(wkhtmltopdf='env\\Lib\\site-packages\\wkhtmltopdf\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
	pdfkit.from_file(filename,pdf_file,configuration=config)
	return pdf_file

def from_excel(filename):
	filename=str(pathlib.Path.cwd() / filename)
	pdf_file=os.path.splitext(filename)[0]+"_temp.pdf"
	excel=client.DispatchEx("Excel.Application")
	excel.Visible=0
	wb=excel.Workbooks.Open(filename)
	ws=wb.Worksheets[0]
	wb.SaveAs(pdf_file,FileFormat=57)
	wb.Close()
	excel.Quit()
	return pdf_file

def extract_invoice(filename):
	template=invoice2data.extract.loader.read_templates("env\\Lib\\site-packages\\invoice2data\\extract\\templates\\max\\")
	result = invoice2data.extract_data(filename,template)
	if result:
		return to_list(result)
	else:
		exit()

def to_list(result):
	result_format=list()
	values=['invoice_number','date','price','gst','amount','issuer','nature','category']

	for value in values:
		if value not in result.keys():
			result[value]=0
	#add cgst and sgst to gst
	if 'cgst' in result.keys() and 'sgst' in result.keys():
		result['gst']=float(result.get('cgst').replace(',',''))+float(result.get('sgst').replace(',',''))
		del result['cgst']
		del result['sgst']
	if result['amount']==0:
		result['amount']= float(result.get('gst').replace(',',''))+float(result.get('price').replace(',',''))

	#set TDS and payment fields
	TDS=0
	result['price']=result['price'].replace(',','')
	if result['category']:
		if result['category']=='94I':
			TDS=float(result['price'])*0.075
		elif result['category']=='94J':
			TDS=float(result['price'])*0.075
		elif result['category']=='94C':
			TDS=float(result['price'])*0.075	
	else:
		TDS=0
	payment=float(result['amount'])-TDS
	result_format=[result['date'].strftime('%d-%m-%Y'),result['date'].strftime("%B"),result['date'].year,result['issuer'],result['nature'],result['invoice_number'],result['price'],result['gst'],result['amount'],TDS,result['category'],payment]
	return result_format

def send_to_excel(result_final):
	workbook = openpyxl.load_workbook('Payments.xlsx')    #workbook is added in quotes
	worksheet = workbook['20-21']   # worksheet name is added in quotes
	for result in result_final:
		worksheet.append(result)
	workbook.save('Payments.xlsx')

def main():
	print("Please enter the path for your invoice or the folder containing your invoice.")
	path=str(input())
	filenames=list()
	if os.path.isdir(path):
		filenames=get_filenames(path)
	elif os.path.isfile(path):
		filenames=[path]
	else:
		print("Incorrect filename entered.")
	result_final=list()
	for filename in filenames:
		result=convert_to_pdf(filename)
		if result==0:
			print("an error occured with this file format")
			continue
		result_final.append(result)
		print("===========================Invoice"+filename+"parsed=================================")
	send_to_excel(result_final)
	print("=================Completed=====================")	

if __name__=="__main__":
	main()


#!/usr/bin/env python 
# -*- coding: utf-8 -*-
from pdf2image import convert_from_path
import sys
import os
from PIL import Image
import pytesseract
from pytesseract import Output
import cv2

def to_text(path):

	PDF_file=path
	pages=convert_from_path(PDF_file,500)

	page_counter=1
	for page in pages:
		filename="page_"+str(page_counter)+".jpg"
		page.save(filename,"JPEG")
		page_counter+=1

	extract_text=""
	for i in range(1, page_counter): 
		print(i)
		filename = "page_"+str(i)+".jpg"
		img = cv2.imread(filename)
		custom_config = r'--oem 3 --psm 6'
		text=pytesseract.image_to_string(img, config=custom_config)
		os.remove(filename)
		extract_text=extract_text+text
	return extract_text

if __name__=='__main__':
    to_text(sys.argv[1])
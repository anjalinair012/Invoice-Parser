pip install virtualenv
python -m venv env
call env\Scripts\activate.bat
pip install -r requirements.txt
move /y installations\poppler-0.68.0_x86 "C:\Program Files\"
move /y installations\wkhtmltopdf "env\Lib\site-packages\wkhtmltopdf"
move /y installations\max "env\Lib\site-packages\invoice2data\extract\templates\"
move /y main.py "env\Lib\site-packages\invoice2data\"
move /y invoice_template.py "env\Lib\site-packages\invoice2data\extract\"
move pdfocr.py env\Lib\site-packages\invoice2data\input\



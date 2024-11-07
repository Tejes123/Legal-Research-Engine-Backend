# from unstructured.partition.pdf import partition_pdf
# from unstructured.documents.elements import Table, PageNumber

import os
import pymupdf

PDF_FILES_DIR = r"C:\Tejeswar\Smart India\Litigate Smart\backend\data"
PDF_EXTRACTION_DIR = r"extractedPDFContent"

if not os.path.exists(PDF_EXTRACTION_DIR):
    os.makedirs(PDF_EXTRACTION_DIR)

PDF_files = os.listdir(PDF_FILES_DIR)

def extractPDF(pdf_path):
    try:
        doc = pymupdf.open(pdf_path)
        pdf_text = ''
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text = page.get_text()
            pdf_text = pdf_text + text
        return pdf_text
    except:
        print("Cannot process the file ",pdf_path )
    return ''

for file_path in PDF_files:
    absolutePath = os.path.join(PDF_FILES_DIR, file_path )
    pdfContent = extractPDF(absolutePath)
    with open(os.path.join(PDF_EXTRACTION_DIR,  os.path.splitext(os.path.basename(file_path))[0] + '.txt'), 'w') as file:
        file.write(pdfContent)
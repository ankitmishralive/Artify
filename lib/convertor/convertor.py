# import pythoncom
from pdf2docx import Converter
import os
import shutil
from docx2pdf import convert
from pdf2image import convert_from_path
from PIL import Image
# import patoolib
import fitz  
from zipfile import ZipFile 
from pypdf import PdfWriter



def convert_pdf_to_docx(pdf_path, docx_path):
    print("entering in functi.............")
    cv = Converter(pdf_path)
    cv.convert(docx_path, start=0, end=None)
    print("Converted.....")
    cv.close()
    docx_name = f"output.docx" 
    shutil.move(docx_path, os.path.join(os.path.dirname(docx_path), docx_name))



def convert_docx_to_pdf(docx_path,pdf_path):
    print("Doc Path here : ----------",docx_path)
    print("PDF path here : ---------------",pdf_path)
    # convert(docx_path,pdf_path,pythoncom.CoInitialize())
    convert(docx_path,pdf_path)


def convert_img_to_pdf(img_path,pdf_path,name):

    image_1 = Image.open(img_path)
    im_1 = image_1.convert('RGB')
    im_1.save(pdf_path)
    pdf_name=f"{name}.pdf"
    shutil.move(pdf_path, os.path.join(os.path.dirname(pdf_path), pdf_name))

def convert_jpg_to_png(img_path,drop_path,name):
     img = Image.open(img_path)
     img_ext = f"{name}.png"
     img.save(os.path.join(drop_path, img_ext))
     
def convert_png_to_jpg(img_path,drop_path,name):
     img = Image.open(img_path)
     img_ext = f"{name}.jpg"
     img.save(os.path.join(drop_path, img_ext))

     

def convert_pdf_to_img(pdf_path,drop_location):
    file_path = pdf_path
    doc = fitz.open(file_path)  

    with ZipFile(drop_location+'Artify.zip', 'w') as zip_object:  # yeah line brbr hai 

        for i, page in enumerate(doc):
            pix = page.get_pixmap() 
            pix.save(f"pdftoimage_{i}.png")

            zip_object.write(f"pdftoimage_{i}.png")


    

def merge_pdf(fileloc,drop_location,i):
        merger = PdfWriter()
        print("value of i ::: " ,i)

        for pdf in i:
              merger.append(fileloc+pdf)
        merger.write(f"{drop_location}/merged-pdf.pdf")
        merger.close()

    
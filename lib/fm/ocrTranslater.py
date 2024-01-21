
from PyPDF2 import PdfReader
from deep_translator import GoogleTranslator
import docx
from docx2pdf import convert
import pythoncom
from gtts import gTTS

import os 
# pdf_file = "Ankit Mishra.pdf"

# Read PDF

import fitz 




def convert_pdf_to_img(pdf_path,):
    file_path = pdf_path
    doc = fitz.open(file_path)  

    # with ZipFile(drop_location+'Artify.zip', 'w') as zip_object:  # yeah line brbr hai 

    for i, page in enumerate(doc):
            pix = page.get_pixmap() 
            pix.save(f"static/Translater/pdftoimage_{i}.png")
     

import easyocr

def image_to_text(image_path,ocrlanguage):
    reader = easyocr.Reader(ocrlanguage)
    result = reader.readtext(image_path)
    # Extract and concatenate the recognized text
    text = ' '.join([item[1] for item in result])
    return text


def pdf_toaudio(pdf,language,name,extension):
    # The text that you want to convert to audio
    # reader = PdfReader(pdf)
    textargs = []
    print("-----Extension",extension)

    if ".pdf" in extension:
        reader = PdfReader(pdf)
        print("Reader---:",reader)
        for page in reader.pages:
            text = page.extract_text()
            print("try Block---text :",text)
            if text:
                textargs.append(text)
        print("text args here : ",textargs)

        
        if len(textargs)==0:
            
            print("----------if --------block here --------------")
            img= convert_pdf_to_img(pdf)
            ocrlanguage =['en','hi','mr']
            content=[file for file in os.listdir("static/Translater/") if file.endswith(".png")]
            print(content)
            for img in content:
                    txt=image_to_text(img,ocrlanguage)
                    print(txt)
                    textargs.append(txt)
                    print(textargs)

    elif extension == ".png" or ".jpg" or ".jpeg":
        #  return f"uploaded file is {extension}"
            # img= convert_pdf_to_img(pdf)
            img = pdf
            ocrlanguage =['en','hi','mr']
            # content=[file for file in os.listdir("static/Translater/") if file.endswith(".png")]
            # print(content)
            # for img in content:
            txt=image_to_text(img,ocrlanguage)
            print(txt)
            textargs.append(txt)
            print(textargs)
   
    
    stringargs = ""

    for text in textargs:
         stringargs  += text   

    Translated_text = GoogleTranslator(source='auto', target=language).translate(stringargs) 
# Language in which you want to conver
    
    myobj = gTTS(text=Translated_text, lang=language, slow=False)
    myobj.save(f"static/Translater/{name}.mp3")





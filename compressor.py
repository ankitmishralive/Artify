

from PIL import Image
from pypdf import PdfReader, PdfWriter


def compresion(old_pic, new_pic, mywidth):
        try:
            img = Image.open(old_pic)

            wpercent = (mywidth/float(img.size[0]))
            hsize = int((float(img.size[1])*float(wpercent)))
            img = img.resize((mywidth,hsize), Image.LANCZOS)
            location = f"static/compressedArea/{new_pic}"
            img.save(location)
        
        except Exception as e:
            print("Error !",e)


def pdf_Compressor(pdf_name,compression_level,compress_img):
    reader = PdfReader(pdf_name)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    for page in writer.pages:
        # ⚠️ This has to be done on the writer, not the reader!
        page.compress_content_streams(level=compression_level)  # This is CPU intensive!
    location = f"static/compressedArea/{compress_img}"
    with open(location, "wb") as f:
        writer.write(f)





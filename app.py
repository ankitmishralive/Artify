from flask import Flask, redirect,render_template,request,flash,request,jsonify, url_for
from werkzeug.utils import secure_filename
import os
from lib.chatVisualizer.chatAnalyzer import Analyze_Chat, user_Selection
from lib.convertor.convertor import convert_pdf_to_docx,convert_docx_to_pdf,convert_img_to_pdf,convert_pdf_to_img,merge_pdf,convert_jpg_to_png,convert_png_to_jpg
from lib.compressor.compressor import compresion,pdf_Compressor
from lib.fm.ocrTranslater import pdf_toaudio
from lib.resumeAnalyzer.ResumeAnalyzer import Analyzer
from lib.image_Enhancer.processor import ProcessImage
from PIL import Image
import cv2

from lib.bot.bot import chatbot
# Grammer Correction 
from pyaspeller import YandexSpeller

from flask_cors import CORS





UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'webp', 'jpeg', 'gif','pdf','docx','zip','txt'}

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
RESUME_UPLOAD_FOLDER = 'static/analyzeArea/'

app.config['RESUME_UPLOAD_FOLDER'] = RESUME_UPLOAD_FOLDER
CHAT_UPLOAD_FOLDER = 'static/chatVisualizer/'

app.config['CHAT_UPLOAD_FOLDER'] = CHAT_UPLOAD_FOLDER
app.secret_key = "yo"



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def home():
    return render_template("index.html")
    
@app.route("/old-home")
def oldhome():
    return render_template("indexSide.html")

@app.route("/zone")
def zone():
    return render_template("zone.html")

@app.route("/compressor")
def compressor():
    return render_template("compressor.html")

@app.route("/features")
def features():
    return render_template("features.html")


@app.route("/convertor")
def convertor():
    return render_template("convertor.html")

@app.route("/listen")
def listen():
    return render_template("ocr.html")

@app.route("/ai-resume-analyzer")
def ResumeAnalyzer():
    return render_template("AI_ResumeAnalyzer.html")


@app.route("/ai-chat-visualizer")
def ChatVisualizer():
    return render_template("ChatVisualizer.html")





@app.route("/pdftodoc",methods=['GET','POST'])
def pdftodoc():
        if request.method == "POST":
        # operations = request.form.get("operations")

            if 'file' not in request.files:
                flash('No file part')
                return "Error!"

            file = request.files['file']
            # multipleFiles =  request.files.getlist("file")
            if file.filename == '':
                flash('No selected file')
                return "No selected file"
            
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    
                
                og_pdffile = f"static/uploads/{filename}"
                                            
                drop_location = f"static/conversionArea/output.docx"
                heading_text = "Convert Your PDF's to DOC's"
                info_text = "upload your .pdf file & transform it in .docx"
                
                try:
                    print("in try")
                    convert_pdf_to_docx(og_pdffile,drop_location)
                    flash(f"Your PDF has been converted to DOC and is available for <a href='{drop_location}' target='_blank' >download</a>")
                    return render_template("/manipulativeOps/pdfTools.html", compressed_file=drop_location,heading=heading_text,info=info_text)
                except:
                    print("in except")
                    flash(f"You are uploading doc file & telling me to convert PDF in to Doc ")
                    return render_template("/manipulativeOps/pdfTools.html")
                
       # return render_template("/manipulativeOps/pdfTools.html")
                
        heading_text = "Convert Your PDF's to DOC's"
        info_text = "upload your .pdf file & transform it in .docx"
    

        return render_template("/manipulativeOps/pdfTools.html" ,heading=heading_text,info=info_text)



@app.route("/doctopdf",methods=['GET','POST'])
def docToPDF():

    if request.method == "POST":
        # operations = request.form.get("operations")

            if 'file' not in request.files:
                flash('No file part')
                return "Error!"

            file = request.files['file']
            # multipleFiles =  request.files.getlist("file")
            if file.filename == '':
                flash('No selected file')
                return "No selected file"
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                name = os.path.splitext(filename)[0].lower()
                og_pdffile = f"static/uploads/{filename}"
                heading_text = "Convert Your DOC to PDF's"
                info_text = "upload your .docx file & transform it in .pdf"
                                            
                try:
                            
                    drop_location = f"static/conversionArea/{name}.pdf"
                    location = "static/conversionArea/"
                    convert_docx_to_pdf(og_pdffile,location)
                    # flash(f"Your DOC has been converted to PDF and is available for <a href='{drop_location}' target='_blank' >download</a>")
                    return render_template("/manipulativeOps/pdfTools.html", compressed_file=drop_location,heading=heading_text,info=info_text)
                except:
                    flash(f"You are uploading PDF file & telling me to convert Doc in to PDF ")
                    return render_template("/manipulativeOps/pdfTools.html")
    
    # return render_template("/manipulativeOps/pdfTools.html")
    heading_text = "Convert Your DOC to PDF's"
    info_text = "upload your .docx file & transform it in .pdf"
            
    return render_template("/manipulativeOps/pdfTools.html" ,heading=heading_text,info=info_text)




@app.route("/pdftoimg",methods=['GET','POST'])
def pdfToImg():

    if request.method == "POST":
        # operations = request.form.get("operations")

            if 'file' not in request.files:
                flash('No file part')
                return "Error!"

            file = request.files['file']
            # multipleFiles =  request.files.getlist("file")
            if file.filename == '':
                flash('No selected file')
                return "No selected file"
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                og_pdffile = f"static/uploads/{filename}"
                heading_text = "Convert PDF to Images"
                info_text = "upload your .pdf file & get .zip file full of images"
                                            
                try:
                    location = f"static/conversionArea/"
                    convert_pdf_to_img(og_pdffile,location)
                    drop_location = f"static/conversionArea/Artify.zip"
                    flash(f"Your DOC has been converted to PDF and is available for <a href='{drop_location}' target='_blank' >download</a>")
                    return render_template("/manipulativeOps/pdfTools.html", compressed_file=drop_location,heading=heading_text,info=info_text)

                except:
                    flash(f"You are perform inappropriate Action, Try Again")
                    return render_template("/manipulativeOps/pdfTools.html")  

    
    # return render_template("/manipulativeOps/pdfTools.html")
    heading_text = "Convert PDF to Images"
    info_text = "upload your .pdf file & get .zip file full of images"
    return render_template("/manipulativeOps/pdfTools.html" ,heading=heading_text,info=info_text)

# name = os.path.splitext(filename)[0].lower()




@app.route("/imgtopdf",methods=['GET','POST'])
def imgtoPDF():

    if request.method == "POST":
        # operations = request.form.get("operations")

            if 'file' not in request.files:
                flash('No file part')
                return "Error!"

            file = request.files['file']
            # multipleFiles =  request.files.getlist("file")
            if file.filename == '':
                flash('No selected file')
                return "No selected file"
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                name = os.path.splitext(filename)[0].lower()

                og_pdffile = f"static/uploads/{filename}"
                heading_text = "Convert Your Images to PDF's"
                info_text = "upload your image file & transform it in .pdf"
                                                  
                try: 
                    drop_location = f"static/conversionArea/{name}.pdf"
                    convert_img_to_pdf(og_pdffile,drop_location,name)
                    flash(f"Your Image File has been converted to PDF and is available for <a href='{drop_location}' target='_blank' >download</a>")
                    return render_template("/manipulativeOps/pdfTools.html", compressed_file=drop_location,heading=heading_text,info=info_text)  
                except:
                    flash(f"You are asking for inappropriate Action",heading=heading_text,info=info_text)
                    return render_template("/manipulativeOps/pdfTools.html",heading=heading_text,info=info_text) 


    
    # return render_template("/manipulativeOps/pdfTools.html",heading=heading_text,info=info_text)
    heading_text = "Convert Your Images to PDF's"
    info_text = "upload your image file & transform it in .pdf"
    return render_template("/manipulativeOps/pdfTools.html" ,heading=heading_text,info=info_text)




#  ------------------------------
@app.route("/pngtojpg",methods=["GET","POST"])
def pngtojpg():
    if request.method == "POST":
    # operations = request.form.get("operations")

        if 'file' not in request.files:
            flash('No file part')
            return "Error!"

        file = request.files['file']
        # multipleFiles =  request.files.getlist("file")
        if file.filename == '':
            flash('No selected file')
            return "No selected file"
        
        if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                og_file = f"static/uploads/{filename}"
                                            
                drop_location = f"static/conversionArea/output.docx"
                name = os.path.splitext(filename)[0].lower()


                try:
                    dropout_location = f"static/conversionArea/"
                    convert_png_to_jpg(og_file,dropout_location,name)
                    drop_location = f"static/conversionArea/{name}.jpg"
                    flash(f"Your Image File has been converted to JPG Format and is available for <a href='{drop_location}' target='_blank' >download</a>")
                    return render_template("/manipulativeOps/pdfTools.html",heading="PNG to JPG Transformation",info="Seamless Conversion: Empowering Your Images with PNG to JPG Transformation" ,compressed_file=drop_location) 
                except:
                    flash(f"you are asking for inapppropriate Action Error in converting to JPG")
                    return render_template("/manipulativeOps/pdfTools.html",heading="PNG to JPG Transformation",info="Seamless Conversion: Empowering Your Images with PNG to JPG Transformation")
                       
        
    
    return render_template("/manipulativeOps/pdfTools.html",heading="PNG to JPG Transformation",info="Seamless Conversion: Empowering Your Images with PNG to JPG Transformation")


@app.route("/jpgtopng",methods=["GET","POST"])
def jpgtopng():
        if request.method == "POST":
    # operations = request.form.get("operations")

            if 'file' not in request.files:
                flash('No file part')
                return "Error!"

            file = request.files['file']
            # multipleFiles =  request.files.getlist("file")
            if file.filename == '':
                flash('No selected file')
                return "No selected file"
            
            if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    og_file = f"static/uploads/{filename}"
                                                
                    drop_location = f"static/conversionArea/output.docx"
                    name = os.path.splitext(filename)[0].lower()


        
            try:
                dropout_location = f"static/conversionArea/"
                convert_jpg_to_png(og_file,dropout_location,name)
                drop_location = f"static/conversionArea/{name}.png"
                flash(f"Your Image File has been converted to PNG Format and is available for <a href='{drop_location}' target='_blank' >download</a>")
                return render_template("/manipulativeOps/pdfTools.html",heading="JPG to PNG Transformation",info="Transforming Moments: JPG to PNG, Where Clarity Meets Precision!", compressed_file=drop_location) 
                # cv2.imwrite(f"static/conversionArea/{name}.png",og_file)
            except:
                flash(f"you are asking for inappropriate Action Error Here..")
                return render_template("/manipulativeOps/pdfTools.html",heading="JPG to PNG Transformation",info="Transforming Moments: JPG to PNG, Where Clarity Meets Precision!")
        
        return render_template("/manipulativeOps/pdfTools.html",heading="JPG to PNG Transformation",info="Transforming Moments: JPG to PNG, Where Clarity Meets Precision!")


@app.route("/mergepdf",methods=["GET","POST"])
def merge():
     if request.method == "POST":
        operations = request.form.get("operations")

        if 'file' not in request.files:
            flash('No file part')
            return "Error!"

        file = request.files['file']
        multipleFiles =  request.files.getlist("file")
        if file.filename == '':
            flash('No selected file')
            return "No selected file"
         
        if len(multipleFiles) >= 2:
                  i=1
                  mf = []       
                  for file in multipleFiles:                      
                       file.save(os.path.join(app.config['UPLOAD_FOLDER'],str(i)+'.pdf'))
                       mf.append(str(i)+'.pdf')
                       i=i+1
                #   print(mf)
                  
                  
                  try:
                        og_pdffile = f"static/uploads/"
                        location = f"static/conversionArea/"
                        merge_pdf(og_pdffile,location,mf)
                        drop_location = f"static/conversionArea/merged-pdf.pdf"
                        flash(f"Your PDF has been Merged and is available for <a href='{drop_location}' target='_blank' >download</a>")
                        return render_template("/manipulativeOps/pdfTools.html",heading="Merge PDFs" ,info="Harmony in Documents: Merge PDFs for a Unified and Organized Experience!" ,compressed_file=drop_location) 
                  except:
                        flash(f"You are uploading doc file & telling me to convert PDF in to Doc ")
                        return render_template("/manipulativeOps/pdfTools.html",heading="Merge PDFs" ,info="Harmony in Documents: Merge PDFs for a Unified and Organized Experience!" ) 
     return render_template("/manipulativeOps/pdfTools.html",heading="Merge PDFs" ,info="Harmony in Documents: Merge PDFs for a Unified and Organized Experience!" )

                
     




@app.route("/ask", methods=['POST'])
def ask():

    message = str(request.form['messageText'])
    print("Received Message :",message)
    # Handle the grammar correction
    speller = YandexSpeller()
    corrected_text = speller.spelled(message)

    print(corrected_text)
    
    print(f"User Input: {message}")
    print(f"Corrected Text: {corrected_text}")

    bot_response = chatbot(corrected_text) 
    print(f"Bot Response: {bot_response}")
    # print(bot_response)
    return jsonify({'status':'OK','answer':bot_response})



@app.route("/translate",methods=['GET','POST'])
def translate():
       if request.method == "POST":
        operations = request.form.get("operations")
      

        if 'file' not in request.files:
            flash('No file part')
            return "Error!"

        file = request.files['file']
     
        if file.filename == '':
            flash('No selected file')
            return "No selected file"
   
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        
            extension = os.path.splitext(filename)[1].lower()
            # print("Extension-------------------------------------",extension)
            name = os.path.splitext(filename)[0].lower()
                # pdf=PdfFileReader(filename)
            og_pdffile = f"static/uploads/{filename}"
            drop_location = f"static/Translater/{name}.mp3"
        
            # language = ""
            match operations:
                    case "english":
                        language = "en"
                        # Pdf_Translator(og_pdffile,language)
                        pdf_toaudio(og_pdffile,language,name,extension)

                        flash(f"Your File has been compressed and is available for download")
                        return render_template("ocr.html", compressed_file=drop_location)
                      
                    case "hindi":
                        language = "hi"
                        pdf_toaudio(og_pdffile,language,name,extension)
                        flash(f"Your File has been Translated and is available for download")
                        return render_template("ocr.html", compressed_file=drop_location)
                    case "gujrati":
                        language = "gu"
                        pdf_toaudio(og_pdffile,language,name,extension)
                        flash(f"Your File has been Translated and is available for download")
                        return render_template("ocr.html", compressed_file=drop_location)
                    case "marathi":
                        language = "mr"
                        pdf_toaudio(og_pdffile,language,name,extension)
                        flash(f"Your File has been Translated and is available for download")
                        return render_template("ocr.html", compressed_file=drop_location)
                    case "punjabi":
                        language = 'pa'
                        pdf_toaudio(og_pdffile,language,name,extension)
                        flash(f"Your File has been Translated and is available for download")
                        return render_template("ocr.html", compressed_file=drop_location)
                    case "malayalam":
                        language = 'ml'
                        pdf_toaudio(og_pdffile,language,name,extension)
                        flash(f"Your File has been Translated and is available for download")
                        return render_template("ocr.html", compressed_file=drop_location)
                
                    case "traditionalchinese":
                        language = 'zh-TW'
                        pdf_toaudio(og_pdffile,language,name,extension)
                        flash(f"Your File has been Translated and is available for download")
                        return render_template("ocr.html", compressed_file=drop_location)
                
                    case "simplifiedchinese":
                        language = 'zh-CN'
                        pdf_toaudio(og_pdffile,language,name,extension)
                        flash(f"Your File has been Translated and is available for download")
                        return render_template("ocr.html", compressed_file=drop_location)
                
                    case "french":
                        language = 'fr'
                        pdf_toaudio(og_pdffile,language,name,extension)
                        flash(f"Your File has been Translated and is available for download")
                        return render_template("ocr.html", compressed_file=drop_location)
        

                    case "german":
                        language = 'de'
                        pdf_toaudio(og_pdffile,language,name,extension)
                        flash(f"Your File has been Translated and is available for download")
                        return render_template("ocr.html", compressed_file=drop_location)
                    case "greek":
                                language = 'el'
                                pdf_toaudio(og_pdffile,language,name,extension)
                                flash(f"Your File has been compressed and is available for download")
                                return render_template("ocr.html", compressed_file=drop_location)
                
                    case "hungarian":
                                language = 'hu'
                                pdf_toaudio(og_pdffile,language,name,extension)
                                flash(f"Your File has been Translated and is available for download")
                                return render_template("ocr.html", compressed_file=drop_location)
   
                    case "italian":
                                language = 'it'
                                pdf_toaudio(og_pdffile,language,name,extension)
                                flash(f"Your File has been Translated and is available for download")
                                return render_template("ocr.html", compressed_file=drop_location)
                 
                    case "japanese":
                                language = 'ja'
                                pdf_toaudio(og_pdffile,language,name,extension)
                                flash(f"Your File has been Translated and is available for download")
                                return render_template("ocr.html", compressed_file=drop_location)
                    case "korean":
                                language = 'ko'
                                pdf_toaudio(og_pdffile,language,name,extension)
                                flash(f"Your File has been Translated and is available for download")
                                return render_template("ocr.html", compressed_file=drop_location)
                    case "burmese":
                                language = 'my'
                                pdf_toaudio(og_pdffile,language,name,extension)
                                flash(f"Your File has been Translated and is available for download")
                                return render_template("ocr.html", compressed_file=drop_location)
                    case "nepali":
                                language = 'ne'
                                pdf_toaudio(og_pdffile,language,name,extension)
                                flash(f"Your File has been Translated and is available for download")
                                return render_template("ocr.html", compressed_file=drop_location)
                 
                    case "russian":
                                language = 'ru'
                                pdf_toaudio(og_pdffile,language,name,extension)
                                flash(f"Your File has been Translated and is available for download")
                                return render_template("ocr.html", compressed_file=drop_location)
                
                    case "veryhigh":
                        compresion_level = 9

 
                    # drop_location = f"static/compressedArea/{filename}"
            # Pdf_Translator(og_pdffile,language)
            # flash(f"Your File has been compressed and is available for download")
            # return render_template("ocr.html")


            # # else:
            # #     flash('Unsupported file type')
            # #     return "Unsupported file type"

            # flash(f"Your File has been compressed and is available for <a href='{compressed_file}' target='_blank' >download</a>")
            # return render_template("compressor.html", compressed_file=compressed_file)
        
    
        


        return render_template("index.html")
        




@app.route("/convert",methods=['GET','POST'])
def convert():
      if request.method == "POST":
        operations = request.form.get("operations")

        if 'file' not in request.files:
            flash('No file part')
            return "Error!"

        file = request.files['file']
        multipleFiles =  request.files.getlist("file")
        if file.filename == '':
            flash('No selected file')
            return "No selected file"
         
        if len(multipleFiles) >= 2:
                  i=1
                  mf = []       
                  for file in multipleFiles:                      
                       file.save(os.path.join(app.config['UPLOAD_FOLDER'],str(i)+'.pdf'))
                       mf.append(str(i)+'.pdf')
                       i=i+1
                #   print(mf)
                  
                  match operations:
                    case "mergepdf":
                        try:
                            og_pdffile = f"static/uploads/"
                            location = f"static/conversionArea/"
                            merge_pdf(og_pdffile,location,mf)
                            drop_location = f"static/conversionArea/merged-pdf.pdf"
                            flash(f"Your PDF has been Merged and is available for <a href='{drop_location}' target='_blank' >download</a>")
                            return render_template("compressor.html", compressed_file=drop_location)
                        except:
                            flash(f"You are uploading doc file & telling me to convert PDF in to Doc ")
                            return render_template("convertor.html")
                
                    
        # elif file and allowed_file(file.filename):
        else:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))       
            extension = os.path.splitext(filename)[1].lower()
            name = os.path.splitext(filename)[0].lower()
            print("Extension-------------------------------------",extension)
            if extension in {'.png', '.jpg', '.jpeg', '.gif'}:
                og_file = f"static/uploads/{filename}"
                with Image.open(og_file) as img:
                    # img_width = img.size[0]
                 match operations:

                        case "imagetopdf":
                            try: 
                                drop_location = f"static/conversionArea/{name}.pdf"
                                convert_img_to_pdf(og_file,drop_location,name)
                            except:
                                flash(f"You are asking for inappropriate Action")
                                return render_template("convertor.html")
                        case "jpgtopng":
                           try:
                                dropout_location = f"static/conversionArea/"
                                convert_jpg_to_png(og_file,dropout_location,name)
                                drop_location = f"static/conversionArea/{name}.png"
                                flash(f"Your Image File has been converted to PNG Format and is available for <a href='{drop_location}' target='_blank' >download</a>")
                                return render_template("convertor.html", compressed_file=drop_location) 
                                # cv2.imwrite(f"static/conversionArea/{name}.png",og_file)
                           except:
                                flash(f"you are asking for inappropriate Action Error Here..")
                                return render_template("convertor.html")
                           
                        case "pngtojpg":
                            try:
                                dropout_location = f"static/conversionArea/"
                                convert_png_to_jpg(og_file,dropout_location,name)
                                drop_location = f"static/conversionArea/{name}.jpg"
                                flash(f"Your Image File has been converted to JPG Format and is available for <a href='{drop_location}' target='_blank' >download</a>")
                                return render_template("convertor.html", compressed_file=drop_location) 
                            except:
                                 flash(f"you are asking for inapppropriate Action Error in converting to JPG")
                                 return render_template("convertor.html")
                       
                        case other:                   
                            flash(f"You Have Asking for inappropriate request by uploading inapprpropriate file")
                            return render_template("convertor.html")
                     
                flash(f"Your Image File has been converted to PDF and is available for <a href='{drop_location}' target='_blank' >download</a>")
                return render_template("convertor.html", compressed_file=drop_location)   
        

       
            # elif extension =='.pdf':
            else:
            
                og_pdffile = f"static/uploads/{filename}"
                # drop_location = f"static/conversionArea/"
       
                match operations:

               
                    case "pdftodoc":
                        try:
                               
                            drop_location = f"static/conversionArea/output.docx"
                            convert_pdf_to_docx(og_pdffile,drop_location)
                            flash(f"Your PDF has been converted to DOC and is available for <a href='{drop_location}' target='_blank' >download</a>")
                            return render_template("convertor.html", compressed_file=drop_location)
                        except:
                            flash(f"You are uploading doc file & telling me to convert PDF in to Doc ")
                            return render_template("convertor.html")

                        
                    case "doctopdf":
                        try:
                          
                                drop_location = f"static/conversionArea/{name}.pdf"
                                location = "static/conversionArea/"
                                convert_docx_to_pdf(og_pdffile,location)
                                flash(f"Your DOC has been converted to PDF and is available for <a href='{drop_location}' target='_blank' >download</a>")
                                return render_template("convertor.html", compressed_file=drop_location)
                        except:
                            flash(f"You are uploading PDF file & telling me to convert Doc in to PDF ")
                            return render_template("convertor.html")
                                        
                    case "pdftoimage":
                        try:
                              location = f"static/conversionArea/"
                              convert_pdf_to_img(og_pdffile,location)
                              drop_location = f"static/conversionArea/Artify.zip"
                              flash(f"Your PDF has been converted to Image and is available for <a href='{drop_location}' target='_blank' >download</a>")
                              return render_template("convertor.html", compressed_file=drop_location)

                        except:
                            flash(f"You are perform inappropriate Action, Try Again")
                            return render_template("convertor.html")            
                
                    case other:
                         flash(f"You Have Asking for inappropriate request by uploading inapprpropriate file")
                         return render_template("convertor.html")

              

        # else:
        #         flash('Unsupported file type')
        #         return render_template("convertor.html")

        
      return render_template("index.html")



@app.route('/compress', methods=['GET','POST'])
def compress():
    if request.method == "POST":
        operations = request.form.get("operations")

        if 'file' not in request.files:
            flash('No file part')
            return "Error!"

        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return "No selected file"
   
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        
            extension = os.path.splitext(filename)[1].lower()
            print("Extension-------------------------------------",extension)
 
            if extension in {'.png', '.jpg', '.jpeg', '.gif'}:
                og_file = f"static/uploads/{filename}"

                with Image.open(og_file) as img:
                    img_width = img.size[0]

                    match operations:
                        case "low":
                            img_width //= 2
                        case "medium":
                            img_width //= 3
                        case "high":
                            img_width //= 5
                        case "veryhigh":
                            img_width //= 7

                compressed_file = f"/static/compressedArea/{filename}"
                compresion(og_file, filename, img_width)
                
            # elif extension =='.pdf':
            else:
                # pdf=PdfFileReader(filename)
                og_pdffile = f"static/uploads/{filename}"
                compresion_level = None

                match operations:
                    case "low":
                        compresion_level = 3
                    case "medium":
                        compresion_level = 6
                    case "high":
                        compresion_level = 9
                    case "veryhigh":
                        compresion_level = 9

                if compresion_level is not None:
                    drop_location = f"static/compressedArea/{filename}"
                    pdf_Compressor(og_pdffile, compresion_level,filename)
                    flash(f"Your File has been compressed and is available for <a href='{drop_location}' target='_blank' >download</a>")
                    return render_template("compressor.html", compressed_file=drop_location)


            # else:
            #     flash('Unsupported file type')
            #     return "Unsupported file type"

            flash(f"Your File has been compressed and is available for <a href='{compressed_file}' target='_blank' >download</a>")
            return render_template("compressor.html", compressed_file=compressed_file)
        
    
        


    return render_template("index.html")

    







@app.route("/edit",methods=["GET","POST"])
def edit():

    if request.method == "POST":
        operations = request.form.get("operations")
    
         # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return "Error ! "
        
        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return "No selected file "
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            ProcessImage(filename,operations)
            edited_image =f'/static/processArea/{filename}'
            og_image = f'static/uploads/{filename}'
            og_file = f'static/uploads/{filename}'
            file_conversion ='/static/processArea/output.docx'
            extension = os.path.splitext(filename)[1].lower()

        # Check file size
            size = os.path.getsize(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            flash(f"Your Image has been processed and is available <a href='/static/processArea/{filename}' target='_blank' >here </a>")
            return render_template("zone.html",edited_image= edited_image,og_image= og_image,extension=extension,size=size,og_file=og_file,file_conversion=file_conversion)
            # return redirect("/",edited_image= edited_image,og_image= og_image)
   

        # return "post request here "
        
        return render_template("index.html")




@app.route("/analyze",methods=['GET','POST'])
def analyze():
       if request.method == "POST":
        if 'file' not in request.files:
            flash('No file part')
            return "Error!"

        file = request.files['file']
        job_description = request.form['jobDescription']
        print("---job description debugging------:",job_description)
     
        if file.filename == '':
            flash('No selected file')
            return "No selected file"
   
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['RESUME_UPLOAD_FOLDER'], filename))        
            # extension = os.path.splitext(filename)[1].lower()
            # print("Extension-------------------------------------",extension)
            
            name = os.path.splitext(filename)[0].lower()
                # pdf=PdfFileReader(filename)
            og_pdffile = f"static/analyzeArea/{filename}"
            drop_location = f"static/analyzeArea/{name}.pdf"
            doc_location = f"static/analyzeArea/"
    
            Insight =Analyzer(og_pdffile,doc_location,job_description)
            flash(f"Your File has been compressed and is available for download")
            
            return render_template("AI_ResumeAnalyzer.html", Insight=Insight)
            
        

        return render_template("index.html")


# @app.route("/upload-chat-file",methods=['GET','POST'])
# def upload_chat_file():
#        if request.method == "POST":
#         if 'file' not in request.files:
#             flash('No file part')
#             return "Error!"

#         file = request.files['file']
 
#         if file.filename == '':
#             flash('No selected file')
#             return "No selected file"
   
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['CHAT_UPLOAD_FOLDER'], filename)) 
#             chat_location = f"static/chatVisualizer/{filename}"

#             data=user_Selection(chat_location) 
#             # redirect(url_for("visualize"))
#             return render_template("AI_ChatVisualizer.html",  data=data,filename=filename)
        

#         return render_template("index.html")
       
# @app.route("/visualize",methods=['GET','POST'])
# def visualize():
#        if request.method == "POST":
#             filename = request.form.get("filename")
#             operations = request.form.get("operations")    
#             chat_location = f"static/chatVisualizer/{filename}"
#             # print(f"Uploaded Filename: {filename}")
#             # print(f"Chat Location: {chat_location}")
#             drop_location = f"static/chatVisualizer/"
#             # doc_location = f"static/analyzeArea/" 
          
#             analytical_data= Analyze_Chat(chat_location,operations,drop_location)

#             flash(f"Your File has been compressed and is available for download")
#             return render_template("AI_ChatVisualizer.html", analytical_data= analytical_data,filename=filename )
        

#        return render_template("index.html")

@app.route("/select-analysis-type", methods=['POST'])
def upload_chat_file():
    if 'file' not in request.files:
        flash('No file part')
        return "Error!"

    file = request.files['file']

    if file.filename == '':
        flash('No selected file')
        return "No selected file"

    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['CHAT_UPLOAD_FOLDER'], filename))
    chat_location = f"static/chatVisualizer/{filename}"

    data = user_Selection(chat_location)
    return render_template("ChatVisualizer.html", data=data, filename=filename)

@app.route("/visualize", methods=['POST'])
def visualize():
    filename = request.form.get("filename")
    operations = request.form.get("operations")

    if not filename:
        flash('No filename provided')
        return "No filename provided"

    chat_location = f"static/chatVisualizer/{filename}"
    drop_location = "static/chatVisualizer/"
    analytical_data = Analyze_Chat(chat_location, operations, drop_location)
    data = user_Selection(chat_location)

    flash(f"Your File has been compressed and is available for download")
    return render_template("ChatVisualizer.html", analytical_data=analytical_data,data=data, filename=filename)

     

     

app.run(debug=True)
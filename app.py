from flask import Flask,render_template,redirect,request,flash,request
from werkzeug.utils import secure_filename
import os
from convertor import convert_pdf_to_docx,convert_docx_to_pdf,convert_img_to_pdf,convert_pdf_to_img,merge_pdf
from compressor import compresion,pdf_Compressor
from processor import ProcessImage
from PIL import Image



UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'webp', 'jpeg', 'gif','pdf','docx','zip'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "yo"




def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route("/")
def home():
    return render_template("index.html")

@app.route("/zone")
def zone():
    return render_template("zone.html")

@app.route("/compressor")
def compressor():
    return render_template("compressor.html")


@app.route("/convertor")
def convertor():
    return render_template("convertor.html")

@app.route("/ocr")
def ocr():
    return render_template("ocr.html")


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



app.run(debug=True)

import cv2 
import numpy as np 
import requests
from  rembg import remove
from skimage import io
from PIL.ImageFilter import(BLUR,CONTOUR,EMBOSS,FIND_EDGES,SMOOTH_MORE,SHARPEN,) 
from PIL import Image
import scipy.ndimage
import imageio
import matplotlib.pyplot as plt

def dodge(front,back): 
    result=front*255/(255-back)  
    result[result>255]=255 
    result[back==255]=255 
    return result.astype('uint8')

def Highlight_Pixels(src, gamma):
    invGamma = 5/ gamma

    table = [((i / 255) ** invGamma) * 255 for i in range(256)]
    table = np.array(table, np.uint8)

    return cv2.LUT(src, table)


def Cartoonify(img):
    # Convert the input image to gray scale 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges  = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 9, 8)
    # Defining input data for clustering
    data = np.float32(img).reshape((-1, 3))
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
    # Applying cv2.kmeans function
    _, label, center = cv2.kmeans(data, 5, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    center = np.uint8(center)
    # Reshape the output data to the size of input image
    result = center[label.flatten()]
    result = result.reshape(img.shape)
    blurred = cv2.medianBlur(result, 3)
    cartoon = cv2.bitwise_and(blurred, blurred, mask=edges)
    return cartoon
    


def ProcessImage(filename, operations):
    
    print(f"the operation is {operations} and filename is {filename}")
   
    kernel = np.ones((5, 5), np.uint8)
    match operations:
        case "cgs":
            img = cv2.imread(f"static/uploads/{filename}")
            imgProcessed = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            cv2.imwrite(f"static/processArea/{filename}", imgProcessed)

        case "sketch":
            start_img = imageio.imread(f"static/uploads/{filename}")
            gray_img=np.dot(start_img[...,:3], [0.299, 0.587, 0.114])
            inverted_img = 255-gray_img
            blur_img = scipy.ndimage.filters.gaussian_filter(inverted_img,sigma=15)
            final_img= dodge(blur_img,gray_img)
            plt.imsave(f"static/processArea/{filename}", final_img, cmap="gray", vmin=0, vmax=255)



        case "removebg":
            img = cv2.imread(f"static/uploads/{filename}")
            imgProcessed = remove(img)
            cv2.imwrite(f"static/processArea/{filename}", imgProcessed)

        case "dilateimage":
            img = cv2.imread(f"static/uploads/{filename}")
            dilation = cv2.dilate(img, kernel, iterations=2)
            cv2.imwrite(f"static/processArea/{filename}", dilation)

        case "erodeimage":
            img = cv2.imread(f"static/uploads/{filename}")
            erosion = cv2.erode(img, kernel, iterations=2)
            cv2.imwrite(f"static/processArea/{filename}", erosion)

        case "gradientimage":
            img = cv2.imread(f"static/uploads/{filename}")
            gradient = cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel)
            cv2.imwrite(f"static/processArea/{filename}", gradient)

        case "sharpenimage": 
            img = Image.open(f"static/uploads/{filename}") 
            sharpenimage = img.filter(SHARPEN) 
            sharpenimage.save(f"static/processArea/{filename}")


        case "contourimage":
            img = Image.open(f"static/uploads/{filename}") 
            contourimage = img.filter(CONTOUR) 
            contourimage.save(f"static/processArea/{filename}")

        case"blurimage": 
           img = Image.open(f"static/uploads/{filename}") 
           blurimage = img.filter(BLUR)   
           blurimage.save(f"static/processArea/{filename}")

        case"findedgesimage": 
           img = Image.open(f"static/uploads/{filename}") 
           findedgesimage = img.filter(FIND_EDGES)   
           findedgesimage.save(f"static/processArea/{filename}")

        case"emboseimage": 
           img = Image.open(f"static/uploads/{filename}")
           embose_image = img.filter(EMBOSS)   
        #    cv2.imwrite(f"static/processArea/{filename}", embose_image)
           embose_image.save(f"static/processArea/{filename}")

        case"smoothingmoreimage": 
           img = Image.open(f"static/uploads/{filename}")
           smoothingmoreimage = img.filter(SMOOTH_MORE)   
           smoothingmoreimage.save(f"static/processArea/{filename}")

        case "highlighting_pixel":
            img = io.imread(f"static/uploads/{filename}")
            r_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            gamma = 2.5      # change the value here to get different result
            highlight_adjusted = Highlight_Pixels(r_img, gamma=gamma)
            cv2.imwrite(f"static/processArea/{filename}", highlight_adjusted)

        case "addlightimage":
            img = io.imread(f"static/uploads/{filename}")
            r_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            gamma = 7.5      # change the value here to get different result
            highlight_adjusted = Highlight_Pixels(r_img, gamma=gamma)
            cv2.imwrite(f"static/processArea/{filename}", highlight_adjusted)

        case "enhancement":
            img = cv2.imread(f"static/uploads/{filename}")
            enhancement =cv2.detailEnhance(img,sigma_r=0.15,sigma_s=10)
            cv2.imwrite(f"static/processArea/{filename}", enhancement)

        case "cartoonify":
            img = cv2.imread(f"static/uploads/{filename}")
            cartoonify = Cartoonify(img)
            cv2.imwrite(f"static/processArea/{filename}", cartoonify)

        



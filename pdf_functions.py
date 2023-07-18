#####
###
## 00 Imports
## 01 Constants
## 02 Functions
###
#####




#####
###
## 00 Imports
###
#####
import os
import fitz
from PIL import Image
import pytesseract as tess
from pytesseract import image_to_string




#####
###
## 01 Constants
###
#####
# tess.pytesseract.tesseract_cmd = r"C:/Users/c082494/AppData/Local/Programs/Tesseract-OCR/tesseract.exe" # main
# tess.pytesseract.tesseract_cmd = r'C:\Users\c055981\AppData\Local\Programs\Tesseract-OCR\tesseract.exe' # Shawn Labby
# tess.pytesseract.tesseract_cmd = r'C:\Users\c008892\AppData\Local\Programs\Tesseract-OCR\tesseract.exe' # Mark Hughes




#####
###
## 02 Functions
###
#####
def delete_image_files(png_dir):
    png_list = [f for f in os.listdir(png_dir) if f.endswith(".png")]
    for img in png_list:
        os.remove(os.path.join(png_dir, img))





def convert_pdf_to_png(filename, png_dir):
    doc = fitz.open(filename)
    i = 1
    page_counter = 0
    for page in doc:
        pix = page.get_pixmap(dpi=200)  # render page to a high resolution (dpi) image
        pix.save(png_dir + "page_" + str(i) + ".png")
        i += 1
        page_counter += 1




def convert_png_to_string(png_dir, chosen_cnumber):
    tess.pytesseract.tesseract_cmd = r"C:/Users/" + chosen_cnumber + r'/AppData/Local/Programs/Tesseract-OCR/tesseract.exe'
    text = ''
    page_counter = len([f for f in os.listdir(png_dir) if f.endswith(".png")])
    for image_counter in range(1, page_counter + 1):
        image = Image.open(png_dir + 'page_' + str(image_counter) + '.png')
        text += "PythonPDFPage" + str(image_counter) + "\n"
        text += image_to_string(image)
        image.close()
        os.remove(png_dir + 'page_' + str(image_counter) + '.png')
    return text, page_counter




if __name__ == "__main__":
    delete_image_files(png_dir="C:/Users/C082494/PycharmProjects/EHR_v1_000/99 Supporting Files - Dont Touch/02 PDF pngs/")
    convert_pdf_to_png(filename="C:/Users/C082494/PycharmProjects/EHR_v1_000/99 Supporting Files - Dont Touch/Ryans_Note.pdf",
                       png_dir="C:/Users/C082494/PycharmProjects/EHR_v1_000/99 Supporting Files - Dont Touch/02 PDF pngs/"
                       )
    x, y = convert_png_to_string(png_dir="C:/Users/C082494/PycharmProjects/EHR_v1_000/99 Supporting Files - Dont Touch/02 PDF pngs/",
                                chosen_cnumber="c082494"
                                )
    print(x)
import os
import re
import spacy
import matplotlib
import matplotlib.pyplot as plt
import pytesseract
import skimage.io

from constants import *
from skimage.color import rgb2gray
from skimage.filters import (threshold_otsu, threshold_niblack, threshold_sauvola)
from syltippy import syllabize
from PIL import Image
from pdf2image import convert_from_path
from perspicuity.perspicuity import *
from posixpath import split


tagger="tokenizer\\postagger\\models\\spanish-ud.tagger"
jar="tokenizer\\postagger\\stanford-postagger.jar"
number_pages = 0

def create_images_from_file(values):
        file_pil_images = convert_from_path(values['file_path'], values['dpi'])
        create_images(file_pil_images)
       
def create_images(pil_images):
    page_number = 1
    for image in pil_images:
        file_name = define_file_name(page_number)
        file_path = define_file_path(file_name)
        image.save(file_path, 'JPEG')
        page_number += 1
        break
    global number_pages
    number_pages = page_number

def refine_image(values): #Falta extraer de esta función
        for i in range(1, values['last_page_number'] + 1):
            file_name = define_file_name(i)
            file_path = define_file_path(file_name)

            original_image = skimage.io.imread(file_path)
            image = rgb2gray(original_image)
            pilimage = Image.open(file_path)
            width, height = pilimage.size
            pilimage.close()

            image.shape
            thresh_otsu = threshold_otsu(image)
            binary_otsu = image > thresh_otsu

            plot_configs = {'width': width, 'height': height, 'dpi': 900, 'file_path': DOCS_ROUTE+'plt-'+file_name}
            plot_image(plot_configs, binary_otsu)

            text = str(((pytesseract.image_to_string(Image.open(DOCS_ROUTE+'plt-'+file_name),lang='spa'))))
            text = text.replace('-\n', '')
            values['file_to_read'].write(text)
        values['file_to_read'].close()

def plot_image(plot_configs, binary_otsu):
    matplotlib.rcParams['font.size'] = 12
    mult=5
    plt.figure(figsize=((int)(plot_configs['width']/plot_configs['dpi'])*mult, (int)(plot_configs['height']/plot_configs['dpi'])*mult))
    plt.imshow(binary_otsu, cmap=plt.cm.gray)
    plt.axis('off')
    plt.savefig(plot_configs['file_path'], bbox_inches='tight')

def define_file_name(number): 
    return 'pagina_'+ str(number) + '.jpg'

def define_file_path(file_name):
    return DOCS_ROUTE+file_name

def delete_files():
    global number_pages
    number_pages = number_pages
    for i in range(1, number_pages):
        file_name = define_file_name(i)
        file_path = define_file_path(file_name)
        os.remove(file_path)
        os.remove(DOCS_ROUTE+'plt-'+file_name) #Reutilizado 3 veces

def refine_text(Lines):
    raw_text = extract_file_text(Lines)
    return substract_from_text(raw_text)

def extract_file_text(Lines):
    text_raw = ''
    for line in Lines:
        text_raw += line
    return text_raw

def substract_from_text(raw_text):
    raw_text = re.sub(r'[0-9]+', '', raw_text)
    raw_text = re.sub(r'@', '', raw_text)
    raw_text = re.sub(r'(  +)', ' ', raw_text)
    raw_text = re.sub(r'(\.|\!|\?|\:)[\r\n][\r\n]+', '.@', raw_text)
    refined_text = re.sub(r'[\r\n][\r\n]+', '', raw_text)
    return refined_text
    
def calculate_amount(values): #renombrar
    counter = 0
    for value in values:
        counter += 1
    return counter

def calculate_syllables(words):
    syllables_counter = 0
    for word in words:
        syllables_counter += get_word_syllables(word)
    return syllables_counter

def get_word_syllables(word):
    syllables, stress = syllabize(u'{}'.format(word.text))
    return len(syllables)

def calculate_perspicuity(perspicuity_values):
    return {
        "SzigrisztPazosLong": SzigrisztPazosLong(perspicuity_values).calculate(),    
        "SzigrisztPazosShort": SzigrisztPazosShort(perspicuity_values).calculate()
    }

pdf_configs = {'dpi':900, 'file_path': define_file_path(PDF_FILE)}
create_images_from_file(pdf_configs)

file_to_read = open(OUTPUT_TEXT, "a", encoding="utf-8")
image_cleaner_configs = {'last_page_number': number_pages-1, 'file_to_read': file_to_read}
refine_image(image_cleaner_configs)

delete_files()

nlp = spacy.load(OCR_MODEL)

with open(OUTPUT_FILE, "a", encoding="utf-8") as text_file:
    raw_file = open(OUTPUT_TEXT, "r")
    Lines = raw_file.readlines()
    refined_text = refine_text(Lines)
    pharagraphs = refined_text.split('@')

    results = []

    for pharagraph in pharagraphs:
        tokenized_pharagraph = nlp(pharagraph)
            
        word_counter = calculate_amount(tokenized_pharagraph)
        phrases_counter = calculate_amount(tokenized_pharagraph.sents)
        syllables_counter = calculate_syllables(tokenized_pharagraph)
           
        perspicuity_values = {'words': word_counter, 'phrases': phrases_counter, 'syllables':syllables_counter }
        result = calculate_perspicuity(perspicuity_values)

        print([pharagraph, {"palabrasParrafo":word_counter, "frasesParrafo":phrases_counter, "silabasParrafo":syllables_counter, 'perspicuidad':result}]) 
        results.append([pharagraph, {"palabrasParrafo":word_counter, "frasesParrafo":phrases_counter, "silabasParrafo":syllables_counter, 'perspicuidad':result}])  
        
    for result in results:
        print(result, file=text_file)
import os
import re
import spacy
import matplotlib
import matplotlib.pyplot as plt
import pytesseract
import skimage.io
from spacy.lang.es.stop_words import STOP_WORDS

from unidecode import unidecode
from constants import *
from skimage.color import rgb2gray
from skimage.filters import (threshold_otsu, threshold_niblack, threshold_sauvola)
from syltippy import syllabize
from PIL import Image
from pdf2image import convert_from_path
from perspicuity.perspicuity import *
from pdf import *
from posixpath import split
import sys
from PyQt6.QtWidgets import (QApplication)
from gui import MainWindow

number_pages = 0
first_page = 1
last_page = 1

def create_images_from_file(values, updateProgress, end_page):
        file_pil_images = convert_from_path(values['file_path'], values['dpi'])
        create_images(file_pil_images, values['first_page'], values['last_page'], end_page, updateProgress)
       
def create_images(pil_images, first_page, last_page, end_page, updateProgress):
    page_number = 1
    
    for image in pil_images:
        if page_number>=first_page and page_number <=last_page:
            file_name = define_file_name(page_number)
            file_path = define_file_path(file_name)
            image.save(file_path, 'JPEG')
            updateProgress.emit()
        page_number += 1 if page_number<end_page else 0
        
    global number_pages
    number_pages = page_number

def refine_image(values, updateProgress): #Falta extraer de esta función
    first_page= values['first_page']
    last_page=values['last_page']
    for i in range(first_page, last_page+1):
        
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
        updateProgress.emit()
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

def delete_files(first_page, last_page, updateProgress):
    global number_pages
    number_pages = number_pages
    for i in range(first_page, last_page+1):
        file_name = define_file_name(i)
        file_path = define_file_path(file_name)
        os.remove(file_path)
        os.remove(DOCS_ROUTE+'plt-'+file_name) #Reutilizado 3 veces
    updateProgress.emit()

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
    raw_text = raw_text.encode("latin-1","ignore").decode("latin-1")
    refined_text = re.sub(r'[\r\n]+', ' ', raw_text)
    return refined_text
    
def calculate_phrases(phrases): 
    counter = 0
    
    for phrase in phrases:
        counter += 1
    return counter

def calculate_words(words):
    counter = 0
    
    for word in words:
        if word.pos_ != "PUNCT" and word.pos_ != "SYM":
            counter += 1
    return counter

def calculate_syllables(words):
    syllables_counter = 0
    for word in words:
        if word.pos_ != "PUNCT" and word.pos_ != "SYM":
            syllables_counter += get_word_syllables(word)
    return syllables_counter

def get_word_syllables(word):
    syllables, stress = syllabize(u'{}'.format(word.text))
    return len(syllables)


def get_letters_per_word(words):
    letters_counter = []
    for word in words:
        if word.pos_ != "PUNCT" and word.pos_ != "SYM":
            letters_counter.append(len(word))
    
    return letters_counter

def calculate_perspicuity(perspicuity_values):
    return {
        "SzigrisztPazosLong": SzigrisztPazosLong(perspicuity_values).calculate(),    
        "SzigrisztPazosShort": SzigrisztPazosShort(perspicuity_values).calculate(),
        "FernandezHuerta": FernandezHuerta(perspicuity_values).calculate(),
        "MuLegibility": MuLegibility(perspicuity_values).calculate(),
    }

def plot_perspicuity_values(perspicuity_values):
    fig = plt.figure()

    pers_formulas = []
    pers_values = []
    for key, value in perspicuity_values.items():
        if value != None:
            pers_formulas.append(key)
            pers_values.append(value)
    print(pers_formulas)
    print(pers_values)
    
    ax = fig.add_subplot(111)
    bars = ax.bar(pers_formulas,pers_values, color=['black', 'red', 'green', 'blue', 'cyan'])
    ax.bar_label(bars)

    plt.xlabel("Formulas")
    plt.ylabel("Escala de perspicuidad")
    plt.title("Valores de perspicuidad para el parrafo")
    #plt.show()
def generatePDF(updateProgress):
    pdf = PDF()#pdf object
    pdf.add_page()
    pdf.titles("ANÁLISIS DE LEGIBILIDAD")
    pdf.resumen()
    pdf.output('test.pdf','F')
    updateProgress.emit()

def clean_output_file():
    cfile = open(OUTPUT_FILE, "w", encoding="utf-8")
    cfile.write("")
    cfile.close()

def process_file(process_configs, updateProgress):
    pdf_configs = {'dpi':900, 'file_path': process_configs['file'], 'first_page': process_configs['first_page'], 'last_page': process_configs['last_page']}
    updateProgress.emit()
    create_images_from_file(pdf_configs, updateProgress, process_configs['page_total'])

    file_to_read = open(OUTPUT_TEXT, "a", encoding="utf-8")
    last_page = process_configs['last_page'] if process_configs['last_page']<number_pages else number_pages
    image_cleaner_configs = {'file_to_read': file_to_read, 'first_page': process_configs['first_page'], 'last_page': last_page}
    refine_image(image_cleaner_configs, updateProgress)

    delete_files(process_configs['first_page'], last_page, updateProgress)

    nlp = spacy.load(OCR_MODEL)

    clean_output_file()

    with open(OUTPUT_FILE, "a", encoding="utf-8") as text_file:
        raw_file = open(OUTPUT_TEXT, "r", encoding="utf-8")
        Lines = raw_file.readlines()
        refined_text = refine_text(Lines)
        pharagraphs = refined_text.split('@')
        results = []
        
        for pharagraph in pharagraphs:
            tokenized_pharagraph = nlp(pharagraph)

            letters_counter = get_letters_per_word(tokenized_pharagraph)

            word_counter = calculate_words(tokenized_pharagraph)
            phrases_counter = calculate_phrases(tokenized_pharagraph.sents)
            syllables_counter = calculate_syllables(tokenized_pharagraph)
            
            perspicuity_values = {'words': word_counter, 'phrases': phrases_counter, 'syllables':syllables_counter, 'letters': letters_counter }
            result = calculate_perspicuity(perspicuity_values)

            plot_perspicuity_values(result)
            print([pharagraph, {"palabrasParrafo":word_counter, "frasesParrafo":phrases_counter, "silabasParrafo":syllables_counter, 'perspicuidad':result}]) 
            results.append([pharagraph, {"palabrasParrafo":word_counter, "frasesParrafo":phrases_counter, "silabasParrafo":syllables_counter, 'perspicuidad':result}])  
        updateProgress.emit()
        for result in results:
            print(result, file=text_file)
        updateProgress.emit()        
        generatePDF(updateProgress)

app = QApplication(sys.argv)

window = MainWindow(process_file)

window.show()
sys.exit(app.exec())
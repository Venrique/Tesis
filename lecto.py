import os
import re
from spacy import load, parts_of_speech, lexeme, tokens

import matplotlib
import matplotlib.pyplot as plt
import pytesseract
import skimage.io
import ctypes
import es_core_news_sm

from constants import *
from skimage.color import rgb2gray
from skimage.filters import (threshold_otsu, thresholding)

from syltippy import syllabize
from PIL import Image
from pdf2image import convert_from_path
from perspicuity.perspicuity import *
from pdf import *
import sys
from PyQt6.QtWidgets import (QApplication)
from PyQt6.QtGui import QIcon
from gui import MainWindow

number_pages = 0
first_page = 1
last_page = 1
Image.MAX_IMAGE_PIXELS = None
basedir = os.path.dirname(__file__)

#Convierte las páginas de un archivo PDF a imágenes y las guarda en un arreglo
def create_images_from_file(values, updateProgress, work):
    file_pil_images = []
    blocks = range(values['first_page'], values['last_page']+1, 10)
    index = 1
    steps = len(blocks)
    for page in blocks:
        updateProgress.emit("Leyendo PDF (bloque "+str(index)+" de "+str(steps)+")" if work[0] else "Cancelando...")
        index += 1
        if work[0]:
            file_pil_images.extend(convert_from_path(values['file_path'], dpi=values['dpi'], first_page=page, last_page = min(page+10-1,values['last_page'])))
        else:
            file_pil_images.extend([""]*min(page+10-1,values['last_page']))

    updateProgress.emit("Creando imagen de página "+str(values['first_page'])+"..." if work[0] else "Cancelando...")
    create_images(file_pil_images, values['first_page'], values['last_page'], updateProgress, work)

#Guarda las imágenes creadas en la ruta especificada
def create_images(pil_images, first_page, end_page, updateProgress, work):
    page_number = first_page
    for image in pil_images:
        if work[0]:
            file_name = define_file_name(page_number)
            file_path = define_file_path(file_name)
            image.save(file_path, 'JPEG')
        if page_number<end_page:
            updateProgress.emit("Creando imagen de página "+str(page_number+1)+"..." if work[0] else "Cancelando...")
        else:
            updateProgress.emit("Procesando imagen de página "+str(first_page)+"..." if work[0] else "Cancelando...")
        page_number += 1 if page_number<end_page else 0
    
    global number_pages
    number_pages = page_number

#La imagen se convierte primero a escala de grises y luego se binariza para obtener mejores resultados
def refine_image(values, updateProgress, work):
    first_page= values['first_page']
    last_page=values['last_page']
    for i in range(first_page, last_page+1):
        if work[0]:
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

            plot_configs = {'width': width, 'height': height, 'dpi': 700, 'file_path': DOCS_ROUTE+'plt-'+file_name}
            plot_image(plot_configs, binary_otsu)
            text = str(((pytesseract.image_to_string(Image.open(DOCS_ROUTE+'plt-'+file_name),lang='spa'))))
            text = text.replace('-\n', '')
            values['file_to_read'].write(text)
        if i<last_page:
            updateProgress.emit("Procesando imagen de página "+str(i+1)+"..." if work[0] else "Cancelando...")
        else:
            updateProgress.emit("Limpiando almacenamiento..." if work[0] else "Cancelando...")
    values['file_to_read'].close()

#Se crea la imagen binarizada y se guarda. La imagen en escala de grises se desecha 
def plot_image(plot_configs, binary_otsu):
    matplotlib.rcParams['font.size'] = 12
    mult=5
    plt.figure(figsize=((int)(plot_configs['width']/plot_configs['dpi'])*mult, (int)(plot_configs['height']/plot_configs['dpi'])*mult))
    plt.imshow(binary_otsu, cmap=plt.cm.gray)
    plt.axis('off')
    plt.savefig(plot_configs['file_path'], bbox_inches='tight')
    plt.cla()
    plt.close()

def define_file_name(number): 
    return 'pagina_'+ str(number) + '.jpg'

def define_file_path(file_name):
    return DOCS_ROUTE+file_name

#Elimina las imagenes originales, a las que no se les ha aplicado ningún algoritmo de procesamiento de imágenes
def delete_files(first_page, last_page, updateProgress, work):
    global number_pages
    number_pages = number_pages
    for i in range(first_page, last_page+1):
        file_name = define_file_name(i)
        file_path = define_file_path(file_name)
        try:
            os.remove(file_path)
            os.remove(DOCS_ROUTE+'plt-'+file_name)
        except Exception as e:
            continue
    updateProgress.emit("Limpiando texto plano..." if work[0] else "Cancelando...")

#Devuelve el texto depurado 
def refine_text(Lines):
    raw_text = extract_file_text(Lines)
    return substract_from_text(raw_text)

#Junta todas las líneas de un texto en una sola variable
def extract_file_text(Lines):
    text_raw = ''
    for line in Lines:
        text_raw += line
    return text_raw

#Limpia el texto usando expresiones regulares
def substract_from_text(raw_text):
    raw_text = re.sub(r'[0-9](\.[0-9]+)*', '', raw_text)
    raw_text = re.sub(r'@', '', raw_text)
    raw_text = re.sub(r'(  +)', ' ', raw_text)
    raw_text = re.sub(r'(\.|\!|\?|\:)[\r\n\v\f][\r\n\v\f ]+', r'\1@', raw_text)
    raw_text = raw_text.encode("latin-1","ignore").decode("latin-1")
    refined_text = re.sub(r'[\r\n\t\v\f]+', ' ', raw_text)
    return refined_text

#Cuenta la cantidad de frases en un párrafo  
def calculate_phrases(phrases): 
    counter = 0
    
    for phrase in phrases:
        counter += 1
    return counter

#Cuenta la cantidad de palabras en un párrafo
def calculate_words(words):
    counter = 0
    
    for word in words:
        if word.pos_ != "PUNCT" and word.pos_ != "SYM":
            counter += 1
    return counter

#Cuenta la cantidad de sílabas en un párrafo
def calculate_syllables(words):
    syllables_counter = 0
    for word in words:
        if word.pos_ != "PUNCT" and word.pos_ != "SYM":
            syllables_counter += get_word_syllables(word)
    return syllables_counter

#Extrae las sílabas de cada palabra
def get_word_syllables(word):
    syllables, stress = syllabize(u'{}'.format(word.text))
    return len(syllables)

#Cuenta las letras en una palabra
def get_letters_per_word(words):
    letters_counter = []
    for word in words:
        if word.pos_ != "PUNCT" and word.pos_ != "SYM":
            letters_counter.append(len(word))
    
    return letters_counter

#Evalúa las fórmulas de perspicuidad con los datos obtenidos y obtiene los resultados
def calculate_perspicuity(perspicuity_values):
    return {
        SIGRISZPAZOS: round(SzigrisztPazos(perspicuity_values).calculate(),2),    
        FERNANDEZHUERTA: round(FernandezHuerta(perspicuity_values).calculate(),2),
        MULEGIBILITY: round(MuLegibility(perspicuity_values).calculate(),2),
    }

#Crea el archivo PDF que muestra los resultados obtenidos y los gráficos
def generatePDF(updateProgress, values_to_print, file_route, file_name, sorted_formulas, generate_complete_report, pdf_complete_report, number_of_pharagraphs, work):
    if work[0]:
        pdf = PDF()
        pdf.add_page()
        pdf.titles("ANÁLISIS DE LEGIBILIDAD")
        pdf.print_resumen(values_to_print, file_name)
        if generate_complete_report:
            pdf.print_complete_report(pdf_complete_report, sorted_formulas, number_of_pharagraphs)
        pdf.add_page()
        pdf.seccion("Anexos")
        pdf.anexos()
        pdf.output(file_route+'/'+PDF_FILE,'F')
    updateProgress.emit("Proceso finalizado." if work[0] else "Proceso cancelado.")

def clean_file(file):
    open(file, "w", encoding="utf-8").close()

#Crea todos los gráficos que se agregan al PDF de resultados
def plot_aggregate_results(paragraphsNumbers, plotData, updateProgress, work):
    bins = [0,10,20,30,40,50,60,70,80,90,100]

    if work[0]:
        plt.clf()
        plt.figure(figsize=[5.5,5], dpi=100)
        plt.hist(plotData[SIGRISZPAZOS], bins, color = "blue", ec = "black")
        plt.ylabel(LABEL_CANT_PARRAFOS)
        plt.xlabel(LABEL_VALOR_PERSPICUIDAD);
        plt.title('Resultados de '+SIGRISZPAZOS_TEXT+'/'+INFLESZ_TEXT);
        plt.savefig(DOCS_ROUTE+PLOT_SIGRISZPAZOS)
    updateProgress.emit(SIGRISZPAZOS_TEXT+" completado" if work[0] else "Cancelando...")

    if work[0]:
        plt.clf()
        plt.figure(figsize=[5.5,5], dpi=100)
        plt.hist(plotData[FERNANDEZHUERTA], bins, color = "red", ec = "black")
        plt.ylabel(LABEL_CANT_PARRAFOS)
        plt.xlabel(LABEL_VALOR_PERSPICUIDAD);
        plt.title('Resultados de '+FERNANDEZHUERTA_TEXT);
        plt.savefig(DOCS_ROUTE+PLOT_FERNANDEZHUERTA)
    updateProgress.emit(FERNANDEZHUERTA_TEXT+" completado" if work[0] else "Cancelando...")

    if work[0]:
        plt.clf()
        plt.figure(figsize=[5.5,5], dpi=100)
        plt.hist(plotData[MULEGIBILITY], bins, color = "green", ec = "black")
        plt.ylabel(LABEL_CANT_PARRAFOS)
        plt.xlabel(LABEL_VALOR_PERSPICUIDAD);
        plt.title('Resultados de '+MULEGIBILITY_TEXT);
        plt.savefig(DOCS_ROUTE+PLOT_MULEGIBILITY)
    updateProgress.emit(MULEGIBILITY_TEXT+" completado" if work[0] else "Cancelando...")

    if work[0]:
        plt.clf()
        plt.figure(figsize=[10,6], dpi=250)
        plt.xlabel(LABEL_NUM_PARRAFO)
        plt.ylabel(LABEL_VALOR_PERSPICUIDAD)
        plt.title('');
        plt.grid(True)
        plt.plot(paragraphsNumbers, plotData[SIGRISZPAZOS], color='blue', marker='.', label=(SIGRISZPAZOS_TEXT+'/'+INFLESZ_TEXT))
        plt.plot(paragraphsNumbers, plotData[FERNANDEZHUERTA], color='red', marker='.', label=FERNANDEZHUERTA_TEXT)
        plt.plot(paragraphsNumbers, plotData[MULEGIBILITY], color='green', marker='.', label=MULEGIBILITY_TEXT)
        plt.legend(bbox_to_anchor=(0,1.02,1,0.2), loc="lower left",mode="expand", borderaxespad=0, ncol=3)
        plt.ylim(ymin=0)
        plt.savefig(DOCS_ROUTE+PLOT_PARAGRAPHS)
    updateProgress.emit("Gráficos completados..." if work[0] else "Cancelando...")
    plt.clf()

#Función principal que maneja todo el flujo del programa
def process_file(process_configs, updateProgress, work):
    clean_file(OUTPUT_TEXT)
    clean_file(OUTPUT_FILE)

    file_name = process_configs['file'].split('/')[-1]
    save_route = process_configs['save_folder']

    pdf_configs = {'dpi':900, 'file_path': process_configs['file'], 'first_page': process_configs['first_page'], 'last_page': process_configs['last_page']}
    updateProgress.emit("Iniciando proceso de lectura del PDF..." if work[0] else "Cancelando...")
    create_images_from_file(pdf_configs, updateProgress, work)
    file_to_read = open(OUTPUT_TEXT, "a", encoding="utf-8")
    last_page = process_configs['last_page'] if process_configs['last_page']<number_pages else number_pages
    image_cleaner_configs = {'file_to_read': file_to_read, 'first_page': process_configs['first_page'], 'last_page': last_page}
    refine_image(image_cleaner_configs, updateProgress, work)

    delete_files(process_configs['first_page'], last_page, updateProgress, work)

    nlp = es_core_news_sm.load()

    szigriszt_values = []
    fernandez_huerta_values = []
    mu_legibility_values = []
    general_values = []

    with open(OUTPUT_FILE, "a", encoding="utf-8") as text_file:
        pharagraphs = []
        if work[0]:
            raw_file = open(OUTPUT_TEXT, "r", encoding="utf-8")
            Lines = raw_file.readlines()
            refined_text = refine_text(Lines)
            pharagraphs = refined_text.split('@')
            pharagraphs = list(filter(None, pharagraphs))

        results = []
        pdf_complete_report = []
        csv = None
        csvSeparator = ";"

        if process_configs['gen_csv']:
            if work[0]: 
                open(save_route+'/'+CSV_FILE, "w").close()
                csv = open(save_route+'/'+CSV_FILE, "a")
                if process_configs['csv_commas']:
                    csvSeparator = ","
                csv.write('Parrafo'+csvSeparator+SIGRISZPAZOS_TEXT+'/'+INFLESZ_TEXT+csvSeparator+FERNANDEZHUERTA_TEXT+csvSeparator+MULEGIBILITY_VAR_TEXT+'\n')
            updateProgress.emit("Calculando de índices de perspicuidad..." if work[0] else "Cancelando...")

        plotData = {
            SIGRISZPAZOS: [],
            FERNANDEZHUERTA: [],
            MULEGIBILITY: []
        }
        paragraphsNumbers = []

        for index, pharagraph in enumerate(pharagraphs):
            tokenized_pharagraph = nlp(pharagraph)

            letters_counter = get_letters_per_word(tokenized_pharagraph)

            word_counter = calculate_words(tokenized_pharagraph)
            phrases_counter = calculate_phrases(tokenized_pharagraph.sents)
            syllables_counter = calculate_syllables(tokenized_pharagraph)
            
            perspicuity_values = {'words': word_counter, 'phrases': phrases_counter, 'syllables':syllables_counter, 'letters': letters_counter }
            result = calculate_perspicuity(perspicuity_values)

            paragraphsNumbers.append(index+1)
            plotData[SIGRISZPAZOS].append(result[SIGRISZPAZOS])
            plotData[FERNANDEZHUERTA].append(result[FERNANDEZHUERTA])
            plotData[MULEGIBILITY].append(result[MULEGIBILITY])

            #Armando objetos para obtener las tablas de mejores y peores
            sigrizt_result = {"parrafo": str(index), "indice_perspicuidad": str(result[SIGRISZPAZOS])}
            fernandez_result = {"parrafo": str(index), "indice_perspicuidad": str(result[FERNANDEZHUERTA])} 
            mu_result = {"parrafo": str(index), "indice_perspicuidad": str(result[MULEGIBILITY])} 
            general_result = {"parrafo": str(index), "indice_perspicuidad": str((result[SIGRISZPAZOS]+result[FERNANDEZHUERTA]+result[MULEGIBILITY])/3.0)} 
            #Agregando cada objeto en arreglo de cada tipo
            szigriszt_values.append(sigrizt_result)
            fernandez_huerta_values.append(fernandez_result)
            mu_legibility_values.append(mu_result)
            general_values.append(general_result)

            #Validar si la propiedad gen_csv viene true para generar en el archivo csv los indices que necesitamos
            if process_configs['gen_csv']:
                csv.write(str(index) + csvSeparator + str(result[SIGRISZPAZOS])  + csvSeparator + str(result[FERNANDEZHUERTA])+ csvSeparator + str(result[MULEGIBILITY])+"\n")

            final_analysis = {"parrafo": pharagraph, "palabrasParrafo":word_counter, "frasesParrafo":phrases_counter, "silabasParrafo":syllables_counter, 'perspicuidad':result}

            results.append([pharagraph, final_analysis])
            pdf_complete_report.append(final_analysis)  
        plot_aggregate_results(paragraphsNumbers, plotData, updateProgress, work)

        if process_configs['gen_csv'] and work[0]:
            csv.close()
        
        #Reordenando objetos
        sorted_formulas = []
        if work[0]:
            sorted_formulas = sort_formulas_results(general_values)
            
            szigriszt_average = calculate_average_formulas(szigriszt_values)
            fernandez_huerta_average = calculate_average_formulas(fernandez_huerta_values)
            mu_average = calculate_average_formulas(mu_legibility_values)
        
        #Imprimiento valores de tabla mejores y peores 
        updateProgress.emit("Almacenando resultados..." if work[0] else "Cancelando...")
        
        if work[0]:
            for result in results:
                print(result, file=text_file)

        updateProgress.emit("Generando PDF..." if work[0] else "Cancelando...")

        values_to_print = {}
        if work[0]:
            values_to_print = {SIGRISZPAZOS: {"value": szigriszt_average, "name": SIGRISZPAZOS_TEXT}, FERNANDEZHUERTA: {"value": fernandez_huerta_average, "name": FERNANDEZHUERTA_TEXT}, "LegibilidadMu": {"value": mu_average,"name": MULEGIBILITY_VAR_TEXT}, "Inflesz": {"value": szigriszt_average, "name": INFLESZ_TEXT}}

        generatePDF(updateProgress, values_to_print, save_route, file_name, sorted_formulas, process_configs['full_report'], pdf_complete_report, len(pharagraphs), work)

#Ordena los párrafos dependiendo del índice de perspicuidad promedio obtenido
def sort_formulas_results(formulas):
    return sorted(formulas, key=lambda x: float(x["indice_perspicuidad"]), reverse=True)

#Obtiene el índice de perspicuidad promedio de todos los párrafos por cada fórmula 
def calculate_average_formulas(formula):
    counter = 0
    total_sum = 0

    for table_object in formula:
        counter += 1
        total_sum += float(table_object[SORT_FIELD])
    
    if counter == 0:
        return 0
    average = total_sum/counter
    return round(average, 2)

app_id = 'sultral.lecto.1_0_0'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)

app = QApplication(sys.argv)
app.setWindowIcon(QIcon(os.path.join(basedir,'app.ico')))

window = MainWindow(process_file)

window.show()
sys.exit(app.exec())
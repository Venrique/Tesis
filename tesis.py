from posixpath import split
import shutil
import os
import re
import pdftotext
import nltk
import spacy
from syltippy import syllabize

from PIL import Image
import pytesseract
import sys
from nltk.tag import StanfordPOSTagger
from pdf2image import convert_from_path
from nltk.tokenize import word_tokenize

import os
java_path = "tokenizer/jdk/bin/java.exe"
os.environ['JAVAHOME'] = java_path

import matplotlib
import matplotlib.pyplot as plt
import skimage.io
from skimage.color import rgb2gray
from skimage.filters import (threshold_otsu, threshold_niblack, threshold_sauvola)


#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger')
#nltk.download('conll2002')



tagger="tokenizer\\postagger\\models\\spanish-ud.tagger"
jar="tokenizer\\postagger\\stanford-postagger.jar"

# Path of the pdf
docs_route = "docs/"
PDF_file = docs_route+"Cuento.pdf"

dpi = 900
paginas = convert_from_path(PDF_file, dpi)
  
numpag = 1

for pagina in paginas:
    filename = "pagina_"+str(numpag)+".jpg"
    pagina.save(docs_route+filename, 'JPEG')
    numpag = numpag + 1
    break
  
filelimit = numpag-1
  
outfile = "out_text.txt"
  
f = open(outfile, "a", encoding="utf-8")
  
for i in range(1, filelimit + 1):
    filename = "pagina_"+str(i)+".jpg"
    original = skimage.io.imread(fname=docs_route+filename)

    image = rgb2gray(original)

    pilimage = Image.open(docs_route+filename)
    width, height = pilimage.size
    pilimage.close()

    image.shape

    matplotlib.rcParams['font.size'] = 12

    thresh_otsu = threshold_otsu(image)
    binary_otsu = image > thresh_otsu

    mult=5
    plt.figure(figsize=((int)(width/dpi)*mult, (int)(height/dpi)*mult))
    plt.imshow(binary_otsu, cmap=plt.cm.gray)
    plt.axis('off')
    plt.savefig(docs_route+'plt-'+filename, bbox_inches='tight')

    text = str(((pytesseract.image_to_string(Image.open(docs_route+'plt-'+filename),lang='spa'))))
    text = text.replace('-\n', '')
    f.write(text)

for i in range(1, filelimit + 1):
    filename = "pagina_"+str(i)+".jpg"
    os.remove(docs_route+filename)
    os.remove(docs_route+'plt-'+filename)

### PROCESAMIENTO ###
nlp = spacy.load("es_core_news_sm")
with open("Output.txt", "a") as text_file:
    raw_file = open(outfile, 'r', encoding="utf-8")
    Lines = raw_file.readlines()
    text_raw = ''
    for line in Lines:
        text_raw += line
    text_raw = re.sub(r'[0-9]+', '', text_raw)
    text_raw = re.sub(r'@', '', text_raw)
    text_raw = re.sub(r'(  +)', ' ', text_raw)
    text_clean = re.sub(r'[\r\n][\r\n]+', '@', text_raw)

    #f_clean = open('clean_'+outfile, "w", encoding="utf-8")
    #f_clean.write(text_raw)
    #f_clean.close()

    parrafos = text_clean.split('@')

    results = []

    for parrafo in parrafos:
        
        contadorP = 0
        contadorF = 0
        contadorS = 0
        
        #results.append([parrafo, {"palabrasParrafo":contadorP, "frasesParrafo":contadorF, "silabasParrafo":contadorS}])

        tokenizar = nlp(parrafo)
        #print(nlp.pipe_names)

        for word in tokenizar:
            contadorP += 1
            #print(word.text, file=text_file)

        for sent in tokenizar.sents:
            contadorF += 1
            #print(sent.text, file=text_file)

        for token in tokenizar:

            syllables, stress = syllabize(u'{}'.format(token.text))
            contadorS += len(syllables)
            #print(u'-'.join(s if stress != i else s.upper() for (i, s) in enumerate(syllables)), file=text_file)
        print([parrafo, {"palabrasParrafo":contadorP, "frasesParrafo":contadorF, "silabasParrafo":contadorS}])
        if contadorF != 0 and contadorP !=0:
            perspicuidad = 207-((62.3*contadorS)/(contadorP*1.0)) - ((contadorP*1.0)/(contadorF*1.0))
            
            results.append([parrafo, {"palabrasParrafo":contadorP, "frasesParrafo":contadorF, "silabasParrafo":contadorS, "pespicuidad":perspicuidad}])
    
    for result in results:
        print(result, file=text_file)



"""
tokens = nltk.word_tokenize(sentence, language='spanish')

etiquetador=StanfordPOSTagger(tagger,jar)
etiquetas=etiquetador.tag(tokens)
for etiqueta in etiquetas:
    res[1].append(etiqueta)
"""

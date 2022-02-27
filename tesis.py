import shutil
import os
import re
import pdftotext
import nltk

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


nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('conll2002')

tagger="tokenizer\\postagger\\models\\spanish-ud.tagger"
jar="tokenizer\\postagger\\stanford-postagger.jar"

# Path of the pdf
docs_route = "docs/"
PDF_file = docs_route+"articulo.pdf"

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
    text = re.sub(r'[0-9]+', '', text)
    text = re.sub(r'(  +)', ' ', text)
    text = re.sub(r'( +)\n\n+', '\n\n', text)
    f.write(text)

for i in range(1, filelimit + 1):
    filename = "pagina_"+str(i)+".jpg"
    os.remove(docs_route+filename)
    #os.remove(docs_route+'plt-'+filename)
  
f.close()


### TOKENIZADOR ###
sentence = "Mario es mañoso, pero kike es delgado"

tokens = nltk.word_tokenize(sentence, language='spanish')

etiquetador=StanfordPOSTagger(tagger,jar)
etiquetas=etiquetador.tag(tokens)
for etiqueta in etiquetas:
    print(etiqueta)

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
java_path = "C:/Program Files/Java/jdk1.8.0_301/bin/java.exe"
os.environ['JAVAHOME'] = java_path

import matplotlib
import matplotlib.pyplot as plt
import skimage.io
from skimage.color import rgb2gray
from skimage.filters import (threshold_otsu, threshold_niblack, threshold_sauvola)


nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('conll2002')

#with open("Bethesda-00046517.pdf", "rb") as f:
#    pdf = pdftotext.PDF(f)
#
#contador = 1
#for pagina in pdf:
#    print("pagina" + " "+str(contador))
#    print(pagina)
#    contador+=1

tagger="C:\\Users\\ragq1\\Desktop\\Tesis\\Tesis\\stanford-postagger-full-2020-11-17\\models\\spanish-ud.tagger"
jar="C:\\Users\\ragq1\\Desktop\\Tesis\\Tesis\\stanford-postagger-full-2020-11-17\\stanford-postagger.jar"



# Path of the pdf
PDF_file = "articulo.pdf"

dpi = 900
paginas = convert_from_path(PDF_file, dpi)
  
numpag = 1

for pagina in paginas:
    filename = "pagina_"+str(numpag)+".jpg"
    pagina.save(filename, 'JPEG')
    numpag = numpag + 1
    #break
  
filelimit = numpag-1
  
outfile = "out_text.txt"
  
f = open(outfile, "a", encoding="utf-8")
  
for i in range(1, filelimit + 1):
    filename = "pagina_"+str(i)+".jpg"
    original = skimage.io.imread(fname=filename)

    image = rgb2gray(original)

    pilimage = Image.open(filename)
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
    plt.savefig('plt-'+filename, bbox_inches='tight')

    text = str(((pytesseract.image_to_string(Image.open('plt-'+filename),lang='spa'))))
    text = text.replace('-\n', '')
    #text = re.sub(r'[0-9]+', '', text)
    #text = re.sub(r'\n\n*', '\n', text)
    f.write(text)

for i in range(1, filelimit + 1):
    filename = "pagina_"+str(i)+".jpg"
    os.remove(filename)
    #os.remove('plt-'+filename)
  
f.close()

training_set = [[(w.lower(),t) for w,t in s] for s in nltk.corpus.conll2002.tagged_sents('esp.train')]
unigram_tagger = nltk.UnigramTagger(training_set)
bigram_tagger = nltk.BigramTagger(training_set, backoff=unigram_tagger)

sentence = """Mario es mañoso, pero kike es delgado"""
#espaniol= word_tokenize(sentence,language='spanish')
#print(espaniol)

tokens = nltk.word_tokenize(sentence, language='spanish')
#tagged = nltk.pos_tag(tokens)
#print(tagged)

etiquetador=StanfordPOSTagger(tagger,jar)
etiquetas=etiquetador.tag(tokens)
for etiqueta in etiquetas:
    print(etiqueta)

print(bigram_tagger)
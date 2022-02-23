import shutil
import os
import pdftotext
import nltk

from PIL import Image
import pytesseract
import sys

from pdf2image import convert_from_path
from nltk.tokenize import word_tokenize

import matplotlib
import matplotlib.pyplot as plt
import skimage.io
from skimage.color import rgb2gray
from skimage.filters import (threshold_otsu, threshold_niblack, threshold_sauvola)


nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('conll2002')

# Path of the pdf
PDF_file = "articulo.pdf"

dpi = 900
paginas = convert_from_path(PDF_file, dpi)
  
numpag = 1

for pagina in paginas:
    filename = "pagina_"+str(numpag)+".jpg"
    pagina.save(filename, 'JPEG')
    numpag = numpag + 1
  
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

    plt.figure(figsize=((int)(width/dpi)*3, (int)(height/dpi)*3))
    plt.imshow(binary_otsu, cmap=plt.cm.gray)
    plt.axis('off')
    plt.savefig('plt-'+filename)

    text = str(((pytesseract.image_to_string(Image.open('plt-'+filename),lang='spa'))))
    text = text.replace('-\n', '')    
    f.write(text)

for i in range(1, filelimit + 1):
    filename = "pagina_"+str(i)+".jpg"
    os.remove(filename)
    #os.remove('plt-'+filename)
  
f.close()

training_set = [[(w.lower(),t) for w,t in s] for s in nltk.corpus.conll2002.tagged_sents('esp.train')]
unigram_tagger = nltk.UnigramTagger(training_set)
bigram_tagger = nltk.BigramTagger(training_set, backoff=unigram_tagger)

sentence = """Mañana voy ir a comer pizza bien rápido. Pero luego ire a comer """
espaniol= word_tokenize(sentence,"spanish")
print(espaniol)
tokens = nltk.word_tokenize(sentence, 'spanish')
print(tokens)

print(bigram_tagger)
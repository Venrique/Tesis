import shutil
import os
import pdftotext
import nltk

from PIL import Image
import pytesseract
import sys

from pdf2image import convert_from_path
from nltk.tokenize import word_tokenize

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


# Path of the pdf
PDF_file = "articulo.pdf"
  
paginas = convert_from_path(PDF_file, 500)
  
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
    text = str(((pytesseract.image_to_string(Image.open(filename),lang='spa'))))
    text = text.replace('-\n', '')    
    f.write(text)

for i in range(1, filelimit + 1):
    filename = "pagina_"+str(i)+".jpg"
    os.remove(filename)
  
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
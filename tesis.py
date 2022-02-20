import shutil
import os
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
    text = str(((pytesseract.image_to_string(Image.open(filename)))))
    text = text.replace('-\n', '')    
    f.write(text)

for i in range(1, filelimit + 1):
    filename = "pagina_"+str(i)+".jpg"
    os.remove(filename)
  
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
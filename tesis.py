import shutil
import os
import random
import pdftotext
import nltk
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('conll2002')

with open("Bethesda-00046517.pdf", "rb") as f:
    pdf = pdftotext.PDF(f)

contador = 1
for page in pdf:
    print("pagina" + " "+str(contador))
    print(page)
    contador+=1

training_set = [[(w.lower(),t) for w,t in s] for s in nltk.corpus.conll2002.tagged_sents('esp.train')]
unigram_tagger = nltk.UnigramTagger(training_set)
bigram_tagger = nltk.BigramTagger(training_set, backoff=unigram_tagger)

sentence = """Mañana voy ir a comer pizza bien rápido. Pero luego ire a comer """
espaniol= word_tokenize(sentence,"spanish")
print(espaniol)
tokens = nltk.word_tokenize(sentence, 'spanish')
print(tokens)

print(bigram_tagger)
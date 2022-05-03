import statistics

class Perspicuity:
    def __init__(self, values):
        self.words = values['words']
        self.phrases = values['phrases']
        self.syllables = values['syllables']
        self.letters = values['letters']

    def calculate(self):
        return 0

class SzigrisztPazos(Perspicuity):
    def calculate(self):
        has_words = self.words > 0
        has_phrases = self.phrases > 0
        #is_hundred_words = self.words == 100
    
        #if(is_hundred_words):
        #    return  (206.835 - (0.623*self.syllables) - self.words)

        if(not(has_words) or not(has_phrases)):
            return 0
        calc = (207 - (62.3*((self.syllables*1.0)/(self.words*1.0))) - ((self.words*1.0)/(self.phrases*1.0)))

        if calc>100.0:
            calc = 100.0
        return calc

'''     
class SzigrisztPazosShort(Perspicuity):
    def calculate(self):
        is_hundred_words = self.words == 100
        return  (206.835 - (0.623*self.syllables) - self.words) if (is_hundred_words) else 0
'''

class FernandezHuerta(Perspicuity):
        
    def calculate(self):
        has_words = self.words > 0
        has_phrases = self.phrases > 0
        if (not(has_words) or not(has_phrases)):
            return 0

        P, F = self.__calculateFernandezHuertaValues()

        calc = (206.84 - (60*P) - (1.02*F))
        if calc>100.0:
            calc=100.0
        return calc
    
    def __calculateFernandezHuertaValues(self):
        P = (self.syllables*1.0)/(self.words*1.0)
        F = (self.words*1.0)/(self.phrases*1.0)
        return P, F

class MuLegibility(Perspicuity):
    def calculate(self):
        try:
            mean = statistics.mean(self.letters)
            variance = statistics.variance(self.letters)
            calc = ((self.words) / ((self.words) - 1.0)) * (mean / variance) * 100
            if calc>100:
                calc=100.0
            return calc
        except:
            return 0
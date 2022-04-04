import statistics

class Perspicuity:
    def __init__(self, values):
        self.words = values['words']
        self.phrases = values['phrases']
        self.syllables = values['syllables']
        self.letters = values['letters']

    def calculate(self):
        return None

class SzigrisztPazosLong(Perspicuity):
    def calculate(self):
        has_words = self.words > 0
        has_phrases = self.phrases > 0
        is_short_text = self.words <= 100
        
        print(self.syllables, self.phrases)

        if(not(has_words) or not(has_phrases) or is_short_text):
            return None

        return (207 - (62.3*((self.syllables*1.0)/(self.words*1.0))) - ((self.words*1.0)/(self.phrases*1.0)))
        
class SzigrisztPazosShort(Perspicuity):
    def calculate(self):
        is_short_text = self.words <= 100
        return  (206.835 - (0.623*self.syllables) - self.words) if (is_short_text) else None

class FernandezHuerta(Perspicuity):

    
        
    def calculate(self):
        P, F = self.__calculateFernandezHuertaValues()
        has_words = self.words > 0
        has_phrases = self.phrases > 0
        if (not(has_words) or not(has_phrases)):
            return None

        return  (206.84 - (60*P) - (1.02*F))
    
    def __calculateFernandezHuertaValues(self):
        P = (self.syllables*1.0)/(self.words*1.0)
        F = (self.words*1.0)/(self.phrases*1.0)
        return P, F

class MuLegibility(Perspicuity):
    def calculate(self):
        try:
            mean = statistics.mean(self.letters)
            variance = statistics.variance(self.letters)
            print(self.words,mean,variance)
            return ((self.words) / ((self.words) - 1.0)) * (mean / variance) * 100
        except:
            return None


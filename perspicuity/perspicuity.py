
class Perspicuity:
    def __init__(self, values):
        self.words = values['words']
        self.phrases = values['phrases']
        self.syllables = values['syllables']

    def calculate(self):
        pass

class SzigrisztPazosLong(Perspicuity):
    def calculate(self):
        result = (207 - ( (62.3*self.syllables)/(self.words*1.0) ) - ( (self.words*1.0)/(self.phrases*1.0) ))
        has_words = self.words > 0
        has_phrases = self.phrases > 0
        return  result if (has_words and has_phrases ) else None

class SzigrisztPazosShort(Perspicuity):
    def calculate(self):
        result = (207 - (0.623*self.syllables) - self.words)
        is_short_text = self.words <= 100
        return  result if (is_short_text) else None



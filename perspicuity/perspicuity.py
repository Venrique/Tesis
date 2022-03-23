
class Perspicuity:
    def __init__(self, values):
        self.words = values['words']
        self.phrases = values['phrases']
        self.syllables = values['syllables']

    def calculate(self):
        return None

class SzigrisztPazosLong(Perspicuity):
    def calculate(self):
        has_words = self.words > 0
        has_phrases = self.phrases > 0
        is_short_text = self.words <= 100
        if(has_words and has_phrases and not(is_short_text)):
            return (206.835 - ( (62.3*self.syllables)/(self.words*1.0) ) - ( (self.words*1.0)/(self.phrases*1.0) ))
        else:
            return None

class SzigrisztPazosShort(Perspicuity):
    def calculate(self):
        is_short_text = self.words <= 100
        return  (206.835 - (0.623*self.syllables) - self.words) if (is_short_text) else None



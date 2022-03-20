
class Perspicuity:
    def __init__(self, values):
        self.words = values['words']
        self.phrases = values['phrases']
        self.syllables = values['syllables']

    def calculate(self):
        pass

class SzigrisztPazosLong(Perspicuity):
    def calculate(self):
        return 207 - ( (62.3*self.syllables)/(self.words*1.0) ) - ( (self.words*1.0)/(self.phrases*1.0) )

class SzigrisztPazosShort(Perspicuity):
    def calculate(self):
        return 207 - (0.623*self.syllables) - self.words if self.words <= 100 else None



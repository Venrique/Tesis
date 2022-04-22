from fpdf import FPDF
from constants import *
from datetime import date
pdf_w=210
pdf_h=297

class PDF(FPDF):
    def titles(self, text):
        self.set_xy(0.0,0.0)
        self.set_font('Arial', 'B', 16)
        self.cell(w=210.0, h=30.0, align='C', txt=text, border=0)

    
    def encabezado(self, archivo):
        self.set_font('Times', 'B', 12)
        
        self.set_xy(10.0,30.0)
        self.cell(1, 0, 'Texto analizado: %s' % (archivo), 0, 1, 'L', 1)

        self.set_font('Times', '', 12)

        self.cell(0, 0, 'Fecha: %s' % (date.today().strftime("%d/%m/%Y")), 0, 1, 'R', 1)

    def seccion(self, title):
        self.set_font('Times', 'B', 12)
        self.set_fill_color(200, 220, 255)
        # Title
        self.cell(0, 6, '%s' % (title), 0, 1, 'L', 1)
        # Line break
        self.ln(4)

    def get_ValorTablaSzigrizs(self,result):
        if 0 <= result <= 15:
            self.set_fill_color(248,105,107)
            return "Muy Difícil"
        elif 16 <= result <= 35:
            self.set_fill_color(250,148,115)
            return "Árido"
        elif 36 <= result <= 50:
            self.set_fill_color(252,191,123)
            return "Bastante Difícil"
        elif 51 <= result <= 65:
            self.set_fill_color(255,235,132)
            return "Normal"
        elif 66 <= result <= 75:
            self.set_fill_color(204,221,130)
            return "Bastante Fácil"
        elif 76 <= result <= 85:
            self.set_fill_color(152,206,127)
            return "Fácil"
        elif 86 <= result <= 100:
            self.set_fill_color(99,190,123)
            return "Muy Fácil"
    
    def get_ValorTablaFernandez(self,result):
        if 0 <= result <= 30:
            self.set_fill_color(248,105,107)
            return "Muy Difícil"
        elif 31 <= result <= 50:
            self.set_fill_color(250,148,115)
            return "Difícil"
        elif 50 <= result <= 60:
            self.set_fill_color(252,191,123)
            return "Algo Difícil"
        elif 61 <= result <= 70:
            self.set_fill_color(255,235,132)
            return "Normal (para adulto)"
        elif 71 <= result <= 80:
            self.set_fill_color(204,221,130)
            return "Algo Fácil"
        elif 81 <= result <= 90:
            self.set_fill_color(152,206,127)
            return "Fácil"
        elif 91 <= result <= 100:
            self.set_fill_color(99,190,123)
            return "Muy Fácil"

    def get_ValorTablaMu(self,result):
        if 0 <= result <= 30:
            self.set_fill_color(248,105,107)
            return "Muy Difícil"
        elif 31 <= result <= 50:
            self.set_fill_color(250,148,115)
            return "Difícil"
        elif 50 <= result <= 60:
            self.set_fill_color(252,191,123)
            return "Un Poco Difícil"
        elif 61 <= result <= 70:
            self.set_fill_color(255,235,132)
            return "Adecuado"
        elif 71 <= result <= 80:
            self.set_fill_color(204,221,130)
            return "Un Poco Fácil"
        elif 81 <= result <= 90:
            self.set_fill_color(152,206,127)
            return "Fácil"
        elif 91 <= result <= 100:
            self.set_fill_color(99,190,123)
            return "Muy Fácil"
    
    def get_ValorTabla(self,formula,result):

        if formula == "SzigrisztPazos":
            return self.get_ValorTablaSzigrizs(result)
        elif formula == "FernandezHuerta":
            return self.get_ValorTablaFernandez(result)
        elif formula == "Legibilidad Mu":
            return self.get_ValorTablaMu(result)


    def print_formulas(self, result):
        
        contador_altura = 50.0

        for formula in result:
            self.set_xy(20.0,contador_altura)
            self.cell(0, 6, '> %s: ' % (formula))
            self.set_x(65.0)
            self.cell(0, 6, str(result[formula]))
            self.set_x(100.0)
            self.set_font('Times', 'B', 12)
            self.cell(0, 6, self.get_ValorTabla(formula,result[formula]), 0, 1, 'L', 1)
            self.set_font('Times', '', 12)
            contador_altura += 8.0
        
        self.set_xy(10.0,contador_altura + 4.0)

    def resultados(self,result):

        self.set_font('Times', '', 12)
        self.print_formulas(result)


    def resultados_generales(self,result):
        self.set_xy(10.0,38.0)
        self.seccion("1. Resultados")
        self.resultados(result)
        self.seccion("2. Detalles")
        self.seccion("3. Conclusión")

    
    def print_resumen(self,result):
        self.encabezado('¿Qué tan seguros son los elevadores?')
        self.resultados_generales(result)


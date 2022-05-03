from fpdf import FPDF
from constants import *
from datetime import date
pdf_w=210
pdf_h=297

class PDF(FPDF):

    pdf_y=0

    def aumentarValorY(self, aumento):
        self.pdf_y += aumento
        return self.pdf_y

    def titles(self, text):
        self.set_xy(0.0,self.pdf_y)
        self.set_font('Arial', 'B', 16)
        self.cell(w=210.0, h=30.0, align='C', txt=text, border=0)

    
    def encabezado(self, archivo):
        self.set_font('Times', 'B', 12)
        self.set_xy(10.0,self.aumentarValorY(30.0))
        self.cell(1, 0, 'Texto analizado: %s' % (archivo), 0, 1, 'L', 1)

        self.set_font('Times', '', 12)

        self.cell(0, 0, 'Fecha: %s' % (date.today().strftime("%d/%m/%Y")), 0, 1, 'R', 1)

    def seccion(self, title):
        self.set_font('Times', 'B', 12)
        self.set_fill_color(200, 220, 255)
        # Title
        self.cell(0, 6, '%s' % (title), 0, 1, 'L', 1)

    def get_ValorTablaSzigrizs(self,result):
        if 0 <= result < 15:
            self.set_fill_color(248,105,107)
            return "Muy Difícil"
        elif 15 <= result < 35:
            self.set_fill_color(250,148,115)
            return "Árido"
        elif 35 <= result < 50:
            self.set_fill_color(252,191,123)
            return "Bastante Difícil"
        elif 50 <= result < 65:
            self.set_fill_color(255,235,132)
            return "Normal"
        elif 65 <= result < 75:
            self.set_fill_color(204,221,130)
            return "Bastante Fácil"
        elif 75 <= result < 85:
            self.set_fill_color(152,206,127)
            return "Fácil"
        elif 85 <= result < 100:
            self.set_fill_color(99,190,123)
            return "Muy Fácil"
    
    def get_ValorTablaFernandez(self,result):
        if 0 <= result < 30:
            self.set_fill_color(248,105,107)
            return "Muy Difícil"
        elif 30 <= result < 50:
            self.set_fill_color(250,148,115)
            return "Difícil"
        elif 50 <= result < 60:
            self.set_fill_color(252,191,123)
            return "Algo Difícil"
        elif 60 <= result < 70:
            self.set_fill_color(255,235,132)
            return "Normal (para adulto)"
        elif 70 <= result < 80:
            self.set_fill_color(204,221,130)
            return "Algo Fácil"
        elif 80 <= result < 90:
            self.set_fill_color(152,206,127)
            return "Fácil"
        elif 90 <= result <= 100:
            self.set_fill_color(99,190,123)
            return "Muy Fácil"

    def get_ValorTablaMu(self,result):
        if 0 <= result < 30:
            self.set_fill_color(248,105,107)
            return "Muy Difícil"
        elif 30 <= result < 50:
            self.set_fill_color(250,148,115)
            return "Difícil"
        elif 50 <= result < 60:
            self.set_fill_color(252,191,123)
            return "Un Poco Difícil"
        elif 60 <= result < 70:
            self.set_fill_color(255,235,132)
            return "Adecuado"
        elif 70 <= result < 80:
            self.set_fill_color(204,221,130)
            return "Un Poco Fácil"
        elif 80 <= result < 90:
            self.set_fill_color(152,206,127)
            return "Fácil"
        elif 90 <= result <= 100:
            self.set_fill_color(99,190,123)
            return "Muy Fácil"
        
    def get_ValorTablaInflesz(self,result):
        if 0 <= result < 40:
            self.set_fill_color(248,105,107)
            return "Muy Difícil"
        elif 40 <= result < 55:
            self.set_fill_color(252,191,123)
            return "Algo Difícil"
        elif 55 <= result < 65:
            self.set_fill_color(255,235,132)
            return "Normal"
        elif 65 <= result < 80:
            self.set_fill_color(204,221,130)
            return "Bastante Fácil"
        elif 80 <= result <= 100:
            self.set_fill_color(99,190,123)
            return "Muy Fácil"
    
    def get_ValorTabla(self,formula,result):
        if formula == "SzigrisztPazos":
            return self.get_ValorTablaSzigrizs(result)
        elif formula == "FernandezHuerta":
            return self.get_ValorTablaFernandez(result)
        elif formula == "LegibilidadMu":
            return self.get_ValorTablaMu(result)
        elif formula == "Inflesz":
            return self.get_ValorTablaInflesz(result)


    def print_formulas(self, result):
        
        self.set_y(self.aumentarValorY(12.0))

        self.set_xy(20.0,self.pdf_y)
        self.set_font('Times', 'B', 12)
        self.cell(0, 6, "Fórmulas")
        self.set_x(65.0)
        self.cell(0, 6, "Resultados")
        self.set_x(100.0)
        self.cell(0, 6, "Interpretaciones")
        self.set_font('Times', '', 12)
        self.set_y(self.aumentarValorY(8.0))

        for formula in result:
            self.set_xy(20.0,self.pdf_y)
            self.cell(0, 6, '> %s: ' % (result[formula]["name"]))
            self.set_x(65.0)
            self.cell(0, 6, str(result[formula]["value"]))
            self.set_x(100.0)
            self.set_font('Times', 'B', 12)
            self.cell(0, 6, self.get_ValorTabla(formula,result[formula]["value"]), 0, 1, 'L', 1)
            self.set_font('Times', '', 12)
            self.set_y(self.aumentarValorY(8.0))
            print(formula, result[formula])
        
        self.set_xy(10.0,self.aumentarValorY(4.0))

    def resultados(self, result):
        self.set_font('Times', '', 12)
        self.print_formulas(result)

    def graficos(self):
        self.set_y(self.aumentarValorY(8.0))
        self.image(DOCS_ROUTE + 'plot-SzigrisztPazos-hist.png',10, self.pdf_y, 90)
        self.image(DOCS_ROUTE + 'plot-FernandezHuerta-hist.png',110, self.pdf_y, 90)
        self.set_y(self.aumentarValorY(90.0))
        self.image(DOCS_ROUTE + 'plot-MuLegibility-hist.png',55, self.pdf_y, 100)
        self.set_y(self.aumentarValorY(90.0))
        self.add_page("L")
        self.pdf_y = 0
        self.set_xy(10,self.aumentarValorY(20.0))
        self.image(DOCS_ROUTE + 'plot-resByParagraph.png',10, self.pdf_y, 300)


    def resultados_generales(self,result):
        self.set_xy(10.0,self.aumentarValorY(8.0))
        self.seccion("1. Resultados")
        self.resultados(result)
        self.seccion("2. Estadísticas")
        self.graficos()
        #self.seccion("3. Conclusión")

    
    def print_resumen(self,result,titulo):
        self.encabezado(titulo)
        self.resultados_generales(result)


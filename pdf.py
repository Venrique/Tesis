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
        self.cell(0, 0, 'Texto analizado: %s' % (archivo), 0, 1, 'L', 1)

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
            return "Difícil"
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
        if formula == SIGRISZPAZOS:
            return self.get_ValorTablaSzigrizs(result)
        elif formula == FERNANDEZHUERTA:
            return self.get_ValorTablaFernandez(result)
        elif formula == MULEGIBILITY:
            return self.get_ValorTablaMu(result)
        elif formula == INFLESZ:
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
        self.image(DOCS_ROUTE + PLOT_SIGRISZPAZOS,10, self.pdf_y, 90)
        self.image(DOCS_ROUTE + PLOT_FERNANDEZHUERTA,110, self.pdf_y, 90)
        self.set_y(self.aumentarValorY(90.0))
        self.image(DOCS_ROUTE + PLOT_MULEGIBILITY,55, self.pdf_y, 100)
        self.set_y(self.aumentarValorY(90.0))
        self.add_page("L")
        self.pdf_y = 0
        self.set_xy(10,self.aumentarValorY(20.0))
        self.image(DOCS_ROUTE + PLOT_PARAGRAPHS,10, self.pdf_y, 300)

    def anexos(self):

        sigrisz = (
            ("Nivel", "Dificultad", "Contenido"),
            ("0 - 14", "Muy Difícil", "Científico / Filosófico"),
            ("15 - 34", "Difícil", "Pedagógico / Especializado"),
            ("35 - 49", "Bastante Difícil", "Literatura / Divulgación"),
            ("50 - 64", "Normal", "Informativo"),
            ("65 - 74", "Bastante Fácil", "Novela / Revista"),
            ("75 - 84", "Fácil", "Kioskos"),
            ("85 - 100", "Muy Fácil", "Cuentos / Relatos")
        )

        huerta = (
            ("Nivel", "Dificultad", "Grado de Lectura"),
            ("0 - 29", "Muy Difícil", "Graduado de Universidad"),
            ("30 - 49", "Difícil", "Universitario"),
            ("50 - 59", "Algo Difícil", "Bachillerato"),
            ("60 - 69", "Normal", "Grados 8 a 9"),
            ("70 - 79", "Algo Fácil", "Grado 7"),
            ("80 - 89", "Fácil", "Grado 6"),
            ("90 - 100", "Muy Fácil", "Grado 5")
        )

        mu = (
            ("Nivel", "Dificultad"),
            ("0 - 29", "Muy Difícil"),
            ("30 - 49", "Difícil"),
            ("50 - 59", "Algo Difícil"),
            ("60 - 69", "Normal"),
            ("70 - 79", "Algo Fácil"),
            ("80 - 89", "Fácil"),
            ("90 - 100", "Muy Fácil")
        )

        inflez = (
            ("Nivel", "Dificultad"),
            ("0 - 39", "Muy Difícil"),
            ("40 - 54", "Algo Difícil"),
            ("55 - 64", "Normal"),
            ("65 - 79", "Bastante Fácil"),
            ("80 - 100", "Muy Fácil")
        )

        self.set_y(self.aumentarValorY(5.0))
        line_height = self.font_size * 2.5
        col_width = self.epw / 3  # distribute content evenly
        self.set_fill_color(255, 255, 255)
        self.cell(0, 0, '%s' % ('Escala Sigrisz Pazos '), 0, 1, 'L', 1)
        self.set_y(self.aumentarValorY(5.0))
        for row in sigrisz:
            for datum in row:
                self.multi_cell(col_width, line_height, datum, border=1,
                        new_x="RIGHT", new_y="TOP", max_line_height=self.font_size)
            self.ln(line_height)

        self.set_y(self.aumentarValorY(100.0))
        for row in huerta:
            for datum in row:
                self.multi_cell(col_width, line_height, datum, border=1,
                        new_x="RIGHT", new_y="TOP", max_line_height=self.font_size)
            self.ln(line_height)

        self.add_page()
        col_width = self.epw / 2  # distribute content evenly
        for row in mu:
            for datum in row:
                self.multi_cell(col_width, line_height, datum, border=1,
                        new_x="RIGHT", new_y="TOP", max_line_height=self.font_size)
            self.ln(line_height)

        self.set_y(self.aumentarValorY(50.0))
        for row in inflez:
            for datum in row:
                self.multi_cell(col_width, line_height, datum, border=1,
                        new_x="RIGHT", new_y="TOP", max_line_height=self.font_size)
            self.ln(line_height)        


    def resultados_generales(self,result):
        self.set_xy(10.0,self.aumentarValorY(8.0))
        self.seccion("1. Resultados")
        self.resultados(result)
        self.seccion("2. Estadísticas")
        self.graficos()
        self.add_page()
        self.seccion("3. Anexos")
        self.anexos()
        #self.seccion("3. Conclusión")

    
    def print_resumen(self,result,titulo):
        self.encabezado(titulo)
        self.resultados_generales(result)


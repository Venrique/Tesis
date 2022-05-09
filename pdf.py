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

    def marca(self):
        self.image('Logo-watermark.png',30, 73.5, 150)

    def titles(self, text):
        self.set_xy(0.0,self.pdf_y)
        self.set_font('Arial', 'B', 16)
        self.cell(w=210.0, h=30.0, align='C', txt=text, border=0)

    
    def encabezado(self, archivo):
        self.set_font('Times', 'B', 12)
        self.set_xy(10.0,self.aumentarValorY(30.0))
        self.cell(0, 0, 'Texto analizado: %s' % (archivo), 0, 1, 'L', 0)

        self.set_font('Times', '', 12)

        self.cell(0, 0, 'Fecha: %s' % (date.today().strftime("%d/%m/%Y")), 0, 1, 'R', 0)

    def seccion(self, title):
        self.set_font('Times', 'B', 12)
        self.set_fill_color(200, 220, 255)
        # Title
        self.cell(0, 6, '%s' % (title), 0, 1, 'L', 1)
        self.set_font('Times', '', 12)

    def get_ValorTablaSzigrizs(self,result):
        if 0 <= result < 15:
            self.set_fill_color(248,105,107)
            return "Lectura Muy Difícil"
        elif 15 <= result < 35:
            self.set_fill_color(250,148,115)
            return "Lectura Difícil"
        elif 35 <= result < 50:
            self.set_fill_color(252,191,123)
            return "Lectura Bastante Difícil"
        elif 50 <= result < 65:
            self.set_fill_color(255,235,132)
            return "Lectura Normal"
        elif 65 <= result < 75:
            self.set_fill_color(204,221,130)
            return "Lectura Bastante Fácil"
        elif 75 <= result < 85:
            self.set_fill_color(152,206,127)
            return "Lectura Fácil"
        elif 85 <= result < 100:
            self.set_fill_color(99,190,123)
            return "Lectura Muy Fácil"
    
    def get_ValorTablaFernandez(self,result):
        if 0 <= result < 30:
            self.set_fill_color(248,105,107)
            return "Lectura Muy Difícil"
        elif 30 <= result < 50:
            self.set_fill_color(250,148,115)
            return "Lectura Difícil"
        elif 50 <= result < 60:
            self.set_fill_color(252,191,123)
            return "Lectura Algo Difícil"
        elif 60 <= result < 70:
            self.set_fill_color(255,235,132)
            return "Lectura Normal (para adulto)"
        elif 70 <= result < 80:
            self.set_fill_color(204,221,130)
            return "Lectura Algo Fácil"
        elif 80 <= result < 90:
            self.set_fill_color(152,206,127)
            return "Lectura Fácil"
        elif 90 <= result <= 100:
            self.set_fill_color(99,190,123)
            return "Lectura Muy Fácil"

    def get_ValorTablaMu(self,result):
        if 0 <= result < 30:
            self.set_fill_color(248,105,107)
            return "Lectura Muy Difícil"
        elif 30 <= result < 50:
            self.set_fill_color(250,148,115)
            return "Lectura Difícil"
        elif 50 <= result < 60:
            self.set_fill_color(252,191,123)
            return "Lectura Un Poco Difícil"
        elif 60 <= result < 70:
            self.set_fill_color(255,235,132)
            return "Lectura Adecuado"
        elif 70 <= result < 80:
            self.set_fill_color(204,221,130)
            return "Lectura Un Poco Fácil"
        elif 80 <= result < 90:
            self.set_fill_color(152,206,127)
            return "Lectura Fácil"
        elif 90 <= result <= 100:
            self.set_fill_color(99,190,123)
            return "Lectura Muy Fácil"
        
    def get_ValorTablaInflesz(self,result):
        if 0 <= result < 40:
            self.set_fill_color(248,105,107)
            return "Lectura Muy Difícil"
        elif 40 <= result < 55:
            self.set_fill_color(252,191,123)
            return "Lectura Algo Difícil"
        elif 55 <= result < 65:
            self.set_fill_color(255,235,132)
            return "Lectura Normal"
        elif 65 <= result < 80:
            self.set_fill_color(204,221,130)
            return "Lectura Bastante Fácil"
        elif 80 <= result <= 100:
            self.set_fill_color(99,190,123)
            return "Lectura Muy Fácil"
    
    def get_ValorTabla(self,formula,result):
        if formula == SIGRISZPAZOS:
            return self.get_ValorTablaSzigrizs(result)
        elif formula == FERNANDEZHUERTA:
            return self.get_ValorTablaFernandez(result)
        elif formula == MULEGIBILITY:
            return self.get_ValorTablaMu(result)
        elif formula == INFLESZ:
            return self.get_ValorTablaInflesz(result)

    def get_ValorTablaGeneral(self,result):
        if 0 <= result < 15:
            return {"textos":"textos de contenido científico o filosófico, que tienen una naturaleza muy profunda", "publico_recomendado": "son las personas con grado universitario o a punto de culminar su educación superior."}
        elif 15 <= result < 35:
            return {"textos":"textos de contenido pedagógico o especializado, que tienen una naturaleza aburrida o complicada", "publico_recomendado": "son las personas cursando un grado universitario."}
        elif 35 <= result < 50:
            return {"textos":"textos literarios (como narrativa, poesía, teatro o ensayos) o de divulgación (textos informativos más especializados como artículos de descubrimientos o de nuevas tecnologías), que tienen una naturaleza sugestiva o contenido importante", "publico_recomendado": "son las personas cursando o que hayan culminado su educación media (bachillerato)."}
        elif 50 <= result < 65:
            return {"textos":"textos de tipo informativo (como diccionarios, enciclopedias, periódicos, reportajes, revistas, entre otros), que tratan temas de la actualidad y son de contenido claro", "publico_recomendado": "es el público en general."}
        elif 65 <= result < 75:
            return {"textos":"textos como novelas populares, revistas femeninas y textos educativos; que suelen ser interesantes o dirigidos al entretenimiento", "publico_recomendado": "son las personas mayores de 12 años."}
        elif 75 <= result < 85:
            return {"textos":"textos que pueden encontrarse en quioscos como revistas e historietas, cuyo contenido es considerablemente simple", "publico_recomendado": "son las personas mayores de 10 años."}
        elif 85 <= result < 100:
            return {"textos":"textos como cuentos, relatos o tebeos (historietas cortas dirigidas a niños, también llamados viñetas), cuya naturaleza es superficial o coloquial", "publico_recomendado": "son los niños entre 6 y 10 años."}

    def get_conclusion_general(self, result):
        avg_result = (result[SIGRISZPAZOS]['value']+result[FERNANDEZHUERTA]['value']+result[MULEGIBILITY]['value'])/3
        resultados = self.get_ValorTablaGeneral(avg_result)
        conclusion = CONCLUSION_GRAL_INICIO+resultados['textos']+CONCLUSION_GRAL_PUBLICO_RECOMENDADO+resultados['publico_recomendado']
        self.set_y(self.aumentarValorY(155.0))
        self.set_font('Times', 'B', 12)
        self.cell(0, 6, "Conclusión: ")
        self.set_font('Times', '', 12)
        self.set_y(self.aumentarValorY(6.5))
        self.multi_cell(0, self.font_size * 1.25, conclusion)


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
        self.set_xy(10,self.aumentarValorY(10.0))
        self.image(DOCS_ROUTE + PLOT_PARAGRAPHS,23.5, self.pdf_y, 250)

    def anexos(self):
        self.pdf_y = 0
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

        aux = True

        self.set_y(self.aumentarValorY(25.0))
        line_height = self.font_size * 1.3
        col_width = self.epw / 3  # distribute content evenly
        self.set_fill_color(255, 255, 255)
        self.cell(0, 0, '%s' % ('Escala Sigrisz Pazos '), 0, 1, 'L', 1)
        self.set_y(self.aumentarValorY(5.0))
        for row in sigrisz:
            if aux:
                self.set_font('Times', 'B', 12)
                aux = False
            else:
                self.set_font('Times', '', 12)
            for datum in row:
                self.multi_cell(col_width, line_height, datum, border=1,
                        new_x="RIGHT", new_y="TOP", max_line_height=self.font_size)
            self.ln(line_height)

        aux = True
        self.set_y(self.aumentarValorY(55.0))
        self.cell(0, 0, '%s' % ('Escala Fernandez Huerta '), 0, 1, 'L', 1)
        self.set_y(self.aumentarValorY(5.0))
        for row in huerta:
            if aux:
                self.set_font('Times', 'B', 12)
                aux = False
            else:
                self.set_font('Times', '', 12)
            for datum in row:
                self.multi_cell(col_width, line_height, datum, border=1,
                        new_x="RIGHT", new_y="TOP", max_line_height=self.font_size)
            self.ln(line_height)

        aux = True
        self.set_y(self.aumentarValorY(55.0))
        self.cell(0, 0, '%s' % ('Escala Mu '), 0, 1, 'L', 1)
        self.set_y(self.aumentarValorY(5.0))
        col_width = self.epw / 2  # distribute content evenly
        for row in mu:
            if aux:
                self.set_font('Times', 'B', 12)
                aux = False
            else:
                self.set_font('Times', '', 12)
            for datum in row:
                self.multi_cell(col_width, line_height, datum, border=1,
                        new_x="RIGHT", new_y="TOP", max_line_height=self.font_size)
            self.ln(line_height)

        aux = True
        self.set_y(self.aumentarValorY(55.0))
        self.cell(0, 0, '%s' % ('Escala Inflesz '), 0, 1, 'L', 1)
        self.set_y(self.aumentarValorY(5.0))
        for row in inflez:
            if aux:
                self.set_font('Times', 'B', 12)
                aux = False
            else:
                self.set_font('Times', '', 12)
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
        self.get_conclusion_general(result)
        self.add_page()
        self.seccion("Anexos")
        self.anexos()
        #self.seccion("3. Conclusión")

    
    def print_resumen(self,result,titulo):
        self.marca()
        self.encabezado(titulo)
        self.resultados_generales(result)


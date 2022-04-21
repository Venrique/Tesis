from fpdf import FPDF
from constants import *
pdf_w=210
pdf_h=297

class PDF(FPDF):
    def lines(self):
        self.set_line_width(0.0)
        self.line(5.0,5.0,205.0,5.0) # top one
        self.line(5.0,292.0,205.0,292.0) # bottom one
        self.line(5.0,5.0,5.0,292.0) # left one
        self.line(205.0,5.0,205.0,292.0) # right one

    def titles(self, text):
        self.set_xy(0.0,0.0)
        self.set_font('Arial', 'B', 16)
        self.cell(w=210.0, h=30.0, align='C', txt=text, border=0)

    def resumen(self):
        # Leer archivo de texto
        
       
        self.set_xy(10.0,80.0)
        # Times 12
        self.set_font('Times', '', 12)
        # Emitir texto justificado
        f = open(OUTPUT_FILE, "r", encoding='utf8')
        print(".........................Texto completo ...........................")
        print(f)
        for x in f:
            print(".........................Texto...........................")
            print(x)
            self.multi_cell(0,5, txt = x, align='C')
            
        # Salto de línea
        self.ln()
        # Mención en italic -cursiva-
        self.set_font('', 'I')
        self.cell(0, 5, '(end of excerpt)')


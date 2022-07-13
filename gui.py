from PyQt6.QtWidgets import (
    QMainWindow,
    QFileDialog,
    QApplication,
    QCheckBox,
    QLabel,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSpinBox,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QMessageBox,
    QButtonGroup)

import time
    
from pathlib import Path
from PyQt6.QtGui import QFont
import PyPDF2
from PyQt6.QtCore import (Qt, QRunnable, pyqtSlot, QThreadPool, pyqtSignal, QObject)


#Clase que contiene todas las rutinas de la interfaz gráfica
class MainWindow(QMainWindow):

    #Constructor de la clase inicializando variables
    def __init__(self, process):
        super().__init__()

        self.initUI()
        self.process = process
        self.threadpool = QThreadPool()
        self.currentProgress = 0
        self.progressIncrease = 0
        self.working = [True]


    #Construcción de la interfaz de usuario.
    def initUI(self):
        self.currentProgress = 0
        self.programSettings = {"file": "", "save_folder": "", "full_report": True, "gen_csv": False, "csv_commas": False, "first_page": 1, "last_page": 999, "page_total": 999}
        mainLayout = QVBoxLayout()
        fileSelectLayout = QHBoxLayout()
        folderSelectLayout = QHBoxLayout()
        reportOptionsLayout = QHBoxLayout()
        csvOptionsLayout = QHBoxLayout()
        limitsLayout = QHBoxLayout()
        mainLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        widget = QWidget()

        lblFileSelect = QLabel("Seleccionar un archivo")
        lblFileSelect.setFont(QFont('Calibri', 14))
        lblFileSelect.setStyleSheet("font-weight: bold; margin-bottom: 0.5em")
        mainLayout.addWidget(lblFileSelect)

        self.btnSelectFile = QPushButton("Buscar archivos...")
        self.btnSelectFile.clicked.connect(self.showDialog)
        self.btnSelectFile.setFont(QFont('Calibri', 12))
        self.btnSelectFile.setStyleSheet("padding: 0.2em")
        fileSelectLayout.addWidget(self.btnSelectFile)
        self.lblFileName = QLabel("Ningún archivo seleccionado.")
        self.lblFileName.setFont(QFont('Calibri', 12))
        fileSelectLayout.addWidget(self.lblFileName)
        mainLayout.addLayout(fileSelectLayout)

        lblFolderSelect = QLabel("Guardado de resultados")
        lblFolderSelect.setFont(QFont('Calibri', 14))
        lblFolderSelect.setStyleSheet("font-weight: bold; margin-bottom: 0.5em")
        mainLayout.addWidget(lblFolderSelect)

        self.btnSelectFolder = QPushButton("Seleccionar carpeta...")
        self.btnSelectFolder.clicked.connect(self.showDialogFolder)
        self.btnSelectFolder.setFont(QFont('Calibri', 12))
        self.btnSelectFolder.setStyleSheet("padding: 0.2em")
        self.btnSelectFolder.setDisabled(True)
        folderSelectLayout.addWidget(self.btnSelectFolder)
        self.lblFolderName = QLabel("Ninguna carpeta seleccionada.")
        self.lblFolderName.setFont(QFont('Calibri', 12))
        folderSelectLayout.addWidget(self.lblFolderName)
        mainLayout.addLayout(folderSelectLayout)

        lblReportType = QLabel("Tipo de reporte")
        lblReportType.setFont(QFont('Calibri', 12))
        reportOptionsLayout.addWidget(lblReportType)

        reportTypeGroup = QButtonGroup(widget)
        self.rbCompleteReport = QRadioButton("Reporte completo")
        self.rbCompleteReport.setFont(QFont('Calibri', 12))
        self.rbCompleteReport.setChecked(True)
        self.rbCompleteReport.fullReport = True
        self.rbCompleteReport.toggled.connect(self.radioHandler)
        reportOptionsLayout.addWidget(self.rbCompleteReport)
        reportTypeGroup.addButton(self.rbCompleteReport)

        self.rbPartialReport = QRadioButton("Reporte resumido")
        self.rbPartialReport.setFont(QFont('Calibri', 12))
        self.rbPartialReport.fullReport = False
        self.rbPartialReport.toggled.connect(self.radioHandler)
        reportOptionsLayout.addWidget(self.rbPartialReport)
        mainLayout.addLayout(reportOptionsLayout)
        reportTypeGroup.addButton(self.rbPartialReport)

        self.ckbCsv = QCheckBox("Generar archivo .csv con los resultados")
        self.ckbCsv.setFont(QFont('Calibri', 12))
        self.ckbCsv.toggled.connect(self.csvHandler)
        mainLayout.addWidget(self.ckbCsv)

        '''self.ckbUseCommas = QCheckBox("Separar con coma (,) en lugar de punto y coma (;)")
        self.ckbUseCommas.setFont(QFont('Calibri', 12))
        self.ckbUseCommas.toggled.connect(self.checkBoxUseCommas)
        self.ckbUseCommas.setDisabled(True)
        self.ckbUseCommas.setStyleSheet("margin-left: 1em")'''

        separatorGroup = QButtonGroup(widget)
        self.rbSemicolon = QRadioButton("Separar con punto y coma (;)")
        self.rbSemicolon.setFont(QFont('Calibri', 12))
        self.rbSemicolon.setChecked(True)
        self.rbSemicolon.setDisabled(True)
        self.rbSemicolon.useCommas = False
        self.rbSemicolon.toggled.connect(self.radioSeparatorHandler)
        self.rbSemicolon.setStyleSheet("margin-left: 1em")
        csvOptionsLayout.addWidget(self.rbSemicolon)
        separatorGroup.addButton(self.rbSemicolon)

        self.rbCommas = QRadioButton("Separar con coma (,)")
        self.rbCommas.setFont(QFont('Calibri', 12))
        self.rbCommas.setDisabled(True)
        self.rbCommas.useCommas = True
        self.rbCommas.toggled.connect(self.radioSeparatorHandler)
        csvOptionsLayout.addWidget(self.rbCommas)
        mainLayout.addLayout(csvOptionsLayout)
        separatorGroup.addButton(self.rbCommas)

        lblOptions = QLabel("Opciones de procesado")
        lblOptions.setFont(QFont('Calibri', 14))
        lblOptions.setStyleSheet("font-weight: bold; margin-bottom: 0.5em; margin-top: 0.5em")
        mainLayout.addWidget(lblOptions)

        self.ckbUseLimits = QCheckBox("Analizar solo una parte del documento")
        self.ckbUseLimits.setFont(QFont('Calibri', 12))
        self.ckbUseLimits.toggled.connect(self.checkBoxHandler)
        self.ckbUseLimits.setDisabled(True)
        mainLayout.addWidget(self.ckbUseLimits)

        lblRange1 = QLabel("Desde la página")
        lblRange1.setFont(QFont('Calibri', 12))

        self.txtPaginaInicio = QSpinBox()
        self.txtPaginaInicio.setFont(QFont('Calibri', 12))
        self.txtPaginaInicio.setValue(1)
        self.txtPaginaInicio.setMinimum(1)
        self.txtPaginaInicio.valueChanged.connect(self.minimumHandler)
        self.txtPaginaInicio.setDisabled(True)

        lblRange2 = QLabel("hasta la página")
        lblRange2.setFont(QFont('Calibri', 12))
        lblRange2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.txtPaginaFin = QSpinBox()
        self.txtPaginaFin.setFont(QFont('Calibri', 12))
        self.txtPaginaFin.setMinimum(1)
        self.txtPaginaFin.setDisabled(True)

        limitsLayout.addWidget(lblRange1)
        limitsLayout.addWidget(self.txtPaginaInicio)
        limitsLayout.addWidget(lblRange2)
        limitsLayout.addWidget(self.txtPaginaFin)

        mainLayout.addLayout(limitsLayout)

        lblSpacer = QLabel()
        mainLayout.addWidget(lblSpacer)

        self.btnRunProgram = QPushButton("Analizar documento")
        self.btnRunProgram.setFont(QFont('Calibri', 12))
        self.btnRunProgram.setStyleSheet("padding: 0.2em")
        self.btnRunProgram.clicked.connect(self.runProgram)
        self.btnRunProgram.setDisabled(True)
        mainLayout.addWidget(self.btnRunProgram)

        self.progressBar = QProgressBar()
        self.progressBar.setValue(0)

        mainLayout.addWidget(self.progressBar)

        self.lblStatusMsg = QLabel("Esperando a tu señal...")
        self.lblStatusMsg.setFont(QFont('Calibri', 12))
        mainLayout.addWidget(self.lblStatusMsg)

        widget.setLayout(mainLayout)

        self.setCentralWidget(widget)

        self.setFixedSize(mainLayout.sizeHint())
        self.setWindowTitle('Lecto: Analizador de Legibilidad')
        self.setFixedWidth(500)
        self.show()

    #Función para seleccionar el documento PDF a analizar.
    def showDialog(self):
        home_dir = str(Path.home())
        fname = QFileDialog.getOpenFileName(self, 'Seleccionar PDF', home_dir, "PDF (*.pdf)")

        if fname[0]:
            self.btnSelectFolder.setDisabled(False)
            self.lblFileName.setText(fname[0])
            self.programSettings['file'] = fname[0]
            file = open(fname[0], 'rb')
            readpdf = PyPDF2.PdfFileReader(file)
            totalpages = readpdf.numPages
            self.txtPaginaInicio.setMaximum(totalpages)
            self.txtPaginaFin.setMaximum(totalpages)
            self.txtPaginaFin.setValue(totalpages)
            self.programSettings['last_page'] = totalpages
            self.programSettings['page_total'] = totalpages
            self.ckbUseLimits.setDisabled(False)

            folder = fname[0].split('/')
            folder.pop()
            folder = '/'.join(folder)
            self.lblFolderName.setText(folder)
            self.programSettings['save_folder'] = folder
            self.btnRunProgram.setDisabled(False)
    
    #Función para seleccionar el directorio donde se guardarán los resultados.
    def showDialogFolder(self):
        fname = QFileDialog.getExistingDirectory(self, 'Seleccionar Carpeta')

        if fname:
            self.lblFolderName.setText(fname)
            self.programSettings['save_folder'] = fname
            #self.btnRunProgram.setDisabled(False)
    
    #Función para deshabilitar todos los campos del formulario.
    def disableForm(self):
        self.btnSelectFile.setDisabled(True)
        self.btnSelectFolder.setDisabled(True)
        self.rbCompleteReport.setDisabled(True)
        self.rbPartialReport.setDisabled(True)
        self.ckbCsv.setDisabled(True)
        #self.ckbUseCommas.setDisabled(True)
        self.rbSemicolon.setDisabled(True)
        self.rbCommas.setDisabled(True)
        self.ckbUseLimits.setDisabled(True)
        self.txtPaginaFin.setDisabled(True)
        self.txtPaginaInicio.setDisabled(True)

    #Función que inicializa el proceso de análisis del documento y crea una instancia del hilo secundario.
    def runProgram(self):
        self.working[0] = True
        self.disableForm()
        self.currentProgress = 0
        self.progressIncrease = 0
        self.programSettings['first_page'] = self.txtPaginaInicio.value() if self.ckbUseLimits.isChecked() else 1
        self.programSettings['last_page'] = self.txtPaginaFin.value() if self.ckbUseLimits.isChecked() else self.programSettings['page_total']
        page_range = self.programSettings['last_page'] - self.programSettings['first_page']
        number_of_steps = (page_range + 1)*2 + 10 + len(range(self.programSettings['first_page'], self.programSettings['last_page']+1, 10))
        if self.programSettings['gen_csv']:
            number_of_steps += 1
        self.progressIncrease = 100/number_of_steps

        self.btnRunProgram.setDisabled(True)
        self.worker = Worker(self.process, self.programSettings, self.working)
        self.worker.signals.progress.connect(self.updateProgressBar)
        self.threadpool.start(self.worker)
    
    #Controlador de los radio buttons de generar reporte completo/resumido
    def radioHandler(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            self.programSettings['full_report'] = radioButton.fullReport

    #Controlador de la checkbox para definir un rango de páginas.
    def checkBoxHandler(self):
        checkBox = self.sender()
        if checkBox.isChecked():
            self.txtPaginaInicio.setDisabled(False)
            self.txtPaginaFin.setDisabled(False)
        else:
            self.txtPaginaInicio.setDisabled(True)
            self.txtPaginaFin.setDisabled(True)

    #Controlador de la checkbox para generar CSV de los resultados.
    def csvHandler(self):
        checkBox = self.sender()
        self.programSettings['gen_csv'] = checkBox.isChecked()
        #self.ckbUseCommas.setDisabled(not(checkBox.isChecked()))
        self.rbSemicolon.setDisabled(not(checkBox.isChecked()))
        self.rbCommas.setDisabled(not(checkBox.isChecked()))

    #Controlador de los radio buttons para utilizar comas en el CSV.
    def radioSeparatorHandler(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            self.programSettings['csv_commas'] = radioButton.useCommas

    #Controlador de la checkbox utilizar comas en el CSV.
    '''def checkBoxUseCommas(self):
        checkBox = self.sender()
        self.programSettings['csv_commas'] = checkBox.isChecked()'''

    #Función para evitra que la página final sea menor que la página inicial.
    def minimumHandler(self):
        self.txtPaginaFin.setMinimum(self.txtPaginaInicio.value())

    #Función para reiniciar el formulario y las configuraciones del análisis.
    def resetForm(self):
        self.btnRunProgram.setText("Analizar documento")
        self.programSettings = {"file": "", "save_folder": "", "full_report": True, "gen_csv": False, "csv_commas": False, "first_page": 1, "last_page": 999, "page_total": 999}
        self.lblFileName.setText("Ningún archivo seleccionado.")
        self.lblFolderName.setText("Ninguna carpeta seleccionada.")
        self.txtPaginaInicio.setValue(1)
        self.txtPaginaFin.setValue(1)
        self.progressBar.setValue(0)
        self.btnSelectFile.setDisabled(False)
        self.rbCompleteReport.setDisabled(False)
        self.rbCompleteReport.setChecked(True)
        self.rbPartialReport.setDisabled(False)
        self.ckbCsv.setChecked(False)
        self.ckbCsv.setDisabled(False)
        #self.ckbUseCommas.setChecked(False)
        self.rbSemicolon.setChecked(True)
        self.ckbUseLimits.setDisabled(True)
        self.ckbUseLimits.setChecked(False)
        try: self.worker.signals.progress.disconnect()
        except Exception: pass
    
    #Función para actualizar la barra de progreso y notificar cuando se haya completado.
    def updateProgressBar(self,message):
        self.lblStatusMsg.setText(message)
        progressiveIncrease = self.progressIncrease
        while progressiveIncrease > 0.5:
            self.currentProgress += 0.5
            self.progressBar.setValue(self.currentProgress)
            time.sleep(0.01)
            progressiveIncrease -= 0.5
        self.currentProgress += progressiveIncrease
        self.progressBar.setValue(self.currentProgress)

        if round(self.currentProgress,1) == 100.0:
            self.resetForm()
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Hecho")

            text = ""
            if self.working[0]:
                text = "El proceso se ha completado"
            else:
                text = "Se ha cancelado la operación"

            self.working[0] = True
            msgBox.setText(text)
            msgBox.exec()
    
    #Función que controla el evento de cerrar la ventana.
    #Su acción es cancelar un análisis si hay uno en curso o cerrar la ventana si no hay un análisis en curso.
    def closeEvent(self, event):
        if self.currentProgress == 0 or round(self.currentProgress,1) == 100.0:
            event.accept()
        elif self.working[0]:

            close = QMessageBox.question(self, "Cancelar", "¿Cancelar el proceso actual?",QMessageBox.StandardButton.Yes| QMessageBox.StandardButton.No)
            if close == QMessageBox.StandardButton.Yes and round(self.currentProgress,1) < 100.0:
                self.working[0] = False
                self.btnRunProgram.setText("Cancelando proceso (esto puede tardar un poco)...")
                
            event.ignore()
        else:
            event.ignore()

#Clase que permite la comunicación entre los hilos.
class WorkerSignals(QObject):
    progress = pyqtSignal(str)

#Clase con la que se genera una instancia del hilo secundario.
class Worker(QRunnable):
    signals = WorkerSignals()

    #Constructor del hilo secundario.
    def __init__(self, fn, args, work):
        super(Worker, self).__init__()
        self.fn = fn
        self.args = args
        self.work = work

    #Ejecución de una función en el hilo secundario (la función main del proceso de análisis).
    @pyqtSlot()
    def run(self):
        self.fn(self.args, self.signals.progress, self.work)
    
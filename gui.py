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
    QMessageBox)

import time
    
from pathlib import Path
from PyQt6.QtGui import QFont
import PyPDF2
from PyQt6.QtCore import (Qt, QRunnable, pyqtSlot, QThreadPool, pyqtSignal, QObject)


class MainWindow(QMainWindow):
    def __init__(self, process):
        super().__init__()

        self.initUI()
        self.process = process
        self.threadpool = QThreadPool()
        self.currentProgress = 0
        self.progressIncrease = 0


    def initUI(self):
        self.currentProgress = 0
        self.programSettings = {"file": "", "save_folder": "", "full_report": True, "gen_csv": False, "csv_commas": False, "first_page": 1, "last_page": 999, "page_total": 999}
        mainLayout = QVBoxLayout()
        fileSelectLayout = QHBoxLayout()
        folderSelectLayout = QHBoxLayout()
        reportOptionsLayout = QHBoxLayout()
        limitsLayout = QHBoxLayout()
        mainLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        lblFileSelect = QLabel("Seleccionar un archivo")
        lblFileSelect.setFont(QFont('Calibri', 14))
        lblFileSelect.setStyleSheet("font-weight: bold; margin-bottom: 0.5em")
        mainLayout.addWidget(lblFileSelect)

        btnSelectFile = QPushButton("Buscar archivos...")
        btnSelectFile.clicked.connect(self.showDialog)
        btnSelectFile.setFont(QFont('Calibri', 12))
        btnSelectFile.setStyleSheet("padding: 0.2em")
        fileSelectLayout.addWidget(btnSelectFile)
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

        self.rbCompleteReport = QRadioButton("Reporte completo")
        self.rbCompleteReport.setFont(QFont('Calibri', 12))
        self.rbCompleteReport.setChecked(True)
        self.rbCompleteReport.fullReport = True
        self.rbCompleteReport.toggled.connect(self.radioHandler)
        reportOptionsLayout.addWidget(self.rbCompleteReport)

        rbPartialReport = QRadioButton("Reporte resumido")
        rbPartialReport.setFont(QFont('Calibri', 12))
        rbPartialReport.fullReport = False
        rbPartialReport.toggled.connect(self.radioHandler)
        reportOptionsLayout.addWidget(rbPartialReport)
        mainLayout.addLayout(reportOptionsLayout)

        self.ckbCsv = QCheckBox("Generar archivo .csv con los resultados")
        self.ckbCsv.setFont(QFont('Calibri', 12))
        self.ckbCsv.toggled.connect(self.csvHandler)
        mainLayout.addWidget(self.ckbCsv)

        self.ckbUseCommas = QCheckBox("Separar con coma (,) en lugar de punto y coma (;)")
        self.ckbUseCommas.setFont(QFont('Calibri', 12))
        self.ckbUseCommas.toggled.connect(self.checkBoxUseCommas)
        self.ckbUseCommas.setDisabled(True)
        self.ckbUseCommas.setStyleSheet("margin-left: 1em")
        mainLayout.addWidget(self.ckbUseCommas)

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

        widget = QWidget()
        widget.setLayout(mainLayout)

        self.setCentralWidget(widget)

        self.setFixedSize(mainLayout.sizeHint())
        self.setWindowTitle('Lecto: Analizador de Legibilidad')
        self.setFixedWidth(500)
        self.show()

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
    
    def showDialogFolder(self):
        fname = QFileDialog.getExistingDirectory(self, 'Seleccionar Carpeta')

        if fname:
            self.lblFolderName.setText(fname)
            self.programSettings['save_folder'] = fname
            #self.btnRunProgram.setDisabled(False)

    def runProgram(self):
        self.currentProgress = 0
        self.progressIncrease = 0
        self.programSettings['first_page'] = self.txtPaginaInicio.value() if self.ckbUseLimits.isChecked() else 1
        self.programSettings['last_page'] = self.txtPaginaFin.value() if self.ckbUseLimits.isChecked() else self.programSettings['page_total']
        
        number_of_steps = (self.programSettings['last_page'] - self.programSettings['first_page'] + 1)*2 + 9
        if self.programSettings['gen_csv']:
            number_of_steps += 1
        self.progressIncrease = 100/number_of_steps

        #print(str(self.programSettings),self.currentProgress,self.progressIncrease)

        self.btnRunProgram.setDisabled(True)
        self.worker = Worker(self.process, self.programSettings)
        self.worker.signals.progress.connect(self.updateProgressBar)
        self.threadpool.start(self.worker)
    
    def radioHandler(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            self.programSettings['full_report'] = radioButton.fullReport

    def checkBoxHandler(self):
        checkBox = self.sender()
        if checkBox.isChecked():
            self.txtPaginaInicio.setDisabled(False)
            self.txtPaginaFin.setDisabled(False)
        else:
            self.txtPaginaInicio.setDisabled(True)
            self.txtPaginaFin.setDisabled(True)

    def csvHandler(self):
        checkBox = self.sender()
        self.programSettings['gen_csv'] = checkBox.isChecked()
        self.ckbUseCommas.setDisabled(not(checkBox.isChecked()))

    def checkBoxUseCommas(self):
        checkBox = self.sender()
        self.programSettings['csv_commas'] = checkBox.isChecked()

    def minimumHandler(self):
        self.txtPaginaFin.setMinimum(self.txtPaginaInicio.value())

    def resetForm(self):
        self.programSettings = {"file": "", "save_folder": "", "full_report": True, "gen_csv": False, "csv_commas": False, "first_page": 1, "last_page": 999, "page_total": 999}
        self.lblFileName.setText("Ningún archivo seleccionado.")
        self.lblFolderName.setText("Ninguna carpeta seleccionada.")
        self.txtPaginaFin.setValue(1)
        self.txtPaginaInicio.setValue(1)
        self.progressBar.setValue(0)
        self.ckbUseLimits.setDisabled(True)
        self.ckbUseLimits.setChecked(False)
        self.ckbUseCommas.setDisabled(True)
        self.ckbUseCommas.setChecked(False)
        self.ckbCsv.setChecked(False)
        self.rbCompleteReport.setChecked(True)
        try: self.worker.signals.progress.disconnect()
        except Exception: pass
    
    def updateProgressBar(self):
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
            msgBox.setText("El proceso se ha completado")
            msgBox.exec()

### Thread Classes

class WorkerSignals(QObject):
    progress = pyqtSignal()

class Worker(QRunnable):
    signals = WorkerSignals()

    def __init__(self, fn, args):
        super(Worker, self).__init__()
        # https://stackoverflow.com/questions/59309979/pyqt-updating-progress-bar-using-thread
        self.fn = fn
        self.args = args

    @pyqtSlot()
    def run(self):
        self.fn(self.args, self.signals.progress)
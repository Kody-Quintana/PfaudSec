import sys

from PyQt5 import QtGui, QtCore, uic, QtWidgets
import ui_redirect
def p(x):
    print(x)

class MainWindow(QtWidgets.QMainWindow,ui_redirect.Ui_MainWindow):#, UI.MainUI.Ui_MainWindow):
    def __init__(self):
        
        QtWidgets.QWidget.__init__(self)


        self.setupUi(self)
        self.actionAbout_PfaudSec.triggered.connect(self.about_PfaudSec)
        self.actionxelatex_config.setVisible(False)
        self.checkBox.stateChanged.connect(self.output_same_dir)
        self.checkBox.setChecked(True)
        
        #Loose files ui stuff
        for i in range(3):
            num = str(i)
            exec("self.pushButton_loose_"+ num + """.setEnabled(False)
self.lineEdit_loose_""" + num + """.setEnabled(False)
self.checkBox_loose_""" + num + '.stateChanged.connect(lambda: self.loose_func(' + num + """))
self.pushButton_loose_""" + num + '.clicked.connect(lambda: self.loose_sel(' + num + '))',
locals(),locals())

        self.lineEdit_loose_name_2.setEnabled(False)

        self.setWindowState(QtCore.Qt.WindowMaximized)       
        self.grab_display.setFocusPolicy(QtCore.Qt.NoFocus)
        self.checkBox.setFocusPolicy(QtCore.Qt.NoFocus)
        self.output_display.setFocusPolicy(QtCore.Qt.NoFocus)

        # This var is to see which LaTeX QProcess is running
        # out of the three required to update the table of contents
        self.proc_num = 0

        self.set_fonts()
        
        #Allow copy/paste on job info line edits
        for i in range(4):
            num = str(i + 1)
            exec('self.job_entry_' + num + """.setDragEnabled(True)
self.job_entry_""" + num + '.setReadOnly(False)',locals(),locals())

        #This is dumb and should be put into some kind of loop
        #First LaTeX run
        self.process_0 = QtCore.QProcess(self)
        self.process_0.setProcessChannelMode(QtCore.QProcess.MergedChannels)
        self.process_0.readyRead.connect(self.stdout_and_err_Ready)
        self.process_0.started.connect(lambda: self.clear())
        self.process_0.started.connect(lambda: p('LaTeX first compile start'))
        self.process_0.finished.connect(lambda: self.proc_num_set(1))

        #Second LaTeX run
        self.process_1 = QtCore.QProcess(self)
        self.process_1.setProcessChannelMode(QtCore.QProcess.MergedChannels)
        self.process_1.readyRead.connect(self.stdout_and_err_Ready)
        self.process_1.started.connect(lambda: p('LaTeX second compile start'))
        self.process_1.finished.connect(lambda: self.proc_num_set(2))

        #Third LaTeX run (to update table of contents)
        self.process_2 = QtCore.QProcess(self)
        self.process_2.setProcessChannelMode(QtCore.QProcess.MergedChannels)
        self.process_2.readyRead.connect(self.stdout_and_err_Ready)
        self.process_2.started.connect(lambda: p('LaTeX third compile start'))
        self.process_2.finished.connect(lambda: self.proc_num_set(0))


    def set_fonts(self):
        #Font imports
        try:
            font_instance = QtGui.QFontDatabase
            PfFont = font_instance.addApplicationFont("TeX/font/OTF/Pfaudler-Book.otf")
            pf_font_family = font_instance.applicationFontFamilies(PfFont)[0]
            pf_font = QtGui.QFont(pf_font_family)

            PfFontBold = font_instance.addApplicationFont("TeX/font/OTF/Pfaudler-Bold.otf")
            pf_font_family_bold = font_instance.applicationFontFamilies(PfFontBold)[0]
            pf_font_bold_large = QtGui.QFont(pf_font_family_bold,50)
            pf_font_bold_large.setWeight(QtGui.QFont.Bold)
            pf_font_bold = QtGui.QFont(pf_font_family_bold)

            self.setFont(pf_font_bold)
            self.outputbox.setFont(pf_font)
            self.outputbox_2.setFont(pf_font)
            self.label.setFont(pf_font_bold_large)
        except IndexError:
            pass
    def about_PfaudSec(self):
        about_box = QtWidgets.QMessageBox()
        about_box.setTextFormat(QtCore.Qt.RichText)
        def link_text(url, display):
            return str('<a href="http://www.' + url + '" style="color: rgb(255,255,255)">' + display + '</a>')

        about_box.setInformativeText(
                'PfaudSec is a '
                + link_text('python.org','Python')
                + '/'
                + link_text('qt.io','Qt5')
                + ' (via '
                + link_text('riverbankcomputing.com/software/pyqt/intro','PyQt5')
                + ') interface for '
                + link_text('sharelatex.com/learn/XeLaTeX','XeLaTeX')
                + ' and '
                + link_text('ghostscript.com','Ghostscript')
                + ' to create PDFs for internal use at '
                + link_text('pfaudler.com/en','Pfaudler.')
                + '<br><br>'
                + 'Source code is available on '
                + link_text('github.com/kody-quintana/PfaudSec','GitHub'))

        font = QtGui.QFont()
        font.setPointSize(14)
        about_box.setFont(font)
        about_box.exec_()

    def loose_func(self, input):
        num = str(input)
        exec('if self.checkBox_loose_' + num + """.isChecked():
    self.pushButton_loose_""" + num + """.setEnabled(True)
    self.lineEdit_loose_""" + num + """.setEnabled(True)
else:
    self.pushButton_loose_""" + num + """.setEnabled(False)
    self.lineEdit_loose_""" + num + '.setEnabled(False)', locals(), locals())
        if self.checkBox_loose_2.isChecked():
            self.lineEdit_loose_name_2.setEnabled(True)
        else:
            self.lineEdit_loose_name_2.setEnabled(False)

    def loose_sel(self, input):
        box_label = {0 : 'Select Brazil Data Book Folder',
                1 : 'Select Second Brazil Data Book Folder',
                2 : 'Select Misc PDF Files Folder'}

        file = str(QtWidgets.QFileDialog.getExistingDirectory(\
                self, box_label.get(input)))
        if file:
            num = str(input)
            exec('self.lineEdit_loose_' + num + '.setText(file)', locals(), locals())
    
    def output_same_dir(self):
        if self.checkBox.isChecked():
            self.output_sel.setEnabled(False)
            self.output_display.setText(self.grab_display.toPlainText())
        else:
            self.output_sel.setEnabled(True)

    def proc_num_set(self, num):
        self.proc_num = num

    def clear(self):
        self.outputbox.clear()


    #xelatex path is passed from the data_book class
        #that is passed to this method
    #work_dir is global
    def compile_tex(self, xelatex_path, work_dir):
        self.process_0.setWorkingDirectory(work_dir)
        self.process_0.start(xelatex_path, ['databook'])

    def compile_tex1(self,xelatex_path, work_dir):
        self.process_1.setWorkingDirectory(work_dir)
        self.process_1.start(xelatex_path, ['databook'])

    def compile_tex2(self,xelatex_path, work_dir):
        self.process_2.setWorkingDirectory(work_dir)
        self.process_2.start(xelatex_path, ['databook'])

    
    # For printing to outputbox_2 (right side)
    # (for general output, see pronk function in main.py)
    def main_append(self, text):
        cursor = self.outputbox_2.textCursor()
        cursor.movePosition(cursor.End)
        cursor.insertText(text)
        cursor.movePosition(cursor.End)
        self.outputbox_2.verticalScrollBar().setSliderPosition\
                (self.outputbox_2.verticalScrollBar().maximum())
    

    # For printing to outputbox (left side) 
    # (for LaTeX output only)
    def append(self, text):
        cursor = self.outputbox.textCursor()
        cursor.movePosition(cursor.End)
        cursor.insertText(text)
        cursor.movePosition(cursor.End)
        self.outputbox.verticalScrollBar().setSliderPosition\
                (self.outputbox.verticalScrollBar().maximum())


    def stdout_and_err_Ready(self):
        text = ''
        ldict = locals()
        exec('text = bytearray(self.process_' + str(self.proc_num)\
                + '.readAll())',ldict)
        text = ldict['text']
        text = text.decode("UTF-8")
        self.append(text)

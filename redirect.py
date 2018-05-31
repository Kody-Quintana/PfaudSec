import sys
from PyQt4 import QtGui, QtCore, uic

def p(x):
    print(x)

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        
        QtGui.QWidget.__init__(self)
        uic.loadUi('redirect.ui', self)
        
        self.setWindowState(QtCore.Qt.WindowMaximized)       
        self.outputbox.setFocusPolicy(QtCore.Qt.NoFocus)
        self.outputbox_2.setFocusPolicy(QtCore.Qt.NoFocus)
        #self.grab_sel.setFocusPolicy(QtCore.Qt.NoFocus)
        #self.output_sel.setFocusPolicy(QtCore.Qt.NoFocus)
        self.grab_display.setFocusPolicy(QtCore.Qt.NoFocus)
        self.output_display.setFocusPolicy(QtCore.Qt.NoFocus)
        self.latex_render.setFocusPolicy(QtCore.Qt.NoFocus)
        #self.job_entry_1.clearFocus()
        # This var is to see which LaTeX QProcess is running
        # out of the two required to update the table of contents
        self.proc_num = 0


        #Font imports
        font_instance = QtGui.QFontDatabase
        PfFont = font_instance.addApplicationFont("TeX/font/TTF/Pfaudler-Book.ttf")
        pf_font_family = font_instance.applicationFontFamilies(PfFont)[0]
        pf_font = QtGui.QFont(pf_font_family)

        PfFontBold = font_instance.addApplicationFont("TeX/font/TTF/Pfaudler-Bold.ttf")
        pf_font_family_bold = font_instance.applicationFontFamilies(PfFontBold)[0]
        pf_font_bold_large = QtGui.QFont(pf_font_family_bold,50)
        pf_font_bold = QtGui.QFont(pf_font_family_bold)

        #self.setFont(pf_font_bold)
        self.outputbox.setFont(pf_font)
        self.outputbox_2.setFont(pf_font)
        self.label.setFont(pf_font_bold_large)


        #Allow copy/paste on job info line edits
        self.job_entry_1.setDragEnabled(True)
        self.job_entry_1.setReadOnly(False)
        self.job_entry_2.setDragEnabled(True)
        self.job_entry_2.setDragEnabled(True)
        self.job_entry_3.setDragEnabled(True)
        self.job_entry_3.setReadOnly(False)
        self.job_entry_4.setReadOnly(False)
        self.job_entry_4.setReadOnly(False)

        
        #First LaTeX run
        self.process_0 = QtCore.QProcess(self)
        self.process_0.readyReadStandardOutput.connect(self.stdoutReady)
        self.process_0.readyReadStandardError.connect(self.stderrReady)
        self.process_0.started.connect(lambda: self.clear())
        self.process_0.started.connect(lambda: p('LaTeX first compile start'))
        self.process_0.finished.connect(lambda: self.proc_num_increase())


        #Second LaTeX run (to update table of contents)
        self.process_1 = QtCore.QProcess(self)
        self.process_1.readyReadStandardOutput.connect(self.stdoutReady)
        self.process_1.readyReadStandardError.connect(self.stderrReady)
        self.process_1.started.connect(lambda: p('LaTeX second compile start'))
        self.process_1.finished.connect(lambda: self.proc_num_reset())
    

    def proc_num_increase(self):
        self.proc_num = 1


    def proc_num_reset(self):
        self.proc_num = 0


    def clear(self):
        self.outputbox.clear()


    #xelatex path is passed from the data_book class
        #that is passed to this method
    #work_dir is global
    def compile_tex(self, xelatex_path, work_dir):
        self.process_0.setWorkingDirectory(work_dir)
        self.process_0.start(xelatex_path, ['databook'])


    def compile_tex2(self,xelatex_path, work_dir):
        self.process_1.setWorkingDirectory(work_dir)
        self.process_1.start(xelatex_path, ['databook'])

    
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


    def stdoutReady(self):
        text = ''
        ldict = locals()
        exec('text = bytearray(self.process_' + str(self.proc_num)\
                + '.readAllStandardOutput())',ldict)
        text = ldict['text']
        text = text.decode("UTF-8")
        self.append(text)


    def stderrReady(self):
        text = ''
        ldict = locals()
        exec('text = bytearray(self.process_' + str(self.proc_num)\
                + '.readAllStandardError())',ldict)
        text = ldict['text']
        text = text.decode("UTF-8")
        self.append(text)

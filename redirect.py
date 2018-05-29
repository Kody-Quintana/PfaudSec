
import sys
from PyQt4 import QtGui, QtCore, uic

def p(x):
    print(x)

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        uic.loadUi('redirect.ui', self)

        print('Connecting process')
        self.process = QtCore.QProcess(self)
        self.process.readyReadStandardOutput.connect(self.stdoutReady)
        self.process.readyReadStandardError.connect(self.stderrReady)
        self.process.started.connect(lambda: p('Started!'))
        self.process.finished.connect(lambda: self.compile_tex2('xelatex','./work'))
        print('Starting process')

        self.process2 = QtCore.QProcess(self)
        self.process2.readyReadStandardOutput.connect(self.stdoutReady2)
        self.process2.readyReadStandardError.connect(self.stderrReady2)
        self.process2.started.connect(lambda: p('Started!'))

    def compile_tex(self, xelatex_path, work_dir):
        self.process.setWorkingDirectory(work_dir)
        self.process.start(xelatex_path, ['databook'])

    def compile_tex2(self,xelatex_path, work_dir):
        self.process2.setWorkingDirectory(work_dir)
        self.process2.start(xelatex_path, ['databook'])
    
    def main_append(self, text):
        cursor = self.outputbox_2.textCursor()
        cursor.movePosition(cursor.End)
        cursor.insertText(text)

    def append(self, text):
        cursor = self.outputbox.textCursor()
        cursor.movePosition(cursor.End)
        self.outputbox.append(str(text).replace('b\'',''))
        #self.output.ensureCursorVisible()


    def stdoutReady(self):
        text = str(self.process.readAllStandardOutput())
        self.append(text)

    def stderrReady(self):
        text = str(self.process.readAllStandardError())
        self.append(text)

    def stdoutReady2(self):
        text = str(self.process2.readAllStandardOutput())
        self.append(text)

    def stderrReady2(self):
        text = str(self.process2.readAllStandardError())
        self.append(text)



def main():
    app = QtGui.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()

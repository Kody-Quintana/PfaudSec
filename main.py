import sys
import subprocess
from PyQt4 import QtCore, QtGui, uic
import tempfile
import os
import shutil
import configparser
import PfaudUI




class MyWindow(QtGui.QDialog):
    def __init__(self):
        super(MyWindow, self).__init__()

        self.ui = Ui_MyWindow()
        self.ui.setupUi(self)

        # go on setting up your handlers like:
        # self.ui.okButton.clicked.connect(function_name)
        # etc...


class DataBook(object):

    def __init__(self):
        self.embed_list = []
        self.nested_list_sections = []
        
        self.config_file = 'sections_config.ini'
        self.xelatex_path = 'xelatex'
        #self.xelatex_path = input('Enter path to xelatex: ')
        #work_dir = './work'
        self.output_dir = './output'
        self.grab_dir = './tempemb'
        self.template_dir = './TeX'
        self.data_book_run()
    
    #change to contextlib later
    
    def resource_path(self,relative_path):
        #Get absolute path to resource, works for dev and for PyInstaller
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
    
        return os.path.join(base_path, relative_path)

    def data_book_run(self):

        with tempfile.TemporaryDirectory() as self.work_dir:
        
            self.config = configparser.ConfigParser()
            self.config.read(self.config_file)
            print('\nLoaded sections from ' + str(self.config_file) + ':')
            for i in self.config.sections():
                print('Section: ' + str(i))
            print('\n')
            
            
            def get_file_list(self,ext,dir):
                self.list = []
                for i in os.listdir(dir):
                    if i.endswith(ext):
                        self.list.append(i)
                return self.list
            
            def pdf_rename(self):
                self.nested_list_sections
                self.embed_list
            
                for l in range(len(self.config.sections())): 
                    # -1 from actual length but configparser makes a DEFAULT section that is not used so the -1 is fine
                    self.nested_list_sections.append([])
            
                for i, k in enumerate((get_file_list(self,'pdf',self.grab_dir))):
                    if (' ' in k):
            
                        #Splits document shorthand, removes leading 0s so that 2.1 is same as 2.01
                        self.doc_id_stage = k.split(' ')[1].replace('.pdf','').split('.')
                        self.doc_id = self.doc_id_stage[0] + '.' + self.doc_id_stage[1].lstrip('0')
                        
                        if self.doc_id[0].isdigit():
            
                            self.section_num = int(self.doc_id[0]) - 1
                            shutil.copy(self.grab_dir + '/' + k, self.work_dir)
                            self.doc_section = (self.config[self.config.sections()[self.section_num]][self.doc_id])
                            self.new_name = self.doc_section.replace(' ','!') + '.pdf' 
                            self.new_full_name = self.work_dir + '/' + self.new_name
                            os.rename(self.work_dir + '/' + k, self.new_full_name)
                            self.nested_list_sections[self.section_num].append(self.new_name)
                            
                for i in self.nested_list_sections:
                    print(i)
            
                for i in range(len(self.nested_list_sections)):
                    if self.nested_list_sections[i]:
                        self.embed_list.append(r'\addsection{' + str(self.config.sections()[i]) + '}')
                        for k in self.nested_list_sections[i]:
                            self.embed_list.append(r'\addpage{' + k + '}')
                
                with open(self.work_dir + '/embedlist.tex', 'w') as self.embed_list_file:
                    for i in self.embed_list:
                        self.embed_list_file.write('%s\n' % i)
                self.embed_list_file.close()
            
            for i in self.embed_list:
                print(i)
            
            def template_stage(self,src,dest):
                
                folder_check(self,dest)
                print('\nWorking directory: ' + str(self.work_dir))
            
                shutil.copytree(self.template_dir + '/font/',dest + '/font/')
            
                for i in os.listdir(src):
                    if i.endswith('.tex'):
                        shutil.copy(src + '/' + i,dest)
            
            
            def embed_stage(self,src,dest):
            
                folder_check(self,dest) 
                for i in os.listdir(src):
                    if i.endswith('.pdf'):
                        shutil.copy(src + '/' + i,dest)
                        print (i)    
            
            
            def compile_TeX(self,path,texfile):
                for _ in range(2):
                    p = subprocess.Popen([path, '-recorder', texfile], cwd=self.work_dir)
                    p.wait()
            
            
            def folder_check(self,folder):
                if not os.path.exists(folder):
                    os.mkdir(folder)
            
            
            def job_info(self):
                self.data_file = ['mo = 1234567', 'serial = 12345', 'equipment = RA-24 thing', 'customer = SomeCorp']
            
                with open(self.work_dir + '/jobinfo.dat', 'w') as self.job_info_file:
                    for i in self.data_file:
                        self.job_info_file.write('%s\n' % i)
                self.job_info_file.close()
            
            
            def output_pdf(self,output_path):
                folder_check(self,output_path)
                print('\nOutput directory: ' + str(output_path))
                shutil.copy(self.work_dir + '/databook.pdf', output_path)
            
            
            template_stage(self, self.template_dir, self.work_dir)
            pdf_rename(self)
            job_info(self)
            compile_TeX(self, self.xelatex_path, 'databook') 
            output_pdf(self, self.output_dir)



class EmittingStream(QtCore.QObject):

    textWritten = QtCore.pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))

class EmittingStream(QtCore.QObject):

    textWritten = QtCore.pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))

class Interface(PfaudUI.Ui_MainWindow):
    def __init__(self):
        super().setupUi(MainWindow)

        sys.stdout = EmittingStream(textWritten=self.normalOutputWritten)
    
    def __del__(self):
        # Restore sys.stdout
        sys.stdout = sys.__stdout__
    
    def normalOutputWritten(self, text):
        """Append text to the QTextEdit."""
        # Maybe QTextEdit.append() works as well, but this is how I do it:
        cursor = self.textEdit.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.textEdit.setTextCursor(cursor)
        self.textEdit.ensureCursorVisible()
    



app = QtGui.QApplication(sys.argv)
MainWindow = QtGui.QMainWindow()
ui = Interface()
MainWindow.show()
#print('text')
data_book = DataBook()
sys.exit(app.exec_())



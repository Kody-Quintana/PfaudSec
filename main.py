import sys
import subprocess
from PyQt4 import QtCore, QtGui, uic
import tempfile
import os
import shutil
import configparser
import redirect #name of interface file


# This replaces print() to output python related messages to a QTextEdit from redirect.py
def pronk(text):
    win.main_append(str(text) + '\n')

#Global tempory working directory for XeLaTeX to use
work_dir = tempfile.mkdtemp(prefix='PfaudSec_')

output_dir = None

class DataBook(object):
    
    def __init__(self):
        self.embed_list = []
        self.nested_list_sections = []
        
        self.config_file = 'sections_config.ini'
        self.grab_dir = None
        self.template_dir = './TeX'
        self.xelatex_config()

    def xelatex_config(self):
        self.xelatex_config_file = 'PfaudSec_config.ini'
        self.xelatex_config = configparser.ConfigParser()
        self.xelatex_config.read(self.config_file)
        self.xelatex_path = 'xelatex'

    def reset(self):
        self.embed_list = []
        self.nested_list_sections = []


# Implement later if pyinstaller is used
#    def resource_path(self,relative_path):
#        #Get absolute path to resource, works for dev and for PyInstaller
#        try:
#            # PyInstaller creates a temp folder and stores path in _MEIPASS
#            base_path = sys._MEIPASS
#        except Exception:
#            base_path = os.path.abspath(".")
#    
#        return os.path.join(base_path, relative_path)

    def data_book_run(self):

        global work_dir 
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file)
        pronk('Starting PfaudSec DataBook compiler.\nLoaded sections from '\
                + str(self.config_file) + ':\n')
        for i in self.config.sections():
            pronk('Section: ' + str(i))
        pronk('')
        
        
        def get_file_list(self,ext,dir):
            self.list = []
            for i in os.listdir(dir):
                if i.endswith(ext):
                    self.list.append(i)
            return sorted(self.list)
        
        def pdf_rename(self):
        
            for l in range(len(self.config.sections())): 
                # -1 from actual length but configparser makes a DEFAULT section that is not used so the -1 is fine
                self.nested_list_sections.append([])
            
            def pdf_skip(self,skipped_pdf):
                pronk('\nSkipping PDF file: "' + str(skipped_pdf) + '" (is name malformed?)')

            for i, k in enumerate((get_file_list(self,'pdf',self.grab_dir))):
                if (' ' in k):
        
                    #Splits document shorthand, removes leading 0s so that 2.1 is same as 2.01
                    try:
                        self.doc_id_stage = k.split(' ')[1].replace('.pdf','').split('.')
                        self.doc_id = self.doc_id_stage[0] + '.' + self.doc_id_stage[1].lstrip('0')
                        
                        if self.doc_id[0].isdigit():
        
                            self.section_num = int(self.doc_id[0]) - 1
                            shutil.copy(self.grab_dir + '/' + k, work_dir)
                            self.doc_section = (self.config[self.config.sections()\
                                    [self.section_num]][self.doc_id])
                            self.new_name = self.doc_section.replace(' ','!') + '.pdf' 
                            self.new_full_name = work_dir + '/' + self.new_name
                            os.rename(work_dir + '/' + k, self.new_full_name)
                            self.nested_list_sections[self.section_num].append(self.new_name)
                        else:
                            pdf_skip(self,k)

                    #This should catch and skip anything not matching an entry in sections_config.ini
                    except(IndexError):
                        pdf_skip(self,k)

                #for catching PDF files that dont have a space in their name
                else:
                    pdf_skip(self,k)

            pronk('\nLoading documents found in:\n"' + str(self.grab_dir) + '"\n\nFound:')
            for i in self.nested_list_sections:
                pronk(str(i).replace('!', ' '))
        
            for i in range(len(self.nested_list_sections)):
                if self.nested_list_sections[i]:
                    self.embed_list.append(r'\addsection{' + str(self.config.sections()[i]) + '}')
                    for k in self.nested_list_sections[i]:
                        self.embed_list.append(r'\addpage{' + k + '}')
            
            with open(work_dir + '/embedlist.tex', 'w') as self.embed_list_file:
                for i in self.embed_list:
                    self.embed_list_file.write('%s\n' % i)
            self.embed_list_file.close()
        
        for i in self.embed_list:
            pronk(i)
        
        def template_stage(self,src,dest):
            
            folder_check(self,dest)
            pronk('Working directory: ' + str(work_dir))
        
            try:
                shutil.copytree(self.template_dir + '/font/',dest + '/font/')
            except:
                pass

            for i in os.listdir(src):
                if i.endswith('.tex'):
                    shutil.copy(src + '/' + i,dest)
        
        
        def embed_stage(self,src,dest):
        
            folder_check(self,dest) 
            for i in os.listdir(src):
                if i.endswith('.pdf'):
                    shutil.copy(src + '/' + i,dest)
                    pronk (i)    
        
        
        def compile_TeX(self,path,texfile):
            win.compile_tex('xelatex', str(work_dir))
        
        
        def folder_check(self,folder):
            if not os.path.exists(folder):
                os.mkdir(folder)
        
        
        def job_info(self):
            self.data_file = ['mo = ' + str(win.job_entry_1.text()), 
                    'serial = ' + str(win.job_entry_2.text()), 
                    'customer = ' + str(win.job_entry_3.text()),
                    'equipment = ' + str(win.job_entry_4.text())] 
        
            with open(work_dir + '/jobinfo.dat', 'w') as self.job_info_file:
                for i in self.data_file:
                    self.job_info_file.write('%s\n' % i)
            self.job_info_file.close()
        
        
        
        template_stage(self, self.template_dir, work_dir)
        pdf_rename(self)
        job_info(self)
        win.compile_tex(self.xelatex_path, work_dir) 
        #output_pdf(self, self.output_dir)

    def folder_check(self,folder):
        if not os.path.exists(folder):
            os.mkdir(folder)

    def output_pdf(self):
        global work_dir
        global output_dir
        self.folder_check(output_dir)
        pronk('\ndatabook.pdf copied to: ' + str(output_dir) + '\n\n\n\n')
        shutil.copy(work_dir + '/databook.pdf', output_dir)
        shutil.rmtree(work_dir)
        self.reset()
        #win.outputbox_2.clear()

        #change to checkbox for open after compile option
        if True:
            if os.name == "nt":
                os.filestart(output_dir + '/databook.pdf')
            elif os.name == "posix":
                os.system("/usr/bin/xdg-open " + output_dir + '/databook.pdf')  

# pyqt interface
# inherits from redirect.py, 
# the methods below need to be here to reference the data_book class
class Interface(redirect.MainWindow):
    def __init__(self):

        global work_dir
        super().__init__()

        self.latex_render.clicked.connect(lambda: self.latex_btn_render())
        self.grab_sel.clicked.connect(self.get_grab_dir)
        self.output_sel.clicked.connect(self.get_output_dir)

        self.process_0.finished.connect(\
                lambda: self.compile_tex2('xelatex', work_dir))
        self.process_1.finished.connect(\
                lambda: self.latex_btn_render_reenable())

    def latex_btn_render_reenable(self):
        self.latex_render.setEnabled(True)
        data_book.output_pdf()
    
    def latex_btn_render(self):
        #Will not render if job info LineEdits are empty
        if (str(win.job_entry_1.text()) != '')\
                and (str(win.job_entry_2.text()) != '')\
                and (str(win.job_entry_1.text()) != '')\
                and (str(win.job_entry_1.text()) != ''):

            self.latex_render.setEnabled(False)
            data_book.data_book_run()
        else:
            pronk('Missing Job Info')

    #Button function: folder select for output
    def get_output_dir(self):
        global output_dir
        file = str(QtGui.QFileDialog.getExistingDirectory(\
                self, "Select PDF Output Directory"))
        if file:
            output_dir = file
            self.output_display.clear()
            self.output_display.append(str(file))


    #Button function: folder select for grab dir
    def get_grab_dir(self):
        file = str(QtGui.QFileDialog.getExistingDirectory(\
                self, "Select Job Documents Directory"))
        if file:
            data_book.grab_dir = file
            self.grab_display.clear()
            self.grab_display.append(str(file))

app = QtGui.QApplication(sys.argv)
win = Interface()
win.show()


#Global font size
font = QtGui.QFont()
font.setPointSize(17)
app.setFont(font)

data_book = DataBook()

sys.exit(app.exec_())


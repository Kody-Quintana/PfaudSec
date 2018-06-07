import sys
import unicodedata
import re
import subprocess
from PyQt5 import QtCore, QtGui, uic, QtWidgets
import tempfile
import os
import shutil
import configparser
import redirect #name of interface file
import qdarkstyle


# This replaces print() to output python related messages to a QTextEdit from redirect.py
def pronk(text):
    win.main_append(str(text) + '\n')

#Global tempory working directory for XeLaTeX to use
#work_dir = tempfile.mkdtemp(prefix='PfaudSec_')

grab_dir = ''
output_dir = None

class DataBook(object):
    
    def __init__(self):
        self.embed_list = []
        self.nested_list_sections = []
        
        self.config_file = 'sections_config.ini'
        self.template_dir = 'TeX'
        self.xelatex_config()

    def xelatex_config(self):
        #self.xelatex_config_file = 'PfaudSec_config.ini'
        #self.xelatex_config = configparser.ConfigParser()
        #self.xelatex_config.read(self.config_file)
        if os.name == "nt":
            self.xelatex_path = 'texlive/bin/win32/xelatex.exe'
        elif os.name == "posix":
            self.xelatex_path = 'xelatex'


    def reset(self):
        global work_dir
        self.embed_list = []
        self.nested_list_sections = []
        shutil.rmtree(work_dir)
        os.makedirs(work_dir)


    def data_book_run(self):

        global work_dir 
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file)
        pronk('Starting PfaudSec DataBook compiler.\nLoaded sections from '\
                + str(self.config_file) + ':\n')
        for i in self.config.sections():
            pronk('Section: ' + str(i))
        pronk('')
        
        
        def get_file_list(self,dir):
            global grab_dir
            pronk('\nLoading documents found in:\n"' + str(grab_dir) + '"\n')
            doc_pattern = re.compile("([^\s]+ \d+\.\d+\.pdf)")
            self.list = []
            for i in os.listdir(dir):
                self.file_list_flag = 0
                if doc_pattern.match(i):
                    for j in self.config.sections():
                        for (x,y) in self.config.items(j):
                            i_dot_split = str(str(i).split(' ')[1]).split('.')
                            if str(i_dot_split[0]) + '.' + str(i_dot_split[1]).lstrip('0') == str(x):
                                self.list.append(i)
                                self.file_list_flag = 1
                    if self.file_list_flag == 0: 
                        pronk('Skipping PDF file: "' + str(i) + '" (name not in sections_config.ini)')
                else:
                    if i.endswith('pdf'):
                        pronk('Skipping PDF file: "' + str(i) + '" (is name malformed?)')
            return sorted(self.list)
        

        def pdf_rename(self):
            global grab_dir
        
            for l in range(len(self.config.sections())): 
                # -1 from actual length but configparser makes a DEFAULT section that is not used so the -1 is fine
                self.nested_list_sections.append([])
            
            def pdf_skip(self,skipped_pdf):
                pronk('\nSkipping PDF file: "' + str(skipped_pdf) + '" (is name malformed?)')

            for i, k in enumerate((get_file_list(self,grab_dir))):
        
                #Splits document shorthand, removes leading 0s so that 2.1 is same as 2.01
                try:
                    self.doc_id_stage = k.split(' ')[1].replace('.pdf','').split('.')
                    self.doc_id = self.doc_id_stage[0] + '.' + self.doc_id_stage[1].lstrip('0')
                    self.section_num = int(self.doc_id[0]) - 1
                    shutil.copy(grab_dir + '/' + k, work_dir)
                    self.doc_section = (self.config[self.config.sections()\
                            [self.section_num]][self.doc_id])
                    self.new_name = self.doc_section.replace(' ','!') + '.pdf' 
                    self.new_full_name = work_dir + '/' + self.new_name
                    os.rename(work_dir + '/' + k, self.new_full_name)
                    self.nested_list_sections[self.section_num].append(self.new_name)

                #This should catch and skip anything not matching an entry in sections_config.ini
                except IndexError:
                    pdf_skip(self,k)
                except FileExistsError:
                    pdf_skip(self,k)

            
            pronk('\n\nFound:')
            for i in self.nested_list_sections:
                pronk(str(i).replace('!', ' ').replace('.PDF', '').replace('.pdf', ''))
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
        
        def strip_accents(self, s):
           return ''.join(c for c in unicodedata.normalize('NFD', s)
                          if unicodedata.category(c) != 'Mn')
        

        def loose_files_stage(self, input_loose_name, path):

                global work_dir

                self.loose_embed_list = [] 
                self.loose_name = str(input_loose_name).replace(' ', '!')
                self.folder_check(work_dir + r'/' + self.loose_name)                

                def try_copy(src, dest):
                    #this is not a good way, change later
                    try:
                        shutil.copy(src, dest)
                    except FileExistsError:
                        pass
                
                for root, dirs, files in os.walk(path):
                    for j in files:
                        if j.endswith('.pdf'):
                            self.loose_embed_list.append(str(root + r'/' + j).replace(r'//',r'/'))
                self.loose_embed_list.sort()
                            
                
                for i in self.loose_embed_list:
                    try_copy(i, work_dir + r'/' + self.loose_name)
                    # strip_accents(self, self.input)

                for i in os.listdir(work_dir + '/' + self.loose_name):
                    if i.endswith('.pdf'):
                        os.rename(work_dir + '/' + self.loose_name + '/' + i,
                                work_dir + '/' + self.loose_name + '/' + strip_accents(self, i\
                                        .replace('-','')\
                                        .replace('_','!')\
                                        .replace(' ','!')))
                
                
                with open(work_dir + '/embedlist.tex', 'a') as self.embed_list_file:
                    self.embed_list_file.write('\n' + r'\addsection{' 
                            + self.loose_name.replace('!',' ') + '}')

                    for i in self.loose_embed_list:
                        self.embed_list_file.write('\n' 
                                + r'\addpage{' 
                                + self.loose_name 
                                + '/' 
                                + strip_accents(self, str(i\
                                        .replace('-','')\
                                        .replace('_','!')\
                                        .replace(' ','!')\
                                        .split('/')[len(i.split('/')) - 1]))
                                + '}')

                    self.embed_list_file.close()

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
            win.compile_tex(data_book.xelatex_path, str(work_dir))
        
        
        def folder_check(self,folder):
            if not os.path.exists(folder):
                os.mkdir(folder)
        
        
        def job_info(self):
            self.data_file = ['mo = ' + str(win.job_entry_1.text()).replace('\\',''), 
                    'serial = ' + str(win.job_entry_2.text()).replace('\\',''),
                    'customer = ' + str(win.job_entry_3.text()).replace('\\',''),
                    'equipment = ' + str(win.job_entry_4.text()).replace('\\','')] 
        
            with open(work_dir + '/jobinfo.dat', 'w') as self.job_info_file:
                for i in self.data_file:
                    self.job_info_file.write('%s\n' % i)
            self.job_info_file.close()
        
        
        
        template_stage(self, self.template_dir, work_dir)
        pdf_rename(self)
        job_info(self)


       # Runs loose files if checkboxes are checked

        if win.checkBox_loose_0.isChecked() and win.lineEdit_loose_0.text() != '':
            loose_files_stage(self, 'Pfaudler Brazil Data Book', win.lineEdit_loose_0.text())

        if win.checkBox_loose_1.isChecked() and win.lineEdit_loose_1.text() != '':
            loose_files_stage(self, 'Pfaudler Brazil Data Book', win.lineEdit_loose_1.text())

        if win.checkBox_loose_2.isChecked() and win.lineEdit_loose_2.text() != '':
            loose_files_stage(self, win.lineEdit_loose_name_2.text(), win.lineEdit_loose_2.text())

        win.compile_tex(self.xelatex_path, work_dir) 

    def folder_check(self,folder):
        if not os.path.exists(folder):
            os.mkdir(folder)

    def output_pdf(self):
        global work_dir
        global output_dir

        try:

            self.folder_check(str(output_dir))
            pronk('\ndatabook.pdf copied to: ' + str(output_dir))
            shutil.copy(work_dir + '/databook.pdf',str(output_dir))
            #shutil.rmtree(work_dir)
            self.reset()
            #win.outputbox_2.clear()

            #change to checkbox for open after compile option
            if True:
                if os.name == "nt":
                    os.startfile(output_dir + '/databook.pdf')
                elif os.name == "posix":
                    os.system("/usr/bin/xdg-open " + output_dir + '/databook.pdf')  
        except:
            pass

# pyqt interface
# inherits from redirect.py, 
# the methods below need to be here to reference the data_book class
class Interface(redirect.MainWindow):
    def __init__(self):

        global work_dir
        super().__init__()
        
        

        #self.checkBox.stateChanged.connect(self.output_same_dir)
        #self.checkBox.setChecked(True)

        #self.checkBox.stateChanged.connect(self.output_same_dir)

        self.latex_render.clicked.connect(self.latex_btn_render)
        self.grab_sel.clicked.connect(self.get_grab_dir)
        self.output_sel.clicked.connect(self.get_output_dir)

        self.actionSections_config.triggered.connect(self.edit_sections_config)
        self.actionUser_Procedure.triggered.connect(self.open_procedure)

        self.process_0.finished.connect(\
                lambda: self.compile_tex1(data_book.xelatex_path, work_dir))

        self.process_1.finished.connect(\
                lambda: self.compile_tex2(data_book.xelatex_path, work_dir))

        self.process_2.finished.connect(\
                lambda: self.latex_btn_render_reenable())

        QtWidgets.QShortcut(QtGui.QKeySequence("Return"), self, \
                lambda: self.enter_key())

        QtWidgets.QShortcut(QtGui.QKeySequence("Enter"), self, \
                lambda: self.enter_key())
    

    def open_procedure(self):
        try:
            if os.name == "nt":
                os.startfile('user_procedure.pdf')
            elif os.name == "posix":
                os.system("/usr/bin/xdg-open " + 'user_procedure.pdf')  
        except:
            pronk('Can\'t find user_procedure.pdf')

    def edit_sections_config(self):
        if os.name == "nt":
            os.startfile('sections_config.ini')
        elif os.name == "posix":
            os.system("/usr/bin/xdg-open " + 'sections_config.ini')  
        
    def enter_key(self):
        if self.grab_sel.hasFocus():
            self.grab_sel.click()
        elif self.output_sel.hasFocus():
            self.output_sel.click()
        else:
            self.latex_render.click()

    def latex_btn_render_reenable(self):
        self.latex_render.setEnabled(True)
        data_book.output_pdf()
   

    def latex_btn_render(self):
        #Will not render if job info LineEdits are empty
        if (str(win.job_entry_1.text()) != '')\
                and (str(self.job_entry_2.text()) != '')\
                and (str(self.job_entry_3.text()) != '')\
                and (str(self.job_entry_4.text()) != '')\
                and (str(self.output_display.toPlainText()) != '')\
                and (str(self.grab_display.toPlainText()) != ''):

            self.latex_render.setEnabled(False)
            pronk('\n\n\n\n')
            data_book.data_book_run()
        else:
            pronk('Missing one or more fields')
    

    def output_same_dir(self):
        global grab_dir
        global output_dir
        if self.checkBox.isChecked():
            self.output_sel.setEnabled(False)
            self.output_display.setText(self.grab_display.toPlainText())
            if str(output_dir) != '':
                output_dir = grab_dir

        else:
            self.output_sel.setEnabled(True)

    #Button function: folder select for output
    def get_output_dir(self):
        global output_dir
        file = str(QtWidgets.QFileDialog.getExistingDirectory(\
                self, "Select PDF Output Directory"))
        if file:
            output_dir = file
            self.output_display.clear()
            self.output_display.append(str(file))


    #Button function: folder select for grab dir
    def get_grab_dir(self):
        global output_dir
        global grab_dir
        file = str(QtWidgets.QFileDialog.getExistingDirectory(\
                self, "Select Job Documents Directory"))
        if file:
            grab_dir = file
            self.grab_display.clear()
            self.grab_display.append(str(file))

            if win.checkBox.isChecked():
                output_dir = file
                self.output_display.clear()
                self.output_display.append(str(file))
        print(str(output_dir))

with tempfile.TemporaryDirectory(prefix='PfaudSec_') as work_dir:

    app = QtWidgets.QApplication(sys.argv)
    win = Interface()
    win.show()
    
    #Global font size
    font = QtGui.QFont()
    font.setPointSize(14)
    app.setFont(font)
    
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    
    
    data_book = DataBook()
sys.exit(app.exec_())


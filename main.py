import sys
import subprocess
from PyQt4 import QtCore, QtGui, uic
import tempfile
import os
import shutil
import configparser
import redirect


def pronk(text):
    win.main_append(str(text) + '\n')

work_dir = tempfile.mkdtemp(prefix='PfaudSec_')

output_dir = None


class PfaudSecConfig(object):
    def __init__(self):

        self.config_file = 'PfaudSec_config.ini'
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file)


class DataBook(object):
    
    def __init__(self):
        self.embed_list = []
        self.nested_list_sections = []
        
        self.config_file = 'sections_config.ini'
        self.xelatex_path = 'xelatex'
        #self.xelatex_path = input('Enter path to xelatex: ')
        #work_dir = './work'
        self.grab_dir = None
        self.template_dir = './TeX'
    
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
        pronk('Starting PfaudSec DataBook compiler.\nLoaded sections from ' + str(self.config_file) + ':\n')
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
        
            for i, k in enumerate((get_file_list(self,'pdf',self.grab_dir))):
                if (' ' in k):
        
                    #Splits document shorthand, removes leading 0s so that 2.1 is same as 2.01
                    try:
                        self.doc_id_stage = k.split(' ')[1].replace('.pdf','').split('.')
                        self.doc_id = self.doc_id_stage[0] + '.' + self.doc_id_stage[1].lstrip('0')
                        
                        if self.doc_id[0].isdigit():
        
                            self.section_num = int(self.doc_id[0]) - 1
                            shutil.copy(self.grab_dir + '/' + k, work_dir)
                            self.doc_section = (self.config[self.config.sections()[self.section_num]][self.doc_id])
                            self.new_name = self.doc_section.replace(' ','!') + '.pdf' 
                            self.new_full_name = work_dir + '/' + self.new_name
                            os.rename(work_dir + '/' + k, self.new_full_name)
                            self.nested_list_sections[self.section_num].append(self.new_name)

                    #This should catch and skip anything not matching an entry in sections_config.ini
                    except(IndexError):
                        pronk('\nSkipping PDF file: "' + str(k) + '" (is name malformed?)')
                else:
                    pronk('\nSkipping PDF file: "' + str(k) + '" (is name malformed?)')

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

class Interface(redirect.MainWindow):
    def __init__(self):

        global work_dir
        super().__init__()

        self.latex_render.clicked.connect(lambda: self.latex_btn_render())
        self.grab_sel.clicked.connect(self.get_grab_dir)
        self.output_sel.clicked.connect(self.get_output_dir)
        
        pal = QtGui.QPalette()
        bgc = QtGui.QColor(255, 255, 255)
        pf_blue = QtGui.QColor(58, 135, 197)
        pf_grey = QtGui.QColor(125, 125, 130)
        pal.setColor(QtGui.QPalette.Base, bgc)
        textc = QtGui.QColor(0,0,0)
        pal.setColor(QtGui.QPalette.Text, textc)
        self.outputbox.setPalette(pal)
        self.outputbox_2.setPalette(pal)

        font_instance = QtGui.QFontDatabase
        PfFont = font_instance.addApplicationFont("TeX/font/TTF/Pfaudler-Book.ttf")
        pf_font_family = font_instance.applicationFontFamilies(PfFont)[0]
        pf_font = QtGui.QFont(pf_font_family)

        PfFontBold = font_instance.addApplicationFont("TeX/font/TTF/Pfaudler-Bold.ttf")
        pf_font_family_bold = font_instance.applicationFontFamilies(PfFontBold)[0]
        pf_font_bold = QtGui.QFont(pf_font_family_bold)

        self.setFont(pf_font_bold)
        self.outputbox.setFont(pf_font)
        self.outputbox_2.setFont(pf_font)

        self.process.finished.connect(lambda: self.compile_tex2('xelatex', work_dir))
        self.process2.finished.connect(lambda: self.latex_btn_render_reenable())


    def get_output_dir(self):
        global output_dir
        file = str(QtGui.QFileDialog.getExistingDirectory(self, "Select PDF Output Directory"))
        if file:
            output_dir = file
            self.output_display.clear()
            self.output_display.append(str(file))

    def get_grab_dir(self):
        file = str(QtGui.QFileDialog.getExistingDirectory(self, "Select Job Documents Directory"))
        if file:
            data_book.grab_dir = file
            self.grab_display.clear()
            self.grab_display.append(str(file))

    def latex_btn_render_reenable(self):
        self.latex_render.setEnabled(True)
        data_book.output_pdf()

    def latex_btn_render(self):
        self.latex_render.setEnabled(False)
        data_book.data_book_run()
    

app = QtGui.QApplication(sys.argv)
win = Interface()
win.show()


font = QtGui.QFont()
font.setPointSize(17)
#self.editor.setFont(font)

#QtGui.QFontDatabase.addApplicationFont("./TeX/font/TTF/Pfaudler-Book.ttf")
app.setFont(font)


#win.compile_tex('xelatex', './')
data_book = DataBook()
#data_book.data_book_run()


sys.exit(app.exec_())


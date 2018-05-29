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


class DataBook(object):
    
    def __init__(self):
        self.embed_list = []
        self.nested_list_sections = []
        
        self.config_file = 'sections_config.ini'
        self.xelatex_path = 'xelatex'
        #self.xelatex_path = input('Enter path to xelatex: ')
        self.work_dir = './work'
        self.output_dir = './output'
        self.grab_dir = './tempemb'
        self.template_dir = './TeX'
    


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

        
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file)
        pronk('\nLoaded sections from ' + str(self.config_file) + ':')
        for i in self.config.sections():
            pronk('Section: ' + str(i))
        pronk('\n')
        
        
        def get_file_list(self,ext,dir):
            self.list = []
            for i in os.listdir(dir):
                if i.endswith(ext):
                    self.list.append(i)
            return self.list
        
        def pdf_rename(self):
        
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
                pronk(i)
        
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
            pronk(i)
        
        def template_stage(self,src,dest):
            
            folder_check(self,dest)
            pronk('\nWorking directory: ' + str(self.work_dir))
        
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
            #for _ in range(2):
                #p = subprocess.Popen([path, '-recorder', texfile], cwd=self.work_dir, stdout=subprocess.PIPE)
                #for line in p.stdout.readlines():
                #    pronk(line)
                #    sys.stdout.flush()
                #p.wait()
            win.compile_tex('xelatex', str(self.work_dir))
        
        
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
            pronk('\nOutput directory: ' + str(output_path))
            shutil.copy(self.work_dir + '/databook.pdf', output_path)
        
        
        template_stage(self, self.template_dir, self.work_dir)
        pdf_rename(self)
        job_info(self)
        compile_TeX(self, self.xelatex_path, 'databook') 
        #output_pdf(self, self.output_dir)




class Interface(redirect.MainWindow):
    def __init__(self):
        super().__init__()
        self.latex_render.clicked.connect(lambda: self.latex_btn_render())
    
    
        self.process2.finished.connect(lambda: self.latex_btn_render_reenable())

    def latex_btn_render_reenable(self):
        self.latex_render.setEnabled(True)

    def latex_btn_render(self):
        self.latex_render.setEnabled(False)
        data_book.data_book_run()

app = QtGui.QApplication(sys.argv)
win = Interface()
win.show()

#win.compile_tex('xelatex', './')
data_book = DataBook()
#data_book.data_book_run()


sys.exit(app.exec_())


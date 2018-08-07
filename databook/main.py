import sys
import traceback
import importlib
import io
import time
import unicodedata
import re
import subprocess
import tempfile
import os
import shutil
import configparser
import qdarkstyle
from PyQt5 import QtGui, QtWidgets
import redirect #name of interface file
import fontload #decrypt fonts

if os.name == "nt":
    sep = '\\'
elif os.name == "posix":
    sep = '/'

def except_box(excType, excValue, tracebackobj):
    """Exceptions from sys.excepthook displayed in a QMessageBox and saved to logfile"""
    logFile = "PfaudSec_databook_crash.log"
    notice = 'An unhandled exception occured. Please report the problem via email to Quintana.Kody@gmail.com'\
            + '\n\nPlease attach the log file ' + logFile + ' from the PfaudSec databook folder to the email.\n'
    versionInfo = "0.0.1"
    timeString = time.strftime("%Y-%m-%d, %H:%M:%S")

    tbinfofile = io.StringIO()
    traceback.print_tb(tracebackobj, None, tbinfofile)
    tbinfofile.seek(0)
    tbinfo = tbinfofile.read()
    errmsg = '%s: \n%s' % (str(excType), str(excValue))
    sep = '\n'
    sections = [sep, timeString, sep, errmsg, sep, tbinfo]
    msg = ''.join(sections)
    try:
        f = open(logFile, "w")
        f.write(msg)
        f.write(versionInfo)
        f.close()
    except IOError:
        pass
    errorbox = QtWidgets.QMessageBox()
    errorbox.setText(str(notice)+str(msg)+str(versionInfo))
    errorbox.exec_()

if sys.platform.startswith("win"):
    #Don't display the Windows GPF dialog if the invoked program dies.
    import ctypes
    SEM_NOGPFAULTERRORBOX = 0x0002 # From MSDN
    ctypes.windll.kernel32.SetErrorMode(SEM_NOGPFAULTERRORBOX);
    CREATE_NO_WINDOW = 0x08000000  # From Windows API
    subprocess_flags = CREATE_NO_WINDOW
else:
    subprocess_flags = 0

def pronk(text):
    """Replace print() to output python related messages to a QTextEdit from redirect.py"""
    win.main_append(str(text) + '\n')

grab_dir = ''
output_dir = None

class DataBook(object):

    def __init__(self):
        self.embed_list = []
        self.nested_list_sections = []

        self.config_file = 'sections_config.ini'
        self.template_dir = 'TeX'
        self.xelatex_path = ''
        self.xelatex_config()

    def xelatex_config(self):
        """Set path to XeLaTeX based on what system is running"""
        if os.name == "nt":
            self.xelatex_path = 'texlive/bin/win32/xelatex.exe'
        elif os.name == "posix":
            self.xelatex_path = 'xelatex'

    def reset(self):
        """Clear variables and delete then recreate working directory"""
        global work_dir
        self.embed_list = []
        self.nested_list_sections = []
        shutil.rmtree(work_dir)
        os.makedirs(work_dir)


    def data_book_run(self):
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file)
        pronk('Starting PfaudSec DataBook compiler.\nLoaded sections from '\
                + str(self.config_file) + ':\n')
        for i in self.config.sections():
            pronk('Section: ' + str(i))
        pronk('')


        def get_file_list(dir):
            """Scan PDF grab folder, return list of matches"""
            pronk('\nLoading documents found in:\n"' + str(grab_dir) + '"\n')
            doc_pattern = re.compile("([^\s]+ \d+\.\d+\.pdf)")
            file_list = []
            for i in os.listdir(dir):
                file_list_flag = 0
                if doc_pattern.match(i):
                    for j in self.config.sections():
                        for (x, y) in self.config.items(j):
                            i_dot_split = str(str(i).split(' ')[1]).split('.')
                            if str(i_dot_split[0]) + '.' + str(i_dot_split[1]).lstrip('0') == str(x):
                                file_list.append(i)
                                file_list_flag = 1
                    if file_list_flag == 0:
                        pronk('Skipping PDF file: "' + str(i) + '" (name not in sections_config.ini)')
                else:
                    if i.endswith('pdf'):
                        pronk('Skipping PDF file: "' + str(i) + '" (is name malformed?)')
            return sorted(file_list)


        def pdf_rename():
            """Rename PDF files to match names from section_config.ini"""
            for l in range(len(self.config.sections())):
                # -1 from actual length but configparser makes a DEFAULT section that is not used so the -1 is fine
                self.nested_list_sections.append([])

            def pdf_skip(skipped_pdf):
                pronk('\nSkipping PDF file: "' + str(skipped_pdf) + '" (is name malformed?)')

            for i, k in enumerate((get_file_list(grab_dir))):
                try:
                    #Split afer space, second part is compared to sections_config keys
                    doc_id_stage = k.split(' ')[1].replace('.pdf', '').split('.')

                    #Removes leading zeros after the "." so 2.01 becomes 2.1
                    doc_id = doc_id_stage[0] + '.' + doc_id_stage[1].lstrip('0')

                    section_num = int(doc_id[0]) - 1
                    shutil.copyfile(grab_dir + '/' + k, work_dir + '/' + k)
                    config_name = (self.config[self.config.sections()\
                            [section_num]][doc_id])

                    #Must remove spaces for pdfpages LaTeX package (space causes errors)
                    new_name = config_name.replace(' ', '!') + '.pdf'
                    new_full_name = work_dir + '/' + new_name
                    os.rename(work_dir + '/' + k, new_full_name)
                    self.nested_list_sections[section_num].append(new_name)

                #This should catch and skip anything not matching an entry in sections_config.ini
                except KeyError:
                    pdf_skip(k)
                except IndexError:
                    pdf_skip(k)
                except FileExistsError:
                    pdf_skip(k)


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
            """Remove accent characters, for use with Brazil documents to prevent XeLaTeX errors"""
            return ''.join(c for c in unicodedata.normalize('NFD', s)
                          if unicodedata.category(c) != 'Mn')


        def loose_files_stage(input_loose_name, path):
            """Adds "loose" PDF files to LaTeX document, named as found (except accented characters)"""
            loose_embed_list = []
            loose_name = str(input_loose_name).replace(' ', '!')
            self.folder_check(work_dir + r'/' + loose_name)

            def try_copy(src, dest):
                try:
                    shutil.copyfile(src, dest)
                except FileExistsError:
                    pass

            for root, dirs, files in os.walk(path):
                for j in files:
                    if j.endswith('.pdf'):
                        loose_embed_list.append(str(root + r'/' + j).replace(r'//', r'/'))
            loose_embed_list.sort()

            for k, i in enumerate(loose_embed_list):
                file_name = str(i.replace('/', sep).split(sep)[len(i.replace('/', sep).split(sep)) - 1])
                try_copy(i, work_dir + r'/' + loose_name + sep + file_name)

            for i in os.listdir(work_dir + '/' + loose_name):
                if i.endswith('.pdf'):
                    os.rename(work_dir + '/' + loose_name + '/' + i,
                            work_dir + '/' + loose_name + '/' + strip_accents(self, i\
                                    .replace('-', '')\
                                    .replace('_', '!')\
                                    .replace(' ', '!')))


            with open(work_dir + '/embedlist.tex', 'a') as embed_list_file:
                embed_list_file.write('\n' + r'\addsection{'
                        + loose_name.replace('!', ' ') + '}')

                for i in loose_embed_list:
                    embed_list_file.write('\n'
                            + r'\addpage{'
                            + loose_name
                            + '/'
                            + strip_accents(self, str(i\
                                    .replace('-', '')\
                                    .replace('_', '!')\
                                    .replace(' ', '!')\
                                    .split('/')[len(i.split('/')) - 1]))
                            + '}')

                embed_list_file.close()

        def template_stage(src, dest):
            """Copy fonts and tex files to working directory"""
            self.folder_check(dest)
            pronk('Working directory: ' + str(work_dir))

            try:
                shutil.copytree(self.template_dir + '/font/', dest + '/font/')
            except:
                pass

            for i in os.listdir(src):
                if i.endswith('.tex'):
                    shutil.copyfile(src + '/' + i, dest + '/' + i)


        def job_info():
            """Create jobinfo.dat for use by LaTeX document to enter job information"""
            data_file = ['mo = ' + str(win.job_entry_1.text()).replace(sep, ''),
                    'serial = ' + str(win.job_entry_2.text()).replace(sep, ''),
                    'customer = ' + str(win.job_entry_3.text()).replace(sep, ''),
                    'equipment = ' + str(win.job_entry_4.text()).replace(sep, '')]

            with open(work_dir + '/jobinfo.dat', 'w') as job_info_file:
                for i in data_file:
                    job_info_file.write('%s\n' % i)



        template_stage(self.template_dir, work_dir)
        pdf_rename()
        job_info()


        # Runs loose files if checkboxes are checked
        if win.checkBox_loose_0.isChecked() and win.lineEdit_loose_0.text() != '':
            loose_files_stage('Pfaudler Brazil Data Book', win.lineEdit_loose_0.text())

        if win.checkBox_loose_1.isChecked() and win.lineEdit_loose_1.text() != '':
            loose_files_stage('Pfaudler Brazil Second Data Book', win.lineEdit_loose_1.text())

        if win.checkBox_loose_2.isChecked() and win.lineEdit_loose_2.text() != '':
            loose_files_stage(win.lineEdit_loose_name_2.text(), win.lineEdit_loose_2.text())


        # Runs all pdfs through ghostscript
        comp_level = {0 : '/prepress', 1 : '/printer', 2 : '/ebook', 3 : '/screen'}
        pronk('Scanning and repairing PDF files (interface will hang during this process)\n(Compression level: '
                + comp_level.get(int(win.spinBox.value())).replace('/', '') + ')')
        app.processEvents()
        if os.name == "nt":
            self.gs_path = os.path.dirname(os.path.realpath(__file__)) + '/Ghostscript/bin/gswin32c.exe'
        elif os.name == "posix":
            self.gs_path = 'gs'
        for root, dirs, files in os.walk(work_dir):
            for i in files:
                if i.endswith('.pdf'):
                    self.folder_check(os.path.expandvars(root) + sep + 'repair' + sep)
                    pronk('Working on ' + str(i).replace('!', ' '))
                    app.processEvents()
                    p = subprocess.Popen([self.gs_path,
                        '-sOutputFile=' + str(os.path.expandvars(root) + sep + 'repair' + sep + i),
                        '-sDEVICE=pdfwrite',
                        '-dPDFSETTINGS=' + comp_level.get(int(win.spinBox.value())),
                        '-dBatch',
                        '-dNOPAUSE',
                        #'-dQUIET',
                        str(os.path.expandvars(root) + sep + i)],
                        cwd=os.path.dirname(os.path.realpath(__file__)),
                        stdout=subprocess.PIPE,
                        stdin=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        creationflags=subprocess_flags).communicate()[1]

                    try:
                        shutil.copyfile(root + sep + 'repair' + sep + i, root + sep + i)
                    except FileNotFoundError:
                        print("Couldn't copy file")
        pronk('Ghostscript: Done')

        win.compile_tex(self.xelatex_path, work_dir)

    @staticmethod
    def folder_check(folder):
        """Create folder if it doesn't exist"""
        if not os.path.exists(folder):
            os.mkdir(folder)

    def output_pdf(self):
        """Copy final PDF to output_dir, reset(), and open PDF"""
        global work_dir
        global output_dir

        try:

            self.folder_check(str(output_dir))
            pronk('\ndatabook for ' + win.job_entry_2.text() + ' copied to: ' + str(output_dir))
            os.rename(work_dir + '/databook.pdf', work_dir + '/Pfaudler Databook for ' + win.job_entry_2.text() + '.pdf')
            shutil.copyfile(work_dir + '/Pfaudler Databook for ' + win.job_entry_2.text() + '.pdf',
                    str(output_dir) + '/Pfaudler Databook for ' + win.job_entry_2.text() + '.pdf')
            self.reset()

            if os.name == "nt":
                os.startfile(output_dir + '/Pfaudler Databook for ' + win.job_entry_2.text() + '.pdf')
            elif os.name == "posix":
                subprocess.call(["/usr/bin/xdg-open", output_dir + '/Pfaudler Databook for ' + win.job_entry_2.text() + '.pdf'])

        except:
            pass

class Interface(redirect.MainWindow):
    """pyqt interface

    inherits from redirect.py,
    the methods below need to be here to reference the data_book class
    """

    def __init__(self):

        global work_dir
        super().__init__()

        self.latex_render.clicked.connect(self.latex_btn_render)
        self.grab_sel.clicked.connect(self.get_grab_dir)
        self.output_sel.clicked.connect(self.get_output_dir)

        self.setWindowIcon(QtGui.QIcon('TeX/db_logo.ico'))

        self.actionSections_config.triggered.connect(self.edit_sections_config)
        self.actionUser_Procedure.triggered.connect(self.open_procedure)

        self.process_0.finished.connect(\
                lambda: self.compile_tex1(data_book.xelatex_path, work_dir))

        self.process_1.finished.connect(\
                lambda: self.compile_tex2(data_book.xelatex_path, work_dir))

        self.process_2.finished.connect(self.latex_btn_render_reenable)

        QtWidgets.QShortcut(QtGui.QKeySequence("Return"), self, self.enter_key)

        QtWidgets.QShortcut(QtGui.QKeySequence("Enter"), self, self.enter_key)

    def error_message(self, message):
        QtWidgets.QMessageBox.warning(self, 'Error', message)

    def open_procedure(self):
        """Open user_procedure.pdf in default program"""
        try:
            if os.name == "nt":
                os.startfile('user_procedure.pdf')
            elif os.name == "posix":
                os.system("/usr/bin/xdg-open " + 'user_procedure.pdf')
        except:
            pronk('Can\'t find user_procedure.pdf')

    def edit_sections_config(self):
        """Open sections_config.ini in default editor"""
        if os.name == "nt":
            os.startfile('sections_config.ini')
        elif os.name == "posix":
            os.system("/usr/bin/xdg-open " + 'sections_config.ini')

    def enter_key(self):
        """Determine behavior of enter key based on what has focus"""
        if self.grab_sel.hasFocus():
            self.grab_sel.click()
        elif self.output_sel.hasFocus():
            self.output_sel.click()
        else:
            self.latex_render.click()

    def latex_btn_render_reenable(self):
        """Allow render button to be clicked after compile"""
        self.latex_render.setEnabled(True)
        data_book.output_pdf()


    def latex_btn_render(self):
        """Button function to run data_book_run()
        
        will not render if job info LineEdits are empty"""
        if (str(win.job_entry_1.text()) != '')\
                and (str(self.job_entry_2.text()) != '')\
                and (str(self.job_entry_3.text()) != '')\
                and (str(self.job_entry_4.text()) != '')\
                and (str(self.output_display.toPlainText()) != '')\
                and (str(self.grab_display.toPlainText()) != ''):

            self.latex_render.setEnabled(False)
            win.outputbox_2.clear()
            data_book.data_book_run()
        else:
            pronk('Missing one or more fields')


    def output_same_dir(self):
        """Make output folder same as grab folder if option checked"""
        global output_dir
        if self.checkBox.isChecked():
            self.output_sel.setEnabled(False)
            self.output_display.setText(self.grab_display.toPlainText())
            if str(output_dir) != '':
                output_dir = grab_dir

        else:
            self.output_sel.setEnabled(True)

    def get_output_dir(self):
        """Button function: folder select for output"""
        global output_dir
        file = str(QtWidgets.QFileDialog.getExistingDirectory(\
                self, "Select PDF Output Directory"))
        if file:
            output_dir = file
            self.output_display.setText(str(file))


    def get_grab_dir(self):
        """Button function: folder select for grab dir"""
        global output_dir
        global grab_dir
        file = str(QtWidgets.QFileDialog.getExistingDirectory(\
                self, "Select Job Documents Directory"))
        if file:
            grab_dir = file
            self.grab_display.setText(str(file))

            if win.checkBox.isChecked():
                output_dir = file
                self.output_display.setText(str(file))
        print(str(output_dir))

sys.excepthook = except_box
with tempfile.TemporaryDirectory(prefix='PfaudSec_') as work_dir:

    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    win = Interface()
    win.show()

    font_decrypt = fontload.Prompt()
    if font_decrypt.check_success() == False:
        try:
            import Cryptodome
        except:
            pass
        if 'Cryptodome' in sys.modules:
            font_decrypt.show()

    #Global font size
    font = QtGui.QFont()
    font.setPointSize(14)
    app.setFont(font)

    data_book = DataBook()
    sys.exit(app.exec_())

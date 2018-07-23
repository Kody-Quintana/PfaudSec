import datetime
import dateutil.relativedelta
import itertools
import configparser
import os
import time
import sys
#import tempfile
import functools
import shutil
import sharepy
import traceback
import io
import appdirs
import pathlib
import qdarkstyle
from openpyxl import load_workbook
from openpyxl.utils import column_index_from_string #,coordinate_from_string
from collections import Counter
from PyQt5 import QtWidgets, QtCore, QtGui

import sp_prompt #Credentials prompt
import ui_log #Log window
import iniedit
import ini_storage
import date_set

if os.name == 'nt':
    os.chdir(os.path.dirname(sys.executable))

#pgfplots tex file stored as list in a python file
from texstorage import line_graph_tex, bar_graph_tex 

def folder_check(folder):
    pathlib.Path(folder).mkdir(parents = True, exist_ok = True)

def filename_noext(filename):
    """Returns filename with no extension"""
    return filename.split('/')[len(filename.split('/')) - 1].rsplit(".", 1)[0]

def except_box(excType, excValue, tracebackobj):
    """Exceptions from sys.excepthook displayed in a QMessageBox and saved to logfile"""
    logFile = "PfaudSec_spreadsheet_crash.log"
    notice = 'An unhandled exception occured. Please report the problem via email to Quintana.Kody@gmail.com'\
            + '\n\nPlease attach the log file PfaudSec_spreadsheet_crash.log from the PfaudSec spreadsheet folder to the email.\n'
    versionInfo = "0.0.0"
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

class EditConfig(QtWidgets.QDialog, iniedit.Ui_Dialog):
    def __init__(self, mode, file_to_save):
        super(EditConfig, self).__init__()
        self.setupUi(self)
        self.setModal(True)
        font = QtGui.QFontDatabase.systemFont(QtGui.QFontDatabase.FixedFont)
        font.setPointSize(14)
        self.textEdit.setFont(font)
        self.file_to_save = file_to_save

        self.buttonBox.button(QtWidgets.QDialogButtonBox.Save).clicked.connect(self.save_file)

        #TODO make basic text editor for individual workbook configs
        # make example configs for each type, then based on input, open with example config pasted in
        def is_not_empty(item):
            try:
                if os.path.getsize(item) > 0:
                    return True
                else:
                    return False
            except OSError:
                return False


        if is_not_empty(file_to_save):
            with open(file_to_save, 'r') as existing_file:
                self.textEdit.setText(existing_file.read())
        else:
            if mode == 'document':
                self.textEdit.setText(ini_storage.ini_document)
                pass
            elif mode == 'program':
                pass
            else:
                pass

        #mode for what kind of ini to edit, the sharepoint ini or a document ini
    def save_file(self):
        with open(self.file_to_save, 'w') as ini_file:
            ini_file.write(self.textEdit.toPlainText())

    def closeEvent(self, event):
        trayIcon.rebuild_menu()
        #self.save_file()
        #self.hide()
        #event.ignore()


class Grapher(object):

    def __init__(self, work_dir, work_file, doc_name):
        self.ready = False
        try:
            os.remove(work_dir + '/graph.tex')
        except OSError:
            pass
        self.doc_name = filename_noext(doc_name)
        self.work_dir = work_dir
        self.work_file = work_file
        self.config_file = 'resource/' + filename_noext(self.work_file) + '.ini'
        self.config = configparser.ConfigParser()

        def try_config_read(): 
            try:
                with open(self.config_file) as f:
                    self.config.read_file(f)
            except IOError:
                edit_config = EditConfig('document', self.config_file)
                print(self.config_file)
                edit_config.exec_() #Block until closed
                try_config_read() #keep trying until the file exists and is read

        try_config_read()

        # Worksheet number config
        if self.config.has_option('document', 'worksheet'):
            try:
                sheet_number = int(self.config['document']['worksheet'])
                if sheet_number == 0:
                    sheet_number = 1
                    print('Sheet numbers start at 1, setting worksheet to 1 instead of 0')
            except:
                sheet_number = 1
                print('Invalid worksheet specified in ' + str(self.config_file) + ' defaulting to sheet 1')
        else:
            print('No worksheet specified in ' + str(self.config_file) + ' defaulting to sheet 1')
            sheet_number = 1

        self.ws = load_workbook(work_dir + '/' + work_file).worksheets[sheet_number - 1]


        # Date column config
        if self.config.has_option('document', 'date_column'):
            if str(self.config['document']['date_column']).isalpha():
                self.date_column = self.config['document']['date_column']
            else:
                print('Date column must be a letter')
                return
                #exit()
        else:
            print('No date column defined in ' + str(self.config_file))
            return
            #exit()

        self.cells_start, self.cells_end = self.date_cell_range(self.date_column)
        self.ready = True
    
     
    def date_cell_range(self, column):
        """Determines worksheet active rows by first date and last date in input column"""
        last_date_cell = None
        first_date_cell = None
        last_date_counter = 0
    
        for r in self.ws[column + '1':\
                column + str(len(self.ws[column]))]:
            for cell in r:
                last_date_counter = last_date_counter + 1
                if cell.value != None:
                    if isinstance(cell.value, datetime.datetime):
                        last_date_cell = last_date_counter
                        if first_date_cell == None:
                            first_date_cell = last_date_counter
    
        return(str(first_date_cell), str(last_date_cell))
    
    
    def column_list(self, column):
        """For readability, returns a list of all cell.value
        for input column, range determined by date_cell_range()"""
        row_cells = []
        for i in self.ws[column + self.cells_start : column + self.cells_end]:
            for cell in i:
                row_cells.append(cell.value)
        return row_cells
    
    
    def month_string(self, i):
        """returns month as 3 letter string"""
        out = None
        if isinstance(i, datetime.datetime) or isinstance(i, datetime.date):
            out = i.strftime('%b %y')
        else:
            print('Cant convert ' + str(type(i)) + ' to month string')
        return out
    
    
    def cell_enumerate(self, item):
        """enumerate() but index starts at first cell

        as determined by date_cell_range()"""
        i = int(self.cells_start)
        it = iter(item)
        while True:
            yield (i, it.__next__())
            i += 1
    
    
    def unique_column_list(self, column):
        """Returns set of column_list()"""
        values = list(set(self.column_list(column)))
        values.sort
        return values
    
    
    def diff_month(self, d1, d2):
        """Returns how many months apart two dates are"""
        return (d1.year - d2.year) * 12 + d1.month - d2.month
    
    
    def curr_month_values(self, column, blanks=False):
        """Totals for input column for this month"""
        this_month = []
        total_occurances = 0
        for i, j in self.cell_enumerate(self.column_list(column)):
            date_cell = self.ws.cell(i,column_index_from_string(self.date_column)).value
    
            if blanks == False and str(j) == 'None':
                continue #Skips blank cells
    
            if date_cell.month == now.month\
                    and date_cell.year == now.year:
                this_month.append(j)
                total_occurances  += 1
        return Counter(this_month), total_occurances
    
    
    def relative_month_to_string(self, relative_month):
        """Takes relative month as int, returns month string

        int is positive for time in past (think int(x) months ago)"""
        return self.month_string(now 
                - dateutil.relativedelta.relativedelta(\
                        months=int(relative_month)))
    
    
    def totals_by_month_graph(self, months=12, title='Totals by month'):
        """Writes line pgfplot to graph.tex of totals by month"""
        column = self.date_column
        months_counter = [0] * months
        return_dict = {}
        symbolic_xcoords = [] # turns into string later
        coordinates = []
        ticks_distance_flag = 0
    
        for index, data in reversed(list(self.cell_enumerate(self.column_list(self.date_column)))):
            column_value = self.ws[column + str(index)].value
            try:
                months_ago = self.diff_month(now, column_value)
            except AttributeError:
                continue
            if months_ago > (months - 1):
                break
            months_counter[months_ago] += 1
    
        #if any(x > 5 for x in months_counter):
        #    ticks_distance_flag = 1
        for i in months_counter:
            if int(i) > 5:
                ticks_distance_flag = 1
    
        for index, data in reversed(list(enumerate(months_counter))):
            xcoord_name = self.relative_month_to_string(index)
            coordinates.append('(' + xcoord_name + ',' + str(data) + ')')
            symbolic_xcoords.append(xcoord_name + ',')
    
        symbolic_xcoords = '\n'.join([str(i) for i in symbolic_xcoords])
        coordinates = '\n'.join([str(i) for i in coordinates])
    
        with open(self.work_dir + '/graph.tex', 'a', encoding='utf-8') as graphs_file:
            graphs_file.write(line_graph_tex[0])
            graphs_file.write(title + ' - ' + now.strftime('%B, %Y'))
            graphs_file.write(line_graph_tex[1])
            graphs_file.write(symbolic_xcoords)
            graphs_file.write(line_graph_tex[2])
            if ticks_distance_flag == 0:
                graphs_file.write('ytick distance=1,')
            graphs_file.write(line_graph_tex[3])
            graphs_file.write(coordinates)
            graphs_file.write(line_graph_tex[4])
    
    
    def values_by_month(self, column, months=12):
        """returns dict of tuples, tuple index is how many months ago data is for"""
        catagories_index = {} #dict to get index from string for catagories
        catagories = []       #list of lists for each catagory
        return_dict = {}
        for k, i in reversed(list(self.cell_enumerate(self.column_list(self.date_column)))):
            column_value = str(self.ws[column + str(k)].value) #This must be str to allow sorted()
            try:
                months_ago = self.diff_month(now, i)
            except AttributeError:
                continue
            if months_ago > (months - 1):
                break
            if column_value not in catagories_index:
                catagories_index[column_value] = len(catagories_index)
                catagories.append([0] * months) #index is how many months ago
            catagories[catagories_index.get(column_value)][months_ago] += 1
        
        for i in catagories_index:
            return_dict[i] = tuple(catagories[catagories_index.get(i)])
        return(return_dict)
    
    
    def current_month_graph(self, column, title, blanks=False):
        """Writes bar/pareto pgfplot to graph.tex of current month values"""
        current_data, total_occurances = self.curr_month_values(column, blanks)
    
        symbolic_xcoords = '\n'.join([str(i) + ',' for i \
                in sorted(current_data, key=current_data.get, reverse=True)])
        coordinates = '\n'.join([str(i).replace("'",'') for i in current_data.most_common()])
    
        # ytick distance must be set to 1 for values less than 6
        # or the ytick labels will be non whole numbers
        ticks_distance_flag = 0
        occurances = sorted(current_data.values(), reverse=True)

        for i in occurances:
            if int(i) > 5:
                ticks_distance_flag = 1
    
        pareto = list(itertools.accumulate(occurances))
        pareto = [round(x / total_occurances * 100) for x in pareto]
        pareto = '\n'.join(['(' + str(index) + ',' + str(percent) + ')'\
                for index, percent in enumerate(pareto)])
    
        with open(self.work_dir + '/graph.tex', 'a', encoding='utf-8') as graphs_file:
            graphs_file.write(bar_graph_tex[0])
            graphs_file.write(title + ' - ' + now.strftime('%B, %Y'))
            graphs_file.write(bar_graph_tex[1])
            #TODO make bar width = 0.5/num of bars
            graphs_file.write(symbolic_xcoords)
            graphs_file.write(bar_graph_tex[2])
            if ticks_distance_flag == 0:
                graphs_file.write('ytick distance=1,')
            graphs_file.write(bar_graph_tex[3])
            graphs_file.write(coordinates)
            graphs_file.write(bar_graph_tex[4])
            graphs_file.write(pareto)
            graphs_file.write(bar_graph_tex[5])
    
    
    #Uses line graph for one catagory over time
    def monthly_graph(self, column, title, months=12, blanks=False):
        """Writes line pgfplot to graph.tex for one catagory over time"""
        for catagory, month_count_tuple in sorted(self.values_by_month(column, months).items()):
    
            if blanks == False and str(catagory) == 'None':
                continue #this skips empty cells
    
            symbolic_xcoords = []
            coordinates = []
            ticks_distance_flag = 0
    
            # ytick distance must be set to 1 for values less than 6
            # or the ytick labels will be non whole numbers
            for relative_month, occurances in enumerate(month_count_tuple):
                if int(occurances) > 5:
                    ticks_distance_flag = 1
    
                xcoord_month = self.relative_month_to_string(relative_month)
    
                #for use in LaTeX pgfplots package
                symbolic_xcoords.insert(0, xcoord_month + ',')
                coordinates.insert(0, '(' + xcoord_month + ',' + str(occurances) + ')')
    
            #lists changed to str with newlines to avoid using a loop to append to tex file
            symbolic_xcoords = '\n'.join([str(i) for i in symbolic_xcoords])
            coordinates = '\n'.join([str(i) for i in coordinates])
    
            with open(self.work_dir + '/graph.tex', 'a', encoding='utf-8') as graphs_file:
                graphs_file.write(line_graph_tex[0])
                graphs_file.write(title + ' - ' + catagory)
                graphs_file.write(line_graph_tex[1])
                graphs_file.write(symbolic_xcoords)
                graphs_file.write(line_graph_tex[2])
                if ticks_distance_flag == 0:
                    graphs_file.write('ytick distance=1,')
                graphs_file.write(line_graph_tex[3])
                graphs_file.write(coordinates)
                graphs_file.write(line_graph_tex[4])
    
    
    def column_has_data(self, column):
        """Returns true if any data is found in rows of a column"""
        try:
            for r in self.ws[column + '1' : column + str(len(self.ws[column]))]:
                for cell in r:
                    if cell.value != None:
                        return True
        except:
            return False
        return False
    
    
    def compile(self):
        """Calls graph functions based on what is found in config file"""

        if self.ready == False:
            return

        print('Starting PfaudSec Graph compiler.\nLoaded columns from '\
                + str(self.config_file) + ':\n')
        
        # Totals from date column
        if self.config.getboolean('document', 'show_totals', fallback=False):
            self.totals_by_month_graph(title = self.doc_name.replace('_',' '))
    
        non_column_sections = frozenset(('document', 'sharepoint'))
        for column in self.config.sections():
    
            if str(column).lower() in non_column_sections:
                continue
    
            if self.column_has_data(column):
    
                # Bar/Pareto graph for current month
                if self.config.getboolean(column, 'current_month', fallback=False):
                    self.current_month_graph(str(column), str(self.config.get(column, 'title', fallback = '')))
    
                # Line graph for one catagory over time
                if self.config.getboolean(column, 'monthly', fallback=False):
                    self.monthly_graph(str(column), str(self.config.get(column, 'title', fallback = '')))
            else:
                print('UserWarning: Column '
                        + str(column)
                        + ' specified in '
                        + str(self.config_file)
                        + ' does not contain valid data')
        return True
        #This true triggers XeLaTeX to be called

# SharePy no longer working, add later if auth can be fixed    
#class SharePoint(object):
#
#    def __init__(self, *arg, **args):
#        #check is the session files exists
#        self.sp_url = 'pfaudlerazuread.sharepoint.com'
#        #self.file_path = 
#
#        if os.path.isfile(config_folder + '/sp-session.pkl'):
#            try:
#                self.session = sharepy.load(config_folder + '/sp-session.pkl')
#            except AttributeError:
#                self.session = sharepy.connect(self.sp_url, *self.get_cred())
#                self.session.save(config_folder + '/sp-session.pkl')
#
#        else:
#            self.session = sharepy.connect(self.sp_url, *self.get_cred())
#            self.session.save(config_folder + '/sp-session.pkl')
#
#
#    def get_cred(self):
#        """Returns packed login credentials
#        
#        use *self.get_cred() as input to function
#        asking for two variables"""
#        class Prompt(QtWidgets.QDialog, sp_prompt.Ui_Dialog):
#            def __init__(self):
#                super(Prompt, self).__init__()
#                self.setupUi(self)
#                self.setModal(True)
#                self.buttonBox.setEnabled(False)
#                self.lineEdit.textChanged.connect(self.btn_enable)
#                self.lineEdit_2.textChanged.connect(self.btn_enable)
#            def btn_enable(self):
#                if '@' and '.' in self.lineEdit.text() and self.lineEdit_2.text() != '':
#                    self.buttonBox.setEnabled(True)
#                else:
#                    self.buttonBox.setEnabled(False)
#        prompt = Prompt()
#        prompt.exec_()
#        if '@' and '.' in prompt.lineEdit.text() and prompt.lineEdit_2.text() != '':
#            return prompt.lineEdit.text(), prompt.lineEdit_2.text() 
#        else:
#            exit()
#
#    def upload(self, filename):
#        pass

class LogWindow(QtWidgets.QDialog,ui_log.Ui_Dialog):#, UI.MainUI.Ui_MainWindow):
    """Normally hidden log window, also "hosts" the QProcess for calling XeLaTeX"""
    #TODO on xelatex finish, copy pdfs to a folder for upload

    layout_text = {'paper' : r'\usepackage[paperwidth=8.27in, paperheight=11.69in, landscape]{geometry}',
            'screen' : r'\usepackage[paperwidth=7.5in, paperheight=13.33in, landscape]{geometry}'}

    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        self.setupUi(self)
        #TODO set outputbox to readonly
        self.process_0 = QtCore.QProcess(self)
        self.process_0.setProcessChannelMode(QtCore.QProcess.MergedChannels)
        self.process_0.readyRead.connect(self.stdout_and_err_Ready)
        self.process_0.finished.connect(self.done_statement)
        self.process_0.stateChanged.connect(self.menu_disable)
        self.proc_count = 0

        self.xelatex_config()

    def menu_disable(self):
        if self.process_0.state() == 0:
            trayIcon.menu.setEnabled(True)
        else:
            trayIcon.menu.setEnabled(False)

    def done_statement(self):
        if self.process_0.exitCode() == 0:
            return
        else:
            print('XeLaTeX error!')
            self.show()
            self.proc_count = 2

    def xelatex_config(self):
        """Set path to XeLaTeX based on what system is running"""
        if os.name == "nt":
            self.xelatex_path = 'texlive/bin/win32/xelatex.exe'
        elif os.name == "posix":
            self.xelatex_path = 'xelatex'

    def compile_tex(self, work_dir, name, layout, upload):

        self.outputbox.clear()
        #sp_upload = upload

        def layout_name(work_dir, name, layout):
            new_name = work_dir + '/' + filename_noext(name) + ' ' + layout + '.pdf'

            os.replace(work_dir + '/present.pdf',
                    new_name)

            print('XeLaTeX: ' + layout + ' done')
            self.proc_count += 1
            if self.proc_count < 2:
                log.compile_tex(work_dir, name, 'paper', upload)
                log.process_0.finished.disconnect()
                log.process_0.finished.connect(lambda: layout_name(work_dir, name, 'paper'))
            else:
                self.proc_count = 0            
                #if running_local == True:
                #    QtWidgets.qApp.quit()
                    #exit()

            if upload == True:

                headers = {"accept": "application/json;odata=verbose",
                "content-type": "application/x-www-urlencoded; charset=UTF-8"}
                 
                with open(new_name, 'rb') as read_file:
                    content = read_file.read()
                 
                r = sp.session.post(r"https://"
                        + sp.sp_url
                        + r"/sites/"
                        + r"PfaudlerUS"
                        + r"/_api/web/GetFolderByServerRelativeUrl('"
                        + r"QC_CAR" #TODO un-hardcode this
                        + r"/"
                        + r'Graphs'
                        + r"')/Files/add(url='"
                        + filename_noext(name).replace("'",'') + ' ' + layout + '.pdf'
                        + r"',overwrite=true)"
                        , data=content
                        , headers=headers)

                if '200' in str(r):
                    print('Upload successful')
                else:
                    print('Upload Error!')

        with open(work_dir + '/layout.tex', 'w', encoding='utf-8') as layout_file:
            layout_file.write(self.layout_text.get(layout))
        with open(work_dir + '/name.tex', 'w', encoding='utf-8') as name_file:
            name_file.write(filename_noext(name).replace('_',' ') + r'\\' + '\n' + now.strftime('%B, %Y'))

 
        self.process_0.setWorkingDirectory(work_dir)
        self.process_0.start(self.xelatex_path, ['--halt-on-error', 'present'])
        self.process_0.finished.disconnect()
        self.process_0.finished.connect(self.done_statement)
        self.process_0.finished.connect(lambda: layout_name(work_dir, name, 'screen'))

    def append(self, text):
        """Write stdout from XeLaTeX to outputbox"""
        cursor = self.outputbox.textCursor()
        cursor.movePosition(cursor.End)
        cursor.insertText(text)
        cursor.movePosition(cursor.End)
        self.outputbox.verticalScrollBar().setSliderPosition\
                (self.outputbox.verticalScrollBar().maximum())

    def stdout_and_err_Ready(self):
        """Feed stdout from XeLaTeX to self.append()"""
        text = bytearray(self.process_0.readAll())
        text = text.decode("UTF-8")
        self.append(text)


class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    """Program "lives" here, treat like mainwindow, call other functions and classes from here"""

    def __init__(self, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)

        self.menu = QtWidgets.QMenu(parent)
        def menu_func(spreadsheet):
            """Base function to compile graph

            fed to functools.partial to make a button for each spreadsheet based on the config file"""
            print(spreadsheet)
            #with tempfile.TemporaryDirectory(prefix='PfaudSec_') as work_dir:
            work_dir = 'test'
            folder_check(work_dir)
            #TODO Change to if else for downloading or running a file locally
            #make config file for what documents to download and run

            #TODO make this run from the config file
            #sp = SharePoint()

            

            doc_name = "MANUFACTURING CAR's Log.xlsx"
            doc_nospace = doc_name.replace(' ','_')
            sp.session.getfile('https://pfaudlerazuread.sharepoint.com/sites/PfaudlerUS/'
                    + "QC_CAR/"
                    + doc_name,
                    filename = work_dir + '/' + doc_nospace)

            #Sequentially compile documents with both sizes
            log.proc_count = 0 #Reset count incase of previous error before count reset natually
            if Grapher(work_dir, doc_nospace, doc_name).compile():
                log.compile_tex(work_dir, doc_name, 'screen', upload=False)

        #def edit_doc_settings(doc):
        #    print('Open editor for: ' + doc)

        #self.config_file = 'resource/PfaudSec_SpreadSheet.ini'
        #self.config = configparser.ConfigParser()

        #def try_config_read(): 
        #    """Opens config maker, will keep opening if file not found"""
        #    try:
        #        with open(self.config_file) as f:
        #            self.config.read_file(f)
        #    except IOError:
        #        edit_config = EditConfig('program')
        #        edit_config.exec_() #Block until closed
        #        try_config_read() #keep trying until the file exists and is read

        #try_config_read()

        #config_list = ['1','2']
        #for i in config_list:
        #    if str(i) == 'Default':
        #        continue
        #    self.menu.addAction(i).triggered.connect(functools.partial(menu_func, spreadsheet=i))
        #    self.menu.addAction('Edit config for: ' + i).triggered.connect(functools.partial(edit_doc_settings, doc=i))

        #delete_cookie = self.menu.addAction('Delete access cookie and exit')
        #delete_cookie.triggered.connect(lambda: os.remove(config_folder + '/sp-session.pkl'))
        #delete_cookie.triggered.connect(QtWidgets.qApp.quit)


        self.setContextMenu(self.menu)
        self.activated.connect(self.tray_clicked)
        self.click_timer = QtCore.QTimer(self)
        self.click_timer.setSingleShot(True)
        self.click_timer.timeout.connect(self.single_click)

        #Used in write() for sys.stdout
        self.print_queue = []
        self.time_stamp = ''
        self.time_format_str = '%H:%M:%S: '
        self.rebuild_menu()

    def rebuild_menu(self):
        def edit_base_function(config_file):
            edit_config = EditConfig(None, config_file)
            edit_config.exec_() #Block until closed
        open_xlsx = self.menu.addAction('Open spreadsheet file')
        open_xlsx.triggered.connect(self.choose_open_file)

        self.menu.clear()
        for item in os.listdir('resource'):
            if item.endswith('.ini'):
                self.menu.addAction('Edit ' + item).triggered.connect(functools.partial(edit_base_function, config_file = 'resource' + '/' + item))

        run_month = self.menu.addAction('Set graph month')
        run_month.triggered.connect(self.get_run_month)
        exitAction = self.menu.addAction("Exit")
        exitAction.triggered.connect(QtWidgets.qApp.quit)

    def choose_open_file(self):
        pass

    def get_run_month(self):
        class Prompt(QtWidgets.QDialog, date_set.Ui_Dialog):
            def __init__(self):
                super(Prompt, self).__init__()
                self.setupUi(self)
                self.setModal(True)
                self.spinBox.valueChanged.connect(self.update_string)
                font = QtGui.QFontDatabase.systemFont(QtGui.QFontDatabase.FixedFont)
                font.setPointSize(20)
                self.label.setFont(font)
                self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(self.global_now)
                self.label.setText(now.strftime('%B %Y'))

            def update_string(self):
                temp_now = (datetime.date.today() - dateutil.relativedelta.relativedelta(months=int(self.spinBox.value())))
                temp_now = temp_now.strftime('%B %Y')
                self.label.setText(temp_now)

            def global_now(self, event):
                global now
                now = (datetime.date.today() - dateutil.relativedelta.relativedelta(months=int(self.spinBox.value())))
                print('Setting Graph date to: ' + now.strftime('%B %Y'))


        prompt = Prompt()
        prompt.exec_()


    def flush(self, *arg, **args):
        """Used only to suppress errors"""
        pass

    def write(self, text):
        """sys.stdout directed to a system tray message"""
        def append(text):
            cursor = log.outputbox_2.textCursor()
            cursor.movePosition(cursor.End)
            cursor.insertText(text)
            cursor.movePosition(cursor.End)
            log.outputbox.verticalScrollBar().setSliderPosition\
                    (log.outputbox.verticalScrollBar().maximum())
        append(text)
        text = text.rstrip()
        if len(text) == 0:
            return

        #Adds timestamp only if different than previous one
        if datetime.datetime.strftime(datetime.datetime.now(),
                self.time_format_str) == self.time_stamp:
            self.print_queue.append(text)
        else:
            self.print_queue.append(datetime.datetime.strftime(datetime.datetime.now(),
                self.time_format_str)
                    + text)

        self.time_stamp = datetime.datetime.strftime(datetime.datetime.now(), self.time_format_str)
        queue_timer = QtCore.QTimer(self)
        queue_timer.setSingleShot(True)
        queue_timer.timeout.connect(self.clear_queue_line)
        queue_timer.start(4000)
        self.showMessage('PfaudSec spreadsheet:', '\n'.join([str(i) for i in self.print_queue]), icon)

    def clear_queue_line(self):
        """Called from a QTimer to reduce lines displayed in system tray message"""
        try:
            del self.print_queue[0]
        except IndexError:
            pass

    def tray_clicked(self, reason):
        """Determine single or double click with a QTimer"""
        if reason == QtWidgets.QSystemTrayIcon.Trigger:
            self.click_timer.start(QtWidgets.qApp.doubleClickInterval())

        elif reason == QtWidgets.QSystemTrayIcon.DoubleClick:
            self.click_timer.stop()
            self.double_click()

    def double_click(self):
        print('double click')

    def single_click(self):
        if log.isVisible():
            log.hide()
        else:
            log.show()

sys.excepthook = except_box
app = QtWidgets.QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)
app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

now = datetime.date.today() #+ dateutil.relativedelta.relativedelta(months=-1)

icon = QtGui.QIcon('resource/logo.ico')  # need a icon
trayIcon = SystemTrayIcon(icon)
trayIcon.show()
sys.stdout = trayIcon
log = LogWindow()

def local_or_sp():
    for arg in sys.argv:
        if '.xlsx' in arg:
            local_file = arg
    if 'local_file' in locals():
        work_dir = 'test'
        folder_check(work_dir)
        if os.name == 'nt':
            doc_name = local_file.split('\\')
            doc_name = doc_name[len(doc_name) - 1]
        else:
            doc_name = local_file.split('/')
            doc_name = doc_name[len(doc_name) - 1]
        doc_nospace = doc_name.replace(' ','_')
        try:
            shutil.copyfile(local_file, work_dir + '/' + doc_nospace)
        except shutil.SameFileError:
            pass
        if Grapher(work_dir, doc_nospace, doc_name).compile():
            log.compile_tex(work_dir, doc_name, 'screen', upload=False)
        return True
    else:
        return False

running_local = local_or_sp()
if running_local == False:
    pass #Sharepy not authenticating, uncomment to reimplement the auto-download/upload functionality
    #config_folder = appdirs.user_config_dir('PfaudSec')
    #folder_check(config_folder)
    #sp = SharePoint()
def choose_open_file():
    #QT file dialog
    work_dir = 'test'
    folder_check(work_dir)
    if os.name == 'nt':
        doc_name = local_file.split('\\')
        doc_name = doc_name[len(doc_name) - 1]
    else:
        doc_name = local_file.split('/')
        doc_name = doc_name[len(doc_name) - 1]
    doc_nospace = doc_name.replace(' ','_')
    try:
        shutil.copyfile(local_file, work_dir + '/' + doc_nospace)
    except shutil.SameFileError:
        pass
    if Grapher(work_dir, doc_nospace, doc_name).compile():
        log.compile_tex(work_dir, doc_name, 'screen', upload=False)
        

sys.exit(app.exec_())

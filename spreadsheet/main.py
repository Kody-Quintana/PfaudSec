import datetime
import dateutil.relativedelta
import itertools
import configparser
import os
import sys
import tempfile
import shutil
import sharepy
import traceback
import io
import time
import appdirs
from openpyxl import load_workbook
from openpyxl.utils import column_index_from_string #,coordinate_from_string
from collections import Counter
from PyQt5 import QtWidgets, QtCore, QtGui

import sp_prompt

#pgfplots tex file stored as list in a python file
from texstorage import line_graph_tex, bar_graph_tex 

def folder_check(folder):
    """Create folder if it doesn't exist"""
    if not os.path.exists(folder):
        os.mkdir(folder)

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

def filename_noext(filename):
    """Returns filename with no extension"""
    return filename.split('/')[len(filename.split('/')) - 1].rsplit(".", 1)[0]

class EditConfig(QtWidgets.QDialog):
    def __init__(self):
        super(EditConfig, self).__init__()
        # Put a text edit in here for config

    def closeEvent(self, event):
        #self.hide()
        #event.ignore()
        shutil.copyfile('./car_log.ini', 'resource/car_log.ini')

        print('closed now')

class Grapher(object):

    now = datetime.date.today()

    def __init__(self, work_dir, work_file):
        print('Grapher instance start')
        print(os.urandom(10))
        self.work_dir = work_dir
        self.work_file = './car_log.xlsx'
        self.config_file = 'resource/' + filename_noext(self.work_file) + '.ini'
        self.config = configparser.ConfigParser()

        def try_config_read(): 
            try:
                with open(self.config_file) as f:
                    self.config.read_file(f)
            except IOError:
                edit_config = EditConfig()
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

        self.ws = load_workbook(work_file).worksheets[sheet_number - 1]


        # Date column config
        if self.config.has_option('document', 'date_column'):
            if str(self.config['document']['date_column']).isalpha():
                self.date_column = self.config['document']['date_column']
            else:
                print('Date column but be a letter')
                exit()
        else:
            print('No date column defined in ' + str(self.config_file))
            exit()

        self.cells_start, self.cells_end = self.date_cell_range(self.date_column)
    #active_range = range(int(cells_start), int(cells_end))
    
    #if os.name == "nt":
    #    sep = '\\'
    #elif os.name == "posix":
    #    sep = '/'
    
     
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
    
            if date_cell.month == self.now.month\
                    and date_cell.year == self.now.year:
                this_month.append(j)
                total_occurances  += 1
        return Counter(this_month), total_occurances
    
    
    def relative_month_to_string(self, relative_month):
        """Takes relative month as int, returns month string

        int is positive for time in past (think int(x) months ago)"""
        return self.month_string(self.now 
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
            months_ago = self.diff_month(self.now, column_value)
            if months_ago > (months - 1):
                break
            months_counter[months_ago] += 1
    
        for i in months_counter:
            if int(i) > 5:
                ticks_distance_flag = 1
    
        for index, data in reversed(list(enumerate(months_counter))):
            xcoord_name = self.relative_month_to_string(index)
            coordinates.append('(' + xcoord_name + ',' + str(data) + ')')
            symbolic_xcoords.append(xcoord_name + ',')
    
        symbolic_xcoords = '\n'.join([str(i) for i in symbolic_xcoords])
        coordinates = '\n'.join([str(i) for i in coordinates])
    
        with open(self.work_dir + '/graph.tex', 'a') as graphs_file:
            graphs_file.write(line_graph_tex[0])
            graphs_file.write(title)
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
            months_ago = self.diff_month(self.now, i)
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
                ticks_file_flag = 1
    
        pareto = list(itertools.accumulate(occurances))
        pareto = [round(x / total_occurances * 100) for x in pareto]
        pareto = '\n'.join(['(' + str(index) + ',' + str(percent) + ')'\
                for index, percent in enumerate(pareto)])
    
        with open(self.work_dir + '/graph.tex', 'a') as graphs_file:
            graphs_file.write(bar_graph_tex[0])
            graphs_file.write(title)
            graphs_file.write(bar_graph_tex[1])
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
    
            with open(self.work_dir + '/graph.tex', 'a') as graphs_file:
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
    
    
    def compile_tex(self):
        """Calls graph functions based on what is found in config file"""
        print('Starting PfaudSec Graph compiler.\nLoaded columns from '\
                + str(self.config_file) + ':\n')
        
        # Totals from date column
        if self.config.getboolean('document', 'show_totals', fallback=False):
            self.totals_by_month_graph(title = str(self.config.get\
                    ('document', 'document_name', fallback = 'Totals')))
    
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

        #TODO call xelatex somewhere in here, copy pdf, then return location of pdf from this function
    
class SharePoint(object):

    def __init__(self):
        #check is the session files exists
        self.sp_url = 'pfaudlerazuread.sharepoint.com'

        if os.path.isfile(config_folder + '/sp-session.pkl'):
            self.session = sharepy.load(config_folder + '/sp-session.pkl')
            #self.session.raise_for_status()
        else:
            self.session = sharepy.connect(self.sp_url, *self.get_cred())
            self.session.save(config_folder + '/sp-session.pkl')


    def get_cred(self):
        """Returns packed login credentials
        
        use *self.get_cred() as input to function
        asking for two variables"""
        #import sp_prompt
        class Prompt(QtWidgets.QDialog, sp_prompt.Ui_Dialog):
            def __init__(self):
                super(Prompt, self).__init__()
                self.setupUi(self)
        prompt = Prompt()
        prompt.exec_()
        return prompt.lineEdit.text(), prompt.lineEdit_2.text() 

    def upload(self, filename):
        pass

class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        self.menu = QtWidgets.QMenu(parent)

        checkAction = self.menu.addAction("Compile TeX")
        checkAction.triggered.connect(self.sp)

        exitAction = self.menu.addAction("Exit")
        exitAction.triggered.connect(QtWidgets.qApp.quit)

        self.setContextMenu(self.menu)
        self.activated.connect(self.tray_clicked)
        self.click_timer = QtCore.QTimer(self)
        self.click_timer.setSingleShot(True)
        self.click_timer.timeout.connect(self.single_click)

        #Used in write() for sys.stdout
        self.print_queue = []
        self.time_stamp = ''
        self.time_format_str = '%H:%M:%S: '

    def flush(self, *arg, **args):
        """Used only to suppress errors"""
        pass

    def write(self, text):
        """sys.stdout directed to a system tray message"""
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
        queue_timer.start(9000)
        self.showMessage('PfaudSec spreadsheet:', '\n'.join([str(i) for i in self.print_queue]))

    def clear_queue_line(self):
        try:
            del self.print_queue[0]
        except IndexError:
            pass

    def sp(self):
        instance = SharePoint()
        instance.upload('testfile')

    def tray_clicked(self, reason):

        if reason == QtWidgets.QSystemTrayIcon.Trigger:
            self.click_timer.start(QtWidgets.qApp.doubleClickInterval())

        elif reason == QtWidgets.QSystemTrayIcon.DoubleClick:
            self.click_timer.stop()
            self.double_click()

    def double_click(self):
        print('double click')

    def single_click(self):
        print('single click')

    def make_ready(self):
        self.showMessage('PfaudSec', 'Compiling graph')
        for i in range(3):
            with tempfile.TemporaryDirectory(prefix='PfaudSec_') as work_dir:
                k = Grapher(work_dir, './car_log.xlsx')
                k.compile_tex()



sys.excepthook = except_box
app = QtWidgets.QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)
icon = QtGui.QIcon('resource/logo.ico')  # need a icon
config_folder = appdirs.user_config_dir('PfaudSec', 'PfaudSec')
folder_check(config_folder)
print(config_folder)

work_file = './car_log.xlsx'

trayIcon = SystemTrayIcon(icon)
trayIcon.show()
sys.stdout = trayIcon

sys.exit(app.exec_())

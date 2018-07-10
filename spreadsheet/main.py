from openpyxl import load_workbook
from openpyxl.utils import column_index_from_string #,coordinate_from_string
from collections import Counter
import datetime
import dateutil.relativedelta
import itertools
import configparser
import os

#pgfplots tex file stored as list in a python file
from texstorage import line_graph_tex, bar_graph_tex 

class Grapher(object):

    now = datetime.date.today()

    def __init__(self, work_dir, work_file):
        self.work_dir = work_dir

        self.work_file = './car_log.xlsx'
        #self.wb = load_workbook(work_file)
        self.config_file = self.work_dir + self.filename_noext(self.work_file) + '.ini'
        self.config = configparser.ConfigParser()
        try:
            with open(self.config_file) as f:
                self.config.read_file(f)
        except IOError:
            #Put config maker here
            #app.setQuitOnLastWindowClosed(False)
            print('no config file for this workbook')
            exit()

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
    
    
    def filename_noext(self, filename):
        return filename.split('/')[len(filename.split('/')) - 1].rsplit(".", 1)[0]
    
    
    
    
    
    
    
    
    
    # Determines global active rows by first date and last date in input column
    def date_cell_range(self, column):
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
    
    
    # Run this to set global active cells
    #cells_start, cells_end = date_cell_range(date_column)
    #active_range = range(int(cells_start), int(cells_end))
    
    
    # For readability, returns a list of all cell.value
    # for input column, range determined by date_cell_range()
    def column_list(self, column):
        row_cells = []
        for i in self.ws[column + self.cells_start : column + self.cells_end]:
            for cell in i:
                row_cells.append(cell.value)
        return row_cells
    
    
    # returns month as string
    def month_string(self, i):
        out = None
        if isinstance(i, datetime.datetime) or isinstance(i, datetime.date):
            out = i.strftime('%b %y')
        else:
            print('Cant convert ' + str(type(i)) + ' to month string')
        return out
    
    
    # enumerate() but index starts at first cell
    # as determined by date_cell_range()
    def cell_enumerate(self, item):
        i = int(self.cells_start)
        it = iter(item)
        while True:
            yield (i, it.__next__())
            i += 1
    
    
    def unique_column_list(self, column):
        values = list(set(self.column_list(column)))
        values.sort
        return values
    
    
    def diff_month(self, d1, d2):
        return (d1.year - d2.year) * 12 + d1.month - d2.month
    
    
    # Totals for input column for this month
    def curr_month_values(self, column, blanks=False):
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
        return self.month_string(self.now 
                - dateutil.relativedelta.relativedelta(\
                        months=int(relative_month)))
    
    
    def totals_by_month_graph(self, months=12, title='Totals by month'):
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
    
    
    # returns dict of tuples, tuple index is how many months ago data is for
    def values_by_month(self, column, months=12):
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
        try:
            for r in self.ws[column + '1' : column + str(len(self.ws[column]))]:
                for cell in r:
                    if cell.value != None:
                        return True
        except:
            return False
        return False
    
    
    def compile_tex(self):
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
    
graph = Grapher('./', './car_log.xlsx')
graph.compile_tex()

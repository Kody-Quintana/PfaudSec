from openpyxl import load_workbook
from openpyxl.utils import coordinate_from_string,column_index_from_string
from collections import Counter, OrderedDict
import datetime
import dateutil.relativedelta
import itertools

#pgfplots tex file stored as list in a python file
from texstorage import line_graph_tex, bar_graph_tex 

#Variables to be determined by ui later
work_file = './car_log.xlsx'
date_column = 'b'
work_dir = './'

wb = load_workbook(work_file)
ws = wb.worksheets[0]
now = datetime.date.today()

# Determines global active rows by first date and last date in input column
def date_cell_range(date_column):
    last_date_cell = None
    first_date_cell = None
    last_date_counter = 0

    for r in ws[date_column + str(1)\
            :\
            date_column + str(len(ws[date_column]))\
            ]:
        for cell in r:
            last_date_counter = last_date_counter + 1
            if cell.value != None:
                if isinstance(cell.value, datetime.datetime):
                    last_date_cell = last_date_counter
                    if first_date_cell == None:
                        first_date_cell = last_date_counter

    return(str(first_date_cell), str(last_date_cell))


# Run this to set global active cells
cells_start, cells_end = date_cell_range(date_column)
active_range = range(int(cells_start), int(cells_end))

# For readability, returns a list of all cell.value
# for input column, range determined by date_cell_range()
def column_list(column):
    row_cells = []
    for i in ws[column + cells_start : column + cells_end]:
        for cell in i:
            row_cells.append(cell.value)
    return row_cells

# returns month as string
def month_string(i):
    out = None
    if isinstance(i, datetime.datetime) or isinstance(i, datetime.date):
        out = i.strftime('%b %y')
    else:
        print('Cant convert ' + str(type(i)) + ' to month string')
    return out

# enumerate() but index starts at first cell
# as determined by date_cell_range()
def cell_enumerate(item):
    i = int(cells_start)
    it = iter(item)
    while True:
        yield (i, it.__next__())
        i += 1




def unique_column_list(column):
    values = list(set(column_list(column)))
    values.sort
    return values

def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month


# Totals for input column for this month
def curr_month_values(column, blanks=False):
    this_month = []
    total_occurances = 0
    for i, j in cell_enumerate(column_list(column)):
        date_cell = ws.cell(i,column_index_from_string(date_column)).value

        if blanks == False and str(j) == 'None':
            continue #Skips blank cells

        if date_cell.month == now.month\
                and date_cell.year == now.year:
            this_month.append(j)
            total_occurances  += 1
    return Counter(this_month), total_occurances

def relative_month_to_string(relative_month):
    output = month_string(now 
            - dateutil.relativedelta.relativedelta(\
                    months=int(relative_month)))
    return output


def totals_by_month_graph(column=date_column, months=12, title='Totals by month'):
    months_counter = [0] * months
    return_dict = {}
    symbolic_xcoords = [] # turns into string later
    coordinates = []
    ticks_distance_flag = 0

    for index, data in reversed(list(cell_enumerate(column_list(date_column)))):
        column_value = ws[column + str(index)].value #This must be str to allow sorted()
        months_ago = diff_month(now, column_value)
        if months_ago > (months - 1):
            break
        months_counter[months_ago] += 1

    for i in months_counter:
        if int(i) > 5:
            ticks_distance_flag = 1

    for index, data in reversed(list(enumerate(months_counter))):
        xcoord_name = relative_month_to_string(index)
        coordinates.append('(' + xcoord_name + ',' + str(data) + ')')
        symbolic_xcoords.append(xcoord_name + ',')

    symbolic_xcoords = '\n'.join([str(i) for i in symbolic_xcoords])
    coordinates = '\n'.join([str(i) for i in coordinates])

    with open(work_dir + '/graph.tex', 'a') as graphs_file:
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
def values_by_month(column, months=12):
    catagories_index = {} #dict to get index from string for catagories
    catagories = []       #list of lists for each catagory
    return_dict = {}
    for k, i in reversed(list(cell_enumerate(column_list(date_column)))):
        column_value = str(ws[column + str(k)].value) #This must be str to allow sorted()
        months_ago = diff_month(now, i)
        if months_ago > (months - 1):
            break
        if column_value not in catagories_index:
            catagories_index[column_value] = len(catagories_index)
            catagories.append([0] * months) #index is how many months ago
        catagories[catagories_index.get(column_value)][months_ago] += 1
    
    for i in catagories_index:
        return_dict[i] = tuple(catagories[catagories_index.get(i)])
    return(return_dict)



def current_month_graph(column, title, blanks=False):
    current_data, total_occurances = curr_month_values(column, blanks)

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


    with open(work_dir + '/graph.tex', 'a') as graphs_file:
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
def monthly_graph(column, title, months=12, blanks=False):
    for catagory, month_count_tuple in sorted(values_by_month(column, months).items()):

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

            xcoord_month = relative_month_to_string(relative_month)

            #for use in LaTeX pgfplots package
            symbolic_xcoords.insert(0, xcoord_month + ',')
            coordinates.insert(0, '(' + xcoord_month + ',' + str(occurances) + ')')

        #lists changed to str with newlines to avoid using a loop to append to tex file
        symbolic_xcoords = '\n'.join([str(i) for i in symbolic_xcoords])
        coordinates = '\n'.join([str(i) for i in coordinates])

        with open(work_dir + '/graph.tex', 'a') as graphs_file:
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


totals_by_month_graph(title='Total CARs by Month')
current_month_graph('I', 'Item Type')
monthly_graph('I', 'Item Type')
#monthly_graph('N', 'column N values')
current_month_graph('J', 'Root Cause')
monthly_graph('N', '')
current_month_graph('O', 'Action taken')
monthly_graph('L', 'Dept Responsible')




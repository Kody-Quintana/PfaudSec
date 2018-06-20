from openpyxl import load_workbook
from openpyxl.utils import coordinate_from_string,column_index_from_string
from collections import Counter, OrderedDict
import datetime

#Variables to be determined by ui later
work_file = './car_log.xlsx'
date_column = 'b'

wb = load_workbook(work_file)
ws = wb.worksheets[0]

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
    if isinstance(i, datetime.datetime):
        out = i.strftime('%B')
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

# Totals for input column for this month
def curr_month_values(column):
    this_month = []
    for i, j in cell_enumerate(column_list(column)):
        date_cell = ws.cell(i,column_index_from_string(date_column)).value
        now = datetime.date.today()
        if date_cell.month == now.month\
                and date_cell.year == now.year:
            this_month.append(j)
    return Counter(this_month)

print(curr_month_values('L'))


def unique_column_list(column):
    values = list(set(column_list(column)))
    values.sort
    print(values)

unique_column_list('I')


ini_document = """
;   _____   __                _  _____           
;  |  __ \ / _|              | |/ ____|          
;  | |__) | |_ __ _ _   _  __| | (___   ___  ___ 
;  |  ___/|  _/ _` | | | |/ _` |\___ \ / _ \/ __|
;  | |    | || (_| | |_| | (_| |____) |  __/ (__ 
;  |_|    |_| \__,_|\__,_|\__,_|_____/ \___|\___|
;                                                
; Spreadsheet document example config:
;
; <-- Comment character (all text after will be ignored)
;
; [document]        <-- document information section (only one per ini file)
; worksheet = 1     <-- which worksheet contains the information
; date_column = B   <-- which column has the entry dates
; show_totals = yes <-- create a totals graph
; 
; [I]                 <-- column info section (many per ini file)
; title = Item Type   <-- title of graphs for this column
; monthly = yes       <-- monthly line graph
; current_month = yes <-- bar/pareto graph for current month only
"""

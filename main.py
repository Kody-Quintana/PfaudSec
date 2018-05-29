import subprocess
import tempfile
import os
import shutil
import configparser

embed_list = []
nested_list_sections = []

config_file = 'sections_config.ini'
#xelatex_path = 'xelatex'
xelatex_path = input('Enter path to xelatex: ')
#work_dir = './work'
output_dir = './output'
grab_dir = './tempemb'
template_dir = './TeX'

#change to contextlib later

def resource_path(relative_path):
    #Get absolute path to resource, works for dev and for PyInstaller
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

with tempfile.TemporaryDirectory() as work_dir:

    config = configparser.ConfigParser()
    config.read(config_file)
    print('\nLoaded sections from ' + str(config_file) + ':')
    for i in config.sections():
        print('Section: ' + str(i))
    print('\n')
    
    
    def get_file_list(ext,dir):
        list = []
        for i in os.listdir(dir):
            if i.endswith(ext):
                list.append(i)
        return list
    
    def pdf_rename():
        global nested_list_sections
        global embed_list
    
        for l in range(len(config.sections())): 
            # -1 from actual length but configparser makes a DEFAULT section that is not used so the -1 is fine
            nested_list_sections.append([])
    
        for i, k in enumerate((get_file_list('pdf',grab_dir))):
            if (' ' in k):
    
                #Splits document shorthand, removes leading 0s so that 2.1 is same as 2.01
                doc_id_stage = k.split(' ')[1].replace('.pdf','').split('.')
                doc_id = doc_id_stage[0] + '.' + doc_id_stage[1].lstrip('0')
                
                if doc_id[0].isdigit():
    
                    section_num = int(doc_id[0]) - 1
                    shutil.copy(grab_dir + '/' + k, work_dir)
                    doc_section = (config[config.sections()[section_num]][doc_id])
                    new_name = doc_section.replace(' ','!') + '.pdf' 
                    new_full_name = work_dir + '/' + new_name
                    os.rename(work_dir + '/' + k, new_full_name)
                    nested_list_sections[section_num].append(new_name)
                    
        for i in nested_list_sections:
            print(i)
    
        for i in range(len(nested_list_sections)):
            if nested_list_sections[i]:
                embed_list.append(r'\addsection{' + str(config.sections()[i]) + '}')
                for k in nested_list_sections[i]:
                    embed_list.append(r'\addpage{' + k + '}')
        
        with open(work_dir + '/embedlist.tex', 'w') as embed_list_file:
            for i in embed_list:
                embed_list_file.write('%s\n' % i)
        embed_list_file.close()
    
    for i in embed_list:
        print(i)
    
    def template_stage(src,dest):
        
        folder_check(dest)
        print('\nWorking directory: ' + str(work_dir))
    
        shutil.copytree(template_dir + '/font/',dest + '/font/')
    
        for i in os.listdir(src):
            if i.endswith('.tex'):
                shutil.copy(src + '/' + i,dest)

    
    def embed_stage(src,dest):
    
        folder_check(dest) 
        for i in os.listdir(src):
            if i.endswith('.pdf'):
                shutil.copy(src + '/' + i,dest)
                print (i)    
    
    
    def compile_TeX(path,texfile):
        for _ in range(2):
            p = subprocess.Popen([path, '-recorder', texfile], cwd=work_dir)
            p.wait()

    
    def folder_check(folder):
        if not os.path.exists(folder):
            os.mkdir(folder)

   
    def job_info():
        data_file = ['mo = 1234567', 'serial = 12345', 'equipment = RA-24 thing', 'customer = SomeCorp']

        with open(work_dir + '/jobinfo.dat', 'w') as job_info_file:
            for i in data_file:
                job_info_file.write('%s\n' % i)
        job_info_file.close()


    def output_pdf(output_path):
        folder_check(output_path)
        print('\nOutput directory: ' + str(output_path))
        shutil.copy(work_dir + '/databook.pdf', output_path)


    template_stage(template_dir, work_dir)
    pdf_rename()
    job_info()
    compile_TeX(xelatex_path,'databook') 
    output_pdf(output_dir)

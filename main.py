import os
import shutil
import configparser

embed_list = []
nested_list_sections = []

config = configparser.ConfigParser()
config.read('sections_config.ini')
print(config.sections())

for i, k in enumerate(config):

    print ('i is: ' + str(i))
    print ('k is: ' + str(k))

work_dir = './work'
output_dir = './output'
grab_dir = './tempemb'
template_dir = './TeX'

def GetFileList(ext,dir):
    list = []
    for i in os.listdir(dir):
        if i.endswith(ext):
            list.append(i)
    return list

def PdfRename():
    global nested_list_sections
    global embed_list
    for l in range(len(config.sections())): 
        # -1 from actual length but configparser makes a DEFAULT section that is not used so the -1 is fine
        nested_list_sections.append([])

    for i, k in enumerate((GetFileList('pdf',grab_dir))):
        if (' ' in k):
            id = k.split(' ')[1].replace('.pdf','')
            if id[0].isdigit():

                section_num = int(id[0]) - 1
                shutil.copy(grab_dir + '/' + k, work_dir)
                new_name = (config[config.sections()[section_num]][id]) + '.pdf' 
                new_full_name = work_dir + '/' + (config[config.sections()[section_num]][id]) + '.pdf' 
                os.rename(work_dir + '/' + k, new_full_name)
                nested_list_sections[section_num].append(new_name)
                
    for i in nested_list_sections:
        print(i)
    for i in range(len(nested_list_sections)):
        if nested_list_sections[i]:
            embed_list.append(r'\addsection{' + str(config.sections()[i]) + '}')
            for k in nested_list_sections[i]:
                embed_list.append(r'\addpage{' + k + '}')
            
PdfRename()
for i in embed_list:
    print(i)

def TemplateStage(src,dest):
    
    if not os.path.exists(dest):
        os.mkdir(dest)
    
    #os.mkdir(dest + '/font/')
    shutil.copytree(template_dir + '/font/',dest + '/font/')

    for i in os.listdir(src):
        if i.endswith('.tex'):
            shutil.copy(src + '/' + i,dest)

def EmbedStage(src,dest):

    if not os.path.exists(dest):
        os.mkdir(dest)

    for i in os.listdir(src):
        if i.endswith('.pdf'):
            shutil.copy(src + '/' + i,dest)
            print (i)
    


def CompileTeX(bin,texfile):
    pass

def folder_check(folder):
    if not os.path.exists(folder):
        os.mkdir(folder)

#TemplateStage(template_dir, work_dir)
#EmbedStage(grab_dir, work_dir)
#
#print(grab_dir,work_dir)



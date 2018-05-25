import os
import shutil
import configparser

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
    nested_list_sections = []

    for l in range(len(config.sections())):
        nested_list_sections.append([])

    for i, k in enumerate((GetFileList('pdf',grab_dir))):
        if (' ' in k):
            id = k.split(' ')[1].replace('.pdf','')
            if id[0].isdigit():
                print('is is valid')

                print (id[0])
                print (k + ' is ' + id)
    print(nested_list_sections)

PdfRename()


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



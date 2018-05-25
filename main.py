import os
import shutil



work_dir = './work'
output_dir = './output'
grab_dir = './tempemb'
template_dir = './TeX'

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

TemplateStage(template_dir, work_dir)
EmbedStage(grab_dir, work_dir)

print(grab_dir,work_dir)


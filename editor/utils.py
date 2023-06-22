import os
from base.functions import get_templates_directory

def folder_tree(root_directory):
    items = []

    for item in os.listdir(root_directory):
        folder = {}

        root_path = os.path.join(root_directory,item)

        if(os.path.isfile(root_path)):
            folder.update({'name':item,'path':root_path,'is_folder':False})
        else:
            sub_folders = []

            for sub_folder in os.listdir(os.path.join(root_directory,item)):
                path = os.path.join(os.path.join(root_directory,item),sub_folder)

                if os.path.isdir(path):
                    sub_folders.append({'name':sub_folder,'path':path,'items':folder_tree(path),'is_folder':True})
                    
                else:
                    sub_folders.append({'name':sub_folder,'path':path,'is_folder':False})
            
            folder.update({'name':item,'path':root_path,'items':sub_folders,'is_folder':True})

        items.append(folder)

    return items

def display_tree(path):
    folder = {}

    if os.path.isdir(path):
        folder.update({'name':os.path.basename(path),'path':path,'items':reversed(folder_tree(path)),'is_folder':True})
    else:
        folder.update({'name':os.path.basename(path),'path':path,'is_folder':False})

    return folder
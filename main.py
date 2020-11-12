import os
import re

project_root = os.getcwd()

def find_all_quotes(query):
    query = sanitate_query(query)
    sub_dirs = find_folders_with_subs()
    quotes = []
   
    for dir in sub_dirs:
        print(dir)
        for file in os.listdir(dir):
            find_quotes_in_transcript(query, )
    
    return quotes


def find_quotes_in_transcript(query, file_path):
    pass


def return_to_root():
    move_to_folder()


def move_to_folder(root=project_root, folder_name=""):
    path = f"{root}\\{folder_name}" if folder_name != "" else f"{root}"
    try:
        os.chdir(path)
    except OSError:
        print(f"Invalid target path - '{path}'")


def find_folders_with_subs(root=os.getcwd(), strict=True):
    subtitle_dirs = []
    check = all if strict else any

    
    for dir_path, dir_names, file_names in os.walk(root):
        if any(sub_dir.startswith(".") for sub_dir in dir_path.split("\\")):
            continue
        
        if check(f.endswith(".srt") for f in file_names):
            subtitle_dirs.append(dir_path)
   
    return subtitle_dirs


def sanitate_query(query):
    return re.sub("[^a-zA-Z0-9 ]+", "", query).strip()


def calc_match_confidence(query, line_extract):
    pass
import os
import re
from quote import Quote

project_root = os.getcwd()
video_root = project_root + "\\Video"
subtitles_root = project_root + "\\Subtitles"

def find_all_quotes(query):
    query = sanitate_query(query)
    subtitle_dirs = find_folders_with_subs()
    
    for dir in subtitle_dirs:
        for file in os.listdir(dir):
            quotes = find_quotes_in_transcript(query, dir+"\\"+file)
             

    return quotes


def find_quotes_in_transcript(query, file_path):
    quotes = []
    with open(file_path, "r") as f:
        line_generator = ((l.strip() if l!="\n" else "\n") for l in f.readlines())
        line = next(line_generator, -1)
        while True: #?
            if line == -1:
                break
            
            if line == "\n":
                line = next(line_generator, -1) 
                continue
            
            timestamp = next(line_generator)
            start_timestamp, end_timestamp = timestamp.split(" --> ")

            quote = ""
            line = next(line_generator)
            while line != "\n":
                quote += " " + line
                line = next(line_generator)

            quotes.append(Quote(path=file_path, text=quote, 
                          start_timestamp=start_timestamp, end_timestamp=end_timestamp))
    return quotes

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
    
    for dir_path, dir_names, file_names in os.walk(root+"\\Subtitles"):
        if dir_path == root+"\\Subtitles":
            continue
        if check(f.endswith(".srt") for f in file_names):
            subtitle_dirs.append(dir_path)
   
    return subtitle_dirs


def sanitate_query(query):
    words = re.sub("[^a-zA-Z0-9 ]+", " ", query).strip().split(' ') 
    return words #[w for w in words if len(w) > 1]
   

def extract_line():
    pass


def calc_sentence_query_match(query, line_extract):
    pass


def calc_query_sentence_match(query, line_extract):
    pass

find_all_quotes("")
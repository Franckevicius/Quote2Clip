import os
os.getcwd()
os.listdir()

def move_to_folder(folder_name, root=os.getcwd()):
    try:
        os.chdir(f"{root}\\{folder_name}")
    except OSError:
        print(f"Invalid target path - '{root}\\{folder_name}'")

def find_folders_with_sub_files(root=os.getcwd(), strict=False):
    subtitle_dirs = []
    check = all if strict else any
    for dir_path, dir_names, file_names in os.walk(root):
        if check(f.endswith(".srt") for f in file_names):
            subtitle_dirs.append(dir_path)
    return subtitle_dirs
import os
import sys
import re
from quote import Quote
from cut_video import cut_clip


def find_all_quotes(project_root, query, best_count):
    query_words = sanitize_text(query)
    subtitle_dirs = find_folders_with_subs(project_root)
    quotes = []

    for dir in subtitle_dirs:
        for file in os.listdir(dir):
            quotes += find_quotes_in_transcript(query_words, f"{dir}\\{file}")
             
    quotes = sorted(quotes, key=lambda q:(q.query_quote_match, q.quote_query_match), reverse=True)    
    return quotes[:best_count]


def find_quotes_in_transcript(query_words, file_path):
    quotes = []

    with open(file_path, "r") as f:
        all_lines = ((l.strip() if l!="\n" else "\n") for l in f.readlines())
        line = next(all_lines, -1)
        while line != -1:             
            if line == "\n":
                line = next(all_lines, -1) 
                continue
            
            quote_index = int(line)
            start_timestamp, end_timestamp = next(all_lines).split(" --> ")

            quote = ""
            line = next(all_lines)
            while line != "\n":
                quote += " " + line
                line = next(all_lines)

            quote_words = sanitize_text(quote)
            quotes.append(Quote(path=file_path, text=quote, index=quote_index,
                                start_timestamp=start_timestamp, end_timestamp=end_timestamp,
                                quote_query_match=calc_quote_query_match(query_words, quote_words),
                                query_quote_match=calc_query_quote_match(query_words, quote_words)))
    
    return quotes


def find_folders_with_subs(root, strict=True):
    subtitle_dirs = []
    check = all if strict else any
    
    for dir_path, dir_names, file_names in os.walk(root+"\\Subtitles"):
        if dir_path == root+"\\Subtitles":
            continue
        if check(f.endswith(".srt") for f in file_names):
            subtitle_dirs.append(dir_path)
   
    return subtitle_dirs


def sanitize_text(text):
    words = re.sub("[^a-zA-Z0-9 ]+", " ", text).strip().split(" ") 
    return [w.lower() for w in words if len(w) > 0]
   

def calc_quote_query_match(query_words, quote_words):
    return len(set(query_words) & set(quote_words)) / len(set(quote_words))


def calc_query_quote_match(query_words, quote_words):  
    return len(set(query_words) & set(quote_words)) / len(set(query_words))


def clear_output_folder(output_root):
    for file in os.listdir(output_root):
        os.remove(f"{output_root}{file}")


def find_quote_last_index(quote:Quote):
    with open(quote.path, "r") as f:
        lines_reversed = [(l.strip() if l!="\n" else "\n") for l in f.readlines()][::-1]
        last_index = lines_reversed[lines_reversed.index("\n", 2) - 1]
   
    return int(last_index)


def add_context(quote:Quote, context_size):
    if context_size < 0:
        context_index = max(1, quote.index+context_size)
    elif context_size > 0:
        context_index = min(find_quote_last_index(quote), quote.index+context_size)
    if context_size == 0 or context_index == quote.index:
        return

    with open(quote.path, "r") as f:
        all_lines = ((l.strip() if l!="\n" else "\n") for l in f.readlines())
        line = next(all_lines)
        
        while line != str(min(quote.index, context_index)):
            line = next(all_lines)

        start_timestamp, _ = next(all_lines).split(" --> ")
        quote.start_time = quote.calc_second_stamp(start_timestamp)

        while line != str(max(quote.index, context_index)):
            line = next(all_lines)

        _, end_timestamp = next(all_lines).split(" --> ")
        quote.end_time = quote.calc_second_stamp(end_timestamp)


def main(args):
    if len(args) == 0:
        print("No args passed. Check the .readme for usage instructions")
        return
    
    query = args[0]
    best_count = 1 if len(args) < 2 else int(args[1])
    context_size = 0 if len(args) < 3 else int(args[2])
    project_root = os.getcwd()
    video_root = project_root + "\\Video\\"
    subtitles_root = project_root + "\\Subtitles\\"
    output_root = project_root + "\\Output\\"
    clear_output_folder(output_root)
    
    for i, q in enumerate(find_all_quotes(project_root, query, best_count)):
        video_input_path = re.sub(r"\\Subtitles", r"\\Video", q.path)
        video_input_path = re.sub(".srt", ".mkv", video_input_path)
        output_path = f"{output_root}{i}.mkv"
        add_context(q, context_size)
        cut_clip(video_input_path, output_path, q.start_time, q.end_time)

if __name__ == "__main__":
    main(sys.argv[1:])
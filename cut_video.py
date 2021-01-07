import ffmpeg
import os
import main

def calc_second_stamp(timestamp):
    times_split = timestamp.replace(",", ":").split(":")
    times_split = [int(time) for time in times_split]
    hours, minutes, seconds, milliseconds = times_split

    seconds_count = seconds + 60 * minutes + 3600 * hours
    return f"{seconds_count}.{milliseconds}"

start_s = calc_second_stamp("00:03:37,600")
end_s = calc_second_stamp("00:03:40,000")
print(start_s, end_s)

#input = ffmpeg.input("C:\Workarea\Programming\Python\Quote2Clip\Video\F02\202 - Mars University.mkv")
#input_video = ffmpeg.trim(input, start_frame=frame_start, end_frame=frame_end)

def cut_clip(input_path, output_path, start="00.000", end="00.000"):
    input_stream = ffmpeg.input(input_path)

    video = (
        input_stream.video
        .trim(start=start, end=end)
    )
    audio = (
        input_stream.audio
        .filter_('atrim', start=start, end=end)
    )

    joined = ffmpeg.concat(video, audio, v=1, a=1).node
    output = ffmpeg.output(joined[0], joined[1], output_path)
    output.run()

cut_clip(input_path="C:\\Workarea\\Programming\\Python\\Quote2Clip\\Video\\F02\\202 - Mars University.mkv",
     output_path="C:\\Workarea\\Programming\\Python\\Quote2Clip\\Output\\test.mkv",
     start=start_s, end=end_s)
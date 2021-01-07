import ffmpeg
import os

def cut_clip(input_path, output_path, start="00.000", end="00.000"):
    input_stream = ffmpeg.input(input_path)

    video = (
        input_stream.video
        .trim(start=start, end=end)
        .setpts('PTS-STARTPTS')
    )
    audio = (
        input_stream.audio
        .filter_('atrim', start=start, end=end)
        .filter_('asetpts', 'PTS-STARTPTS')
    )

    joined = ffmpeg.concat(video, audio, v=1, a=1).node
    output = ffmpeg.output(joined[0], joined[1], output_path)
    output.run()
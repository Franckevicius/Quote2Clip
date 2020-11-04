class Quote:
    def __init__(self, text, start_timestamp, end_timestamp, framerate):
        self.text = text
        self.start_frame = self.calc_frame(start_timestamp, framerate)
        self.end_frame = self.calc_frame(end_timestamp, framerate)

    def __str__(self):
        return "\n".join([self.text, str(self.start_frame), str(self.end_frame)])

    def calc_frame(self, timestamp, framerate):
        times_split = timestamp.replace(",", ":").split(":")
        times_split = [int(time) for time in times_split]
        hours, minutes, seconds, milliseconds = times_split

        seconds = seconds + 60 * minutes + 3600 * hours
        return seconds*framerate + milliseconds*framerate//1000
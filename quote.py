class Quote:
    def __init__(self, path, text, start_timestamp, end_timestamp):
        self.path = path
        self.text = text
        self.start_time = self.calc_second_stamp(start_timestamp)
        self.end_time = self.calc_second_stamp(end_timestamp)
        self.sentence_match = 0
        self.quote_match = 0
        

    def __str__(self):
        return "\n".join([self.text, str(self.start_time), str(self.end_time)])


    def calc_second_stamp(self, timestamp):
        times_split = timestamp.replace(",", ":").split(":")
        times_split = [int(time) for time in times_split]
        hours, minutes, seconds, milliseconds = times_split

        seconds_count = seconds + 60 * minutes + 3600 * hours
        return f"{seconds_count}.{milliseconds}"
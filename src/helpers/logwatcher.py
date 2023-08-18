import traceback
import tailer
import time
from re import search
import re
from langdetect import detect, LangDetectException


class Static:
    lang = {
        "en": "ENG",
        "fr": "FRE",
        "de": "GER",
        "pt": "POR",
        "es": "SPA",
        "ru": "RUS",
        "th": "THA",
        "ko": "KOR",
        "zh-cn": "TWN"
    }


class LogWatcher:
    def __init__(self, processor=None, test=False, log_file=None, regex_log='', callback=None, slain_regex=''):
        self.callback = callback if callback else print
        self.kill_pill = False
        self.test = test
        self.log_file = log_file
        self.regex_log = regex_log
        self.lang = "ENG"
        self.slain_regex = slain_regex
        self.processor = processor if processor else self._process_line

    def destroy(self):
        self.kill_pill = True

    def watch_log(self):
        # Check encoding on file
        print("Starting log watcher")
        try:
            with open(self.log_file, 'rb') as file:
                pass
                # print("opened")
                # enc = chardet.detect(file.read())
                # print(enc)
        except FileNotFoundError:
            print("Log file not found.")
            return
        # Follow the file as it grows
        t = tailer.Tailer(open(self.log_file, encoding="utf-8"), end=False)

        t.seek_end() if not self.test else t.seek(0)
        trailing = True

        while not self.kill_pill:
            where = t.file.tell()
            line = t.file.readline()
            if line:
                if trailing and line in t.line_terminators:
                    trailing = False
                    time.sleep(0.1)
                    continue

                if line[-1] in t.line_terminators:
                    line = line[:-1]
                    if line[-1:] == '\r\n' and '\r\n' in t.line_terminators:
                        line = line[:-1]

                trailing = False
                match = search(self.regex_log, line)
                if match and match.group(5).startswith("INFO Client"):
                    data = self.processor( match.group(6) )
                    if data:
                        self.callback( data )

            else:
                trailing = True
                t.seek(where)
                time.sleep(1)

    @staticmethod
    def _split_guild(combined):
        guild = ""
        name = ""
        if combined.startswith("<"):
            guild = combined.split("> ", 1)[0].lstrip("<")
            name = combined.split("> ", 1)[1]
        else:
            name = combined.strip()

        return guild, name

    def _process_line(self, line):
        try:
            lang_detected = detect(line)
        except LangDetectException:
            lang_detected = "ENG"
        lang_detected = Static.lang[lang_detected] if lang_detected in Static.lang else "ENG"  # default english for reasons
        # print(line)
        try:
            match = re.search(self.slain_regex, line)
            if match:
                print("Player Slain - Calling back")
                self.callback(line)
        except Exception as e:
            print(traceback.format_exc())

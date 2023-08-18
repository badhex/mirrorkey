import re
from threading import Thread
from helpers.logwatcher import LogWatcher
from helpers.keysender import KeySender

log_file = """E:\\Games\\Grinding Gear Games\\Path of Exile\\logs\\Client.txt"""
debug = False
game_name = "Path of Exile"
key_sender = None


def send_hotkey(line):
    key_sender.shortcut()
    print(line, "Pressing CTRL+SHIFT+F10")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    log_watcher = LogWatcher(
        log_file=log_file,
        test=debug,
        regex_log=re.compile("""^([\d\/]*) ([\d:]*) ([\da-f]*) ([\da-f]*) \[(.*)\] (.*)$"""),
        slain_regex=re.compile("""^(.*) has been slain\."""),
        callback=send_hotkey)

    key_sender = KeySender(window_name=game_name)

    threads = [Thread(target=log_watcher.watch_log),
               Thread(target=key_sender.main_loop)]

    # start the threads
    for thread in threads:
        thread.daemon = True
        thread.start()

    while True:
        pass

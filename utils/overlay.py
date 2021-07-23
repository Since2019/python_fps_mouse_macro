import argparse
import time
import game_overlay_sdk
import game_overlay_sdk.injector
import threading
import logging


logging.basicConfig(filename='test.log', level=logging.WARNING)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
overlay_log_handler = game_overlay_sdk.injector.OvelrayLogHandler()
formatter = logging.Formatter('%(levelname)s:%(message)s')
overlay_log_handler.setFormatter(formatter)
logger.addHandler(overlay_log_handler)


class MessageThread (threading.Thread):

    def __init__(self):
        super(MessageThread, self).__init__()
        self.need_quit = False

    def run(self):
        i = 0
        while not self.need_quit:
            logger.info('Hi from python OverlayLogHandler %d' % i)
            i = i + 1
            time.sleep(1)


def main():
    exe_path = "E:\\Uplay\\Ubisoft Game Launcher\\games\\Tom Clancy's Rainbow Six Siege\\RainbowSix.exe"
    exe_args = ""
    steam_app_id = "359550"

    game_overlay_sdk.injector.enable_monitor_logger()
    game_overlay_sdk.injector.run_process(exe_path, exe_args, steam_app_id)

    # start sending messages to overlay
    thread = MessageThread()
    thread.start()
    input("Press Enter to stop...")
    thread.need_quit = True
    thread.join()

    game_overlay_sdk.injector.release_resources()


if __name__ == "__main__":
    main()

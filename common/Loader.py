import shutil
from itertools import cycle
from os import get_terminal_size
from threading import Thread
from time import sleep


class Loader:
    def __init__(self):
        self._done = False
        # self._steps = ["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]
        self._steps = ["▁", "▂", "▃", "▄", "▅", "▆", "▇", "█", "▇", "▆", "▅", "▄", "▃", "▁"]
        self._timeout = 0.1
        self._desc="Loading..."
        self._end="Done!"
        self._progress = 0
        self._thread = Thread(target=self._animate, daemon=True)

    def start(self):
        self._thread.start()
        return self

    def _animate(self):
        for c in cycle(self._steps):
            if self._done:
                break
            print(f"\r{c} {self._desc}", flush=True, end="")
            sleep(self._timeout)

    def __enter__(self):
        self.start()

    def progress(self, value):
        self._progress = value
        self._desc = f"Loading... {self._progress}%"

    def stop(self):
        self._done = True
        cols = shutil.get_terminal_size().columns
        print("\r" + " " * cols, end="", flush=True)
        print(f"\r{self._end}", flush=True)

    def __exit__(self, exc_type, exc_value, tb):
        # handle exceptions with those variables ^
        self.stop()


if __name__ == "__main__":
    # with Loader() as l:
    #     for i in range(10):
    #         l.progress(10 * i)
    #         sleep(0.25)

    loader = Loader().start()
    for i in range(10):
        loader.progress(10 * i)
        sleep(0.25)
    loader.stop()
import shutil
from itertools import cycle
from threading import Thread
from time import sleep


class Loader:
    def __init__(self, run_description: str = "Loading...", end_description: str = "Done."):
        self._done = False
        self._steps = ["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]
        # self._steps = ["▁", "▂", "▃", "▄", "▅", "▆", "▇", "█", "▇", "▆", "▅", "▄", "▃", "▁"]
        self._timeout = 0.1
        self._desc = run_description
        self._end = end_description
        self._progress = ""
        self._success = True
        self._thread = Thread(target=self._animate, daemon=True)

    def start(self):
        self._thread.start()
        return self

    def _animate(self):
        for c in cycle(self._steps):
            if self._done:
                break
            print(f"\r{c} {self._desc}{self._progress}", flush=True, end="")
            sleep(self._timeout)

    def __enter__(self):
        self.start()

    def progress(self, value):
        self._progress = f"{value}%"

    def stop(self, result_description: str = None, success: bool = True):
        if result_description != None:
            self._end = result_description
        self._success = success
        self._done = True
        cols = shutil.get_terminal_size().columns
        print("\r" + " " * cols, end="", flush=True)
        print(f"\r{'✅' if self._success else '❌'} {self._desc}{self._end}", flush=True)

    def __exit__(self, exc_type, exc_value, tb):
        # handle exceptions with those variables ^
        self.stop()


if __name__ == "__main__":
    # with Loader() as l:
    #     for i in range(10):
    #         l.progress(10 * i)
    #         sleep(0.25)

    loader = Loader().start()
    for i in range(20):
        # loader.progress(5*i)
        sleep(0.1)
    loader.stop()

    loader = Loader().start()
    for i in range(20):
        loader.progress(5 * i)
        sleep(0.1)
    loader.stop(success=False)

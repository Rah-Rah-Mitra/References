from collections.abc import Callable, Iterable, Mapping
import threading
import time
from typing import Any

class SleepyWorker(threading.Thread):
    def __init__(self,seconds, group: None = None, target: Callable[..., object] | None = None, name: str | None = None, args: Iterable[Any] = ..., kwargs: Mapping[str, Any] | None = None, *, daemon: bool | None = None) -> None:
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
    # def __init__(self,seconds, **kwargs):
    #     super(SleepyWorker,self).__init__(**kwargs)
        self._seconds = seconds
        self.start()

    def _sleep_a_little(self):
        time.sleep(self._seconds)

    def run(self):
        self._sleep_a_little()

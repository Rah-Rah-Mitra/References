import asyncio
from collections.abc import Callable, Iterable, Mapping
import multiprocessing
from typing import Any

class MultiprocessingAsync(multiprocessing.Process):
    def __init__(self,durations, group: None = None, target: Callable[..., object] | None = None, name: str | None = None, args: Iterable[Any] = (), kwargs: Mapping[str, Any] = [], *, daemon: bool | None = None) -> None:
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        self._durations = durations

    @staticmethod
    async def async_sleep(duration):
        await asyncio.sleep(duration)
        return duration

    async def consecutive_sleeps(self):
        pending = set()
        for duration in self._durations:
            pending.add(asyncio.create_task(self.async_sleep(duration)))

        while len(pending) > 0:
            done,pending = await asyncio.wait(pending,timeout=1)
            for done_task in done:
                print(await done_task)

    def run(self):
        asyncio.run(self.consecutive_sleeps())
        print('process finished')


if __name__ == '__main__':
    durations = []
    for i in range(1,11):
        durations.append(i)

    processes = []
    for i in range(2):
        processes.append(MultiprocessingAsync(durations[i*5 : (i+1)*5]))

    for p in processes:
        p.start()

    for p in processes:
        p.join()
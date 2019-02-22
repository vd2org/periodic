import asyncio
import logging
from contextlib import suppress

logger = logging.getLogger('periodic')


class Periodic:
    def __init__(self, loop, interval, coro, *args, **kwargs):
        self.coro = coro
        self.args = args
        self.kwargs = kwargs
        self.interval = interval
        self.is_started = False

        self._is_running = False
        self._loop = loop
        self._task = None
        self._handler = None

    async def start(self, delay=None):
        if delay is None:
            delay = self.interval

        if self.is_started:
            return

        self.is_started = True
        self._is_running = False
        if delay == 0:
            self._handler = self._loop.call_soon(self._run)
        else:
            self._handler = self._loop.call_later(self.interval, self._run)

    async def stop(self):
        if not self.is_started:
            return

        self.is_started = False
        if self._handler:
            self._handler.cancel()
            self._handler = None
        if self._task:
            self._task.cancel()
            with suppress(asyncio.CancelledError):
                await self._task
            self._task = None

    async def _runner(self):
        if not self.is_started:
            return

        try:
            with suppress(asyncio.CancelledError):
                await self.coro(*self.args, **self.kwargs)
        except:
            logger.exception('Got exception during awaiting periodically')
        finally:
            self._is_running = False

    def _run(self):
        if not self.is_started:
            return

        self._handler = self._loop.call_later(self.interval, self._run)

        if self._is_running:
            logger.error('Throttling periodic call')
            return

        self._is_running = True
        self._task = asyncio.create_task(self._runner())

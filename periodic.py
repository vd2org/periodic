
import sys
import traceback
import logging
import asyncio
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
 
    async def start(self, immediately=False):
        if not self.is_started:
            self.is_started = True
            self._is_running = False
            if immediately:
                self._handler = self._loop.call_soon(self._run)
            else:
                self._handler = self._loop.call_later(self.interval, self._run)

    async def stop(self):
        if self.is_started:
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
        try:
            if self.is_started:
                with suppress(asyncio.CancelledError):
                    await self.coro(*self.args, **self.kwargs)
        except:
            logger.exception('Got exception durning awaiting periodicly')
        finally:
            self._is_running = False
                
    def _run(self):
        if not self.is_started:
            return

        self._handler = self._loop.call_later(self.interval, self._run)
        
        if not self._is_running:
            self._is_running = True
            self._task = asyncio.ensure_future(self._runner())
        else:
            logger.error('Trottling periodic call')
# Copyright (C) 2017-2019 by Vd.
# This file is part of Periodic package.
# Periodic is released under the MIT License (see LICENSE).

import asyncio
import logging
from contextlib import suppress
from typing import Callable, Awaitable

logger = logging.getLogger('periodic')


class Periodic:
    def __init__(self, interval: float, coro: Callable[..., Awaitable], *args, **kwargs):
        """Creates new periodic.

        Stores coro internally and runs it every `interval` seconds.
        `args` and `kwargs` will be transferred to present coro when it's called.

        If invoked task still running more than `interval` seconds,
        periodic will throttle call(skip it) and log error message.

        :param interval: Run interval.
        :param coro: Any callable object that returns awaitable(e.g. coroutine function).
        :param args: Positional arguments for present coro.
        :param kwargs: Keywords arguments for present coro.
        """

        self.__coro = coro
        self.__args = args
        self.__kwargs = kwargs
        self.__interval = interval
        self.__started = False

        self.__running = False
        self.__loop = asyncio.get_event_loop()
        self.__task = None
        self.__handler = None

    @property
    def interval(self):
        """

        :return: Using interval.
        """
        return self.__interval

    @property
    def started(self):
        """ Current periodic state.

        :return: True if periodic is started.
        """

        return self.__started

    @property
    def running(self):
        """ Current task state.

        :return: True if task is running.
        """

        return self.__running

    @property
    def coro(self):
        """

        :return: Using coro.
        """

        return self.__coro

    @property
    def args(self):
        """

        :return: Using args.
        """

        return self.__args

    @property
    def kwargs(self):
        """

        :return: Using kwargs.
        """

        return self.__kwargs

    async def start(self, delay: float = None):
        """Starts periodic.

        If `delay` is None(default) task will be called first time after selected
        interval, if 0, task will be called immediately, otherwise task will be
        called after `delay` seconds.

        :param delay: Delay for the first run of task in seconds. Default is None.
        :return: None
        """

        if self.__started:
            return

        if delay is None:
            delay = self.__interval

        self.__started = True
        self.__running = False

        if delay is None:
            delay = self.__interval
        if delay == 0:
            self.__handler = self.__loop.call_soon(self.__run)
        else:
            self.__handler = self.__loop.call_later(delay, self.__run)

    async def stop(self, wait: float = 0):
        """Stops periodic. Wait or cancel task if it running.

        If `wait` is 0(by default) task will be cancelled immediately. If False
        then stop will wait until task finished, otherwise stop will wait for
        present seconds and then cancel task.

        :param wait: Seconds for waiting task for stop.
        :return: None
        """

        if not self.__started:
            return

        self.__started = False

        if self.__handler:
            self.__handler.cancel()
            self.__handler = None

        if self.__task is None:
            return

        if wait is False:
            wait = None

        with suppress(asyncio.TimeoutError, asyncio.CancelledError):
            await asyncio.wait_for(self.__task, wait)

        self.__task = None
        self.__running = False

    async def __runner(self):
        if not self.__started:
            return

        try:
            with suppress(asyncio.CancelledError):
                await self.__coro(*self.__args, **self.__kwargs)
        except:  # catching all exceptions
            logger.exception('Got exception during awaiting periodically')
        finally:
            self.__running = False

    def __run(self):
        if not self.__started:
            return

        self.__handler = self.__loop.call_later(self.__interval, self.__run)

        if self.__running:
            logger.error('Throttling periodic call')
            return

        self.__running = True
        self.__task = asyncio.create_task(self.__runner())

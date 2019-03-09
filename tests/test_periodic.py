import pytest
import asyncio

from periodic import Periodic


@pytest.fixture
def loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


def test_run(loop):
    """
    Test that coro runned as expected.
    """

    store = dict(value='was not running')

    async def func():
        store['value'] = 'already runned'

    pr = Periodic(0.01, func)

    async def do():
        await pr.start()
        await asyncio.sleep(0.1)
        await pr.stop()

    loop.run_until_complete(do())

    assert 'already runned' == store['value'], "After run value should be set."


def test_not_run(loop):
    """
    Test that coro not runned with given time.
    """

    store = dict(value='was not running')

    async def func():
        store['value'] = 'already runned'

    pr = Periodic(1, func)

    async def do():
        await pr.start()
        await asyncio.sleep(0.1)
        await pr.stop()

    loop.run_until_complete(do())

    assert 'was not running' == store['value'], "After run value should not be set."


def test_throttling(loop):
    """
    Test throttling.
    """

    store = dict(count=0)

    async def func():
        store['count'] += 1
        await asyncio.sleep(0.1)

    pr = Periodic(0.1, func)

    async def do():
        await pr.start()
        await asyncio.sleep(0.4)
        await pr.stop()

    loop.run_until_complete(do())

    assert 2 == store['count'], "After run count should be 2."


def test_args(loop):
    """
    Test passing args.
    """

    store = dict(arg=None)

    async def func(arg):
        store['arg'] = arg

    pr = Periodic(0.01, func, 'expected')

    async def do():
        await pr.start()
        await asyncio.sleep(0.1)
        await pr.stop()

    loop.run_until_complete(do())

    assert 'expected' == store['arg'], "After run arg should be 'expected'."


def test_kwargs(loop):
    """
    Test passing kwargs.
    """

    store = dict(value=None)

    async def func(value=None):
        store['value'] = value

    pr = Periodic(0.01, func, value='expected')

    async def do():
        await pr.start()
        await asyncio.sleep(0.1)
        await pr.stop()

    loop.run_until_complete(do())

    assert 'expected' == store['value'], "After run arg should be 'expected'."


def test_args_kwargs(loop):
    """
    Test passing args and kwargs together.
    """

    store = dict(arg=None, value=None)

    async def func(arg, value=None):
        store['arg'] = arg
        store['value'] = value

    pr = Periodic(0.01, func, 'expected_arg', value='expected_kwarg')

    async def do():
        await pr.start()
        await asyncio.sleep(0.1)
        await pr.stop()

    loop.run_until_complete(do())

    assert 'expected_arg' == store['arg'], "After run arg should be 'expected'."
    assert 'expected_kwarg' == store['value'], "After run arg should be 'expected'."

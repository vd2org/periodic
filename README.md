# periodic

Simple tool for run asyncio tasks periodically.

# Setup

```bash
pip install asyncio-periodic
```


# Example usage

```python
import asyncio
from datetime import datetime

from periodic import Periodic


async def periodically(param):
    print(datetime.now(), 'Yay!', param)
    await asyncio.sleep(1)
    print(datetime.now(), 'Done!')
    
async def main():
    p = Periodic(3, periodically, 'Periodically!')
    await p.start()
    
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
```

# Testing

Code tested automatically using travis.
You can see build status here: https://travis-ci.com/vd2org/periodic

To test code manually install and run pytest:

```bash
pip install pytest
python -m pytest tests/
```
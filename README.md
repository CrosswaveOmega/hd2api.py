# Helldivers 2 Python API Wrapper

This is an asyncronous api library for the Helldivers 2 API and many of it's community wrappers.

Request the raw data from the api, and use the builders to create easy to understand data classes, potentially using a newer set of static json files so that in game updates can be quickly reflected across objects returned by this library.

All returned objects are Pydantic Models.

Requirements:
 * httpx
 * pydantic


### current stable installation
```
 pip install -U hd2api.py
```
### current latest installation
```
 pip install -U git+https://github.com/CrosswaveOmega/hd2api.py.git
```


### Basic usage
```python
import asyncio
from hd2api import GetApiRawAll, ApiConfig
async def main():
    apiconfig=ApiConfig()
    allval=await GetApiRawAll(apiconfig)
    print(allval.status)


asyncio.run(main)
```
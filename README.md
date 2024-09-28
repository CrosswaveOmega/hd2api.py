# Helldivers 2 Python API Wrapper

This is an asyncronous api frontend library for the Helldivers 2 API and many of it's community wrappers.

Get the latest game state from Helldivers 2,
and transform the raw data into collated
data objects complete with important planet effects,
the latest biome and enviornmental hazards,
and more.

Still currently in development, expect frequent updates
as the static data required by the package to
build the collated objects can change in between patches to Helldivers 2.

All returned objects are Pydantic Models,
which allow them to be quickly dumped and loaded
from/to json strings.

Please note, this API Wrapper was designed to 
primarily work with the asyncio module.  

Requirements:
 * httpx
 * pydantic

This front end supports:

* The community api.
https://github.com/helldivers-2/api

* The diveharder api.
https://github.com/helldivers-2/diveharder_api.py/

* Arrowhead's official API.


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
from hd2api import GetApiRawAll, ApiConfig, build_planet_2
async def main():
    apiconfig=ApiConfig()
    allval=await GetApiRawAll(apiconfig)
    print(allval.status)
    planet=build_planet_2(64,allval, apiconfig.staticdata())
    print(planet)


asyncio.run(main)
```
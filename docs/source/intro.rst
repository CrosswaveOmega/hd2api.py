Introduction
============

This is an all in one library for the Helldivers 2 API as well as the diveharder and community API wrappers,
for use with asyncio python applications.

Fetch raw data from the official API, and collate the api's raw data together
into 'built' objects with optional up to date static files.


Installing
-----------

This library requires Python version 3.8+ for it's pydantic and httpx dependencies.


current stable installation ::

    pip install -U hd2api.py

current latest installation ::

    pip install -U git+https://github.com/CrosswaveOmega/hd2api.py.git



BASIC USAGE
-----------


.. code-block:: python3

    # Retrieve the war status
    import asyncio
    from hd2api import GetApiRawWarStatus, ApiConfig
    async def main():
        apiconfig=ApiConfig()
        allval=await GetApiRawWarStatus(apiconfig)
        print(allval)

    asyncio.run(main)


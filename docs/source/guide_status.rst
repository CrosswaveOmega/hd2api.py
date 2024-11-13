Accessing the Helldivers APIs
=============================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   intro
   hd2api


The Galactic War in Helldivers 2 is one of the key features of the game,
where every mission by every player contributes to an overarching narrative
for the game world.

To facilitate this, Arrowhead launched a web based api which returns the
current state of the Galactic War as it is now, which many in the community
have used to create their own third party applications, such as the
`Helldivers 2 Companion App <https://helldiverscompanion.com/>`_.

But before anything else, you need to define a new APIConfig.


APIConfig
^^^^^^^^^
.. autopydantic_model::  hd2api.api_config.APIConfig
    :no-index:
    :members:
    :model-hide-paramlist:
    :undoc-members: False

ServiceEndpoints
^^^^^^^^^^^^^^^^


There are 5 important raw endpoints from the game's api to consider, each returns an import game object.



War Status is the current state of the galactic war
.. autofunction:: hd2api.services.async_raw_service.GetApiRawWarStatus
   :no-index:

WarInfo is additional infomation on the galactic war's planets, including their supply lines
.. autofunction:: hd2api.services.async_raw_service.GetApiRawWarInfo
   :no-index:

WarSummary is the statistics gathered during the galactic war
.. autofunction:: hd2api.services.async_raw_service.GetApiRawSummary
   :no-index:

Assignment is the major order, if there currently is one.
.. autofunction:: hd2api.services.async_raw_service.GetApiRawAssignment
   :no-index:

The NewsFeed is the list of dispatches.
.. autofunction:: hd2api.services.async_raw_service.GetApiRawNewsFeed
   :no-index:


Of course, if you want to get every raw object at once, it's recommended to use the
GetApiRawAll function, which will return everything within a self contained
"DiveharderAll" class.

.. autofunction:: hd2api.services.async_raw_service.GetApiRawAll
   :no-index:

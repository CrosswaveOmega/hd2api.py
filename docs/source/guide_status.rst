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


ApiConfig
^^^^^^^^^
.. autopydantic_model::  hd2api.api_config.APIConfig
    :no-index:
    :members:
    :model-hide-paramlist:
    :undoc-members: False

ServiceEndpoints
^^^^^^^^^^^^^^^^


There are 5 important raw endpoints from the game's api to consider, each returns an import game object.

.. autofunction:: hd2api.services.async_raw_service.GetApiRawWarStatus
   :no-index:

.. autofunction:: hd2api.services.async_raw_service.GetApiRawWarInfo
   :no-index:


.. autofunction:: hd2api.services.async_raw_service.GetApiRawSummary
   :no-index:

.. autofunction:: hd2api.services.async_raw_service.GetApiRawAssignment
   :no-index:

.. autofunction:: hd2api.services.async_raw_service.GetApiRawNewsFeed
   :no-index:



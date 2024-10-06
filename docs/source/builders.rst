Building Frontend Objects from Raw Data
=======================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   intro
   hd2api

In order to turn the raw objects returned by the api into something that
your python applications would have an easier time parsing, this library
provides access to a set of "Builder" functions which handle much of the collating.

Build dictionary of all planets
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If you need to build a dictionary of all planets in the game,
you'd use the build_all_planets function below.
.. autofunction:: hd2api.builders.planet_builder.build_all_planets
   :no-index:


Example usage

.. code-block:: python3

    # Retrieve the war status
    import asyncio
    from hd2api import GetApiRawAll, ApiConfig, DiveharderAll
    from hd2api.builders import build_all_planets

    apiconfig=ApiConfig()
    async def get_planets():
        allval=await GetApiRawAll(apiconfig)
        planets=build_all_planets(allval, apiconfig.staticdata())
        print(allval)
        return planets

build_all_planets will automatically add in any active planet effects
which are found within the ApiConfig.effects folder.

Please note, while the community api does return built objects,
they don't contain certain newer fields, such as the active planet effects.

Building up campaigns
^^^^^^^^^^^^^^^^^^^^^
You can then load each planet from the planets dictionary into
any campaigns using the build_all_campaigns builder function
.. autofunction:: hd2api.builders.campaign_builder.build_all_campaigns
   :no-index:


Example usage

.. code-block:: python3

   from hd2api.builders import build_all_campaigns

   from hd2api import GetApiRawAll, ApiConfig, DiveharderAll

   async def get_campaigns():
        apiconfig=ApiConfig()
        allval=await GetApiRawAll(apiconfig)
        planets=build_all_planets(allval, allval.war_status)
        print(allval)
        return build_all_campaigns(planets, allval.war_status)



Building Assignment2
^^^^^^^^^^^^^^^^^^^^

If there is currently a major order, this library can parse it into a special
`Assignment2` object using `build_all_assignments`.

Built `Assignment2` objects translate the internal `Assignment`'s Task objects
into something a user can more easily get, IF it was seen before.

.. autofunction:: hd2api.builders.assignment_builder.build_all_assignments
   :no-index:


Example usage

.. code-block:: python3

   from hd2api.builders import build_all_assignments

   from hd2api import GetApiRawAssignment, ApiConfig

   async def get_assignments():
        apiconfig=ApiConfig()
        assignment=await GetApiRawAssignment(apiconfig)
        assignments=get_assignments(assignment)
        return assignment

`Assignment2` may require some front end code to display what you need, though.

.. code-block:: python3

   from hd2api import extract_timestamp as et

   def create_assignment_text(
      data: Assignment2,
      planets: Dict[int, Planet] = {},
      assign_delta: Optional[Assignment2] = None,
   ):
      '''Example function which returns a tuple of the formatted assignment infomation.'''
      did, title = data.id, data.title
      briefing = data.briefing

      assigment_num=f"Assignment A#{did}"
      diff, rates = None, []
      #expiration is a ISO string, so use extract_timestamp to turn it from
      #that format into a format the app can use.
      expire_time = extract_timestamp(data.expiration)
      time_remaining = (expire_time - data.retrieved_at).total_seconds()

      # Assign_delta is the difference between the current Assignment2 and
      # an Assignment2 retrieved from before.
      if data and assign_delta:
         diff = assign_delta.progress if assign_delta.progress else []
         seconds = assign_delta.time_delta.total_seconds()
         if seconds > 0:
               rates = [i / seconds for i in diff]
         else:
               rates = [i / 1 for i in diff]

      progress = data.progress
      task_description = data.description
      tasks = []
      for e, task in enumerate(data.tasks):
         chg, projected = None, None
         prog = ""
         if diff and isinstance(diff, list):
               if e < len(diff):
                  chg = diff[e]
                  projected = progress[e] + (rates[e] * time_remaining)
         tasks.append(task.task_str(progress[e], e, planets, chg, projected))

      rewards=[]
      if data.rewards:
         #Some MOs have multiple Rewards.
         for e, d in enumerate(data.rewards):
            rewards.append(("Reward {e}", value=d.format())
      else:
         rewards.append(("Reward", value=data.reward.format())
      return assigment_num,title,briefing,task_description,tasks,rewards

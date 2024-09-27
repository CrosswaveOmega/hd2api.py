from typing import List, Optional, Type, TypeVar, Dict

import httpx

import datetime as dt
from ..api_config import APIConfig, HTTPException
from ..models import *
from ..models.ABC.model import BaseApiModel

from ..constants import task_types, value_types, faction_names, samples


def build_planet_effect(static_effects: EffectStatic, idv: int) -> KnownPlanetEffect:
    """
    Given a static representation of all known planet effects with their ids,
    retrieve the known planet effect if it exists.

    Args:
        static_effects (EffectStatic): The static representation containing all known effects
            generated from the json files in ./statics
        idv (int): The ID of the planet effect to retrieve.

    Returns:
        KnownPlanetEffect: A known planet effect with a matching id;
        otherwise, a Newly created KnownPlanetEffect indicating the effect is unknown.
    """
    if static_effects.planetEffects is not None:
        peffect: Dict[int, KnownPlanetEffect] = cast(dict, static_effects.planetEffects)
        if idv in peffect:
            # Effect is known.
            return peffect[idv]
        return KnownPlanetEffect(
            galacticEffectId=idv,
            name=f"Planet Effect {idv}",
            description="This planet effect is unknown...",
        )

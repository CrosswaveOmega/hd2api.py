from typing import Dict, cast

from ..models import EffectStatic, KnownPlanetEffect


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

from typing import Dict, List, Optional, cast

from pydantic import Field

from .ABC.model import BaseApiModel
from .Biome import Biome
from .Effects import KnownPlanetEffect
from .Hazard import Hazard

__all__ = ["EffectStatic", "PlanetStatic", "GalaxyStatic", "StaticAll"]


class EffectStatic(BaseApiModel):
    """
    Pydantic reprersentation of all the json files pertaining to effects,
    generated from statics/effects/planetEffects
    """

    planetEffects: Dict[int, KnownPlanetEffect] = Field(
        alias="planetEffects",
        default_factory=dict,
        description="Dictionary of all known planet effects, where the key is the galacticEffectId",
    )

    def check_for_id(self, idv):
        peffect: Dict[int, KnownPlanetEffect] = cast(dict, self.planetEffects)
        if idv in peffect:
            return peffect[idv]
        return KnownPlanetEffect(
            galacticEffectId=idv,
            name=f"Effect {idv}",
            description="Mysterious signature...",
        )


class PlanetStatic(BaseApiModel):
    """All static data reguarding each planet, generated from statics/planets/planets.json"""

    name: Optional[str] = Field(
        alias="name", default=None, description="English name of the planet."
    )
    sector: Optional[str] = Field(
        alias="sector", default=None, description="The name of the planet's sector."
    )
    biome: Optional[str] = Field(
        alias="biome", default=None, description="The 'slug' for the planet's biome."
    )
    environmentals: Optional[List[str]] = Field(
        alias="environmentals",
        default=None,
        description="List of all enviormental effects on this planet.",
    )
    weather_effects: Optional[List[str]] = Field(
        alias="weather_effects",
        default=None,
        description="List of all weather based effects on this planet.",
    )
    type: Optional[str] = Field(
        alias="type",
        default=None,
        description="The 'PlanetType' of this planet.  This determines terrain layouts.",
    )
    names: Optional[Dict[str, str]] = Field(
        alias="names",
        default=None,
        description="All known localized names for this planet.",
    )


class PlanetRegionStatic(BaseApiModel):
    """All static data reguarding each region, generated from statics/planets/planetRegion.json"""

    name: Optional[str] = Field(
        alias="name", default=None, description="English name of the region."
    )
    description: Optional[str] = Field(
        alias="description",
        default=None,
        description="The Description for this region.",
    )


class GalaxyStatic(BaseApiModel):
    """
    Pydantic reprersentation of all the json files pertaining to planets,
    generated from everything inside statics/planets/**
    """

    biomes: Optional[Dict[str, Biome]] = Field(
        alias="biomes",
        default=None,
        description="fan names and descriptions of all known biomes effects.",
    )

    environmentals: Optional[Dict[str, Hazard]] = Field(
        alias="environmentals",
        default=None,
        description="Names and descriptions of all known enviornmental effects.",
    )

    planets: Optional[Dict[int, PlanetStatic]] = Field(
        alias="planets", default=None, description="All static planet data."
    )
    planetRegion: Optional[Dict[int, PlanetRegionStatic]] = Field(
        alias="planetRegion",
        default_factory=dict,
        description="All static planet region data.",
    )


class StaticAll(BaseApiModel):
    """All the static models in one package."""

    galaxystatic: Optional[GalaxyStatic] = Field(alias="galaxystatic", default=None)

    effectstatic: Optional[EffectStatic] = Field(alias="effectstatic", default=None)

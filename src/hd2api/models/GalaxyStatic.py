import datetime
from typing import *

from pydantic import Field
from .ABC.model import BaseApiModel, HealthMixin

from .Biome import Biome
from .Event import Event
from .Hazard import Hazard
from .Position import Position
from .Statistics import Statistics
from .Base.PlanetStatus import PlanetStatus
from .Base.PlanetInfo import PlanetInfo
from .Planet import Planet
from .Base.PlanetStats import PlanetStats
from .Effects import KnownPlanetEffect

from ..constants import task_types, value_types, faction_names, samples

from ..util.utils import (
    human_format as hf,
    changeformatif as cfi,
    extract_timestamp as et,
)


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
        if idv in self.planetEffects:
            return self.planetEffects[idv]
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
    names: Optional[Dict[str, str]] = Field(
        alias="names", default=None, description="All known localized names for this planet."
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


class StaticAll(BaseApiModel):
    """All the static models in one package."""

    galaxystatic: Optional[GalaxyStatic] = Field(alias="galaxystatic", default=None)

    effectstatic: Optional[EffectStatic] = Field(alias="effectstatic", default=None)

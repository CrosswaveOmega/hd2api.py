from typing import *

from pydantic import Field
from ..ABC.model import BaseApiModel


from ...util.utils import human_format as hf, changeformatif as cfi


class PlanetEvent(BaseApiModel):
    """
    Raw model representing An ongoing event on a planet, such as defense campaigns.

    """

    id: Optional[int] = Field(default=None, description="The unique identifier of this event.")

    planetIndex: Optional[int] = Field(
        default=None, description="The planetIndex of the planet where this event is."
    )

    eventType: Optional[int] = Field(
        default=None,
        description="A numerical identifier that indicates what type of event this is."
        + "Only one type is known so far, that being event type 1.",
    )

    race: Optional[int] = Field(
        default=None, description="The identifier of the faction that owns the planet currently."
    )

    health: Optional[int] = Field(default=None, description="The current health of the event.")

    maxHealth: Optional[int] = Field(
        default=None, description="The current maximum health of the event."
    )

    startTime: Optional[int] = Field(
        default=None,
        description="When this event started, in arrowhead's internal 'wartime' format.",
    )

    expireTime: Optional[int] = Field(
        default=None,
        description="When the event will end, in arrowhead's internal 'wartime' format.",
    )

    campaignId: Optional[int] = Field(
        default=None,
        description="For defense campaign events, this is the unique identifier pointing to a campaign object.",
    )

    jointOperationIds: Optional[List[int]] = Field(
        default=None, description="A list of identifiers of related joint operations."
    )

    def long_event_details(self):
        factions = {1: "Humans", 2: "Terminids", 3: "Automaton", 4: "Illuminate"}
        event_details = (
            f"ID: {self.id}, Type: {self.eventType}, Faction: {factions.get(self.race,'UNKNOWN')}\n"  # type: ignore
            f"Event Health: `{(self.health)}/{(self.maxHealth)}`\n"
            f"Start Time: {self.startTime}, End Time: {self.expireTime}\n"
            f"Campaign ID: C{self.campaignId}, Joint Operation IDs: {', '.join(map(str, self.jointOperationIds))}"  # type: ignore
        )
        return event_details

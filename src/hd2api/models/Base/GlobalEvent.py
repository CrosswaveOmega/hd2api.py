from typing import *
import datetime
from pydantic import Field
from ..ABC.model import BaseApiModel, HealthMixin


class GlobalEvent(BaseApiModel):
    """
    Raw object which is an ongoing global event.


    """

    eventId: Optional[int] = Field(
        alias="eventId", default=None, description="The ID of the event."
    )
    id32: Optional[int] = Field(alias="id32", default=None, description="The 32-bit ID.")
    portraitId32: Optional[int] = Field(
        alias="portraitId32", default=None, description="The 32-bit ID of the portrait."
    )
    title: Optional[str] = Field(alias="title", default=None, description="The title of the event.")
    titleId32: Optional[int] = Field(
        alias="titleId32", default=None, description="The 32-bit ID for this event's title."
    )
    message: Optional[str] = Field(
        alias="message", default=None, description="The message of the event."
    )
    messageId32: Optional[int] = Field(
        alias="messageId32", default=None, description="The 32-bit ID for this event's message."
    )
    introMediaId32: Optional[int] = Field(
        alias="introMediaId32",
        default=None,
        description="Identifier for an in game image given with this global event.",
    )
    outroMediaId32: Optional[int] = Field(
        alias="outroMediaId32",
        default=None,
        description="Identifier for an in game image given with this global event.",
    )
    race: Optional[int] = Field(alias="race", default=None, description="The race ID.")
    flag: Optional[int] = Field(
        alias="flag", default=None, description="The flag associated with the event."
    )
    assignmentId32: Optional[int] = Field(
        alias="assignmentId32",
        default=None,
        description="The 32-bit ID of the assignment associated with this global event, if applicable.",
    )
    effectIds: Optional[List[int]] = Field(
        alias="effectIds", default_factory=list, description="List of effect IDs."
    )
    planetIndices: Optional[List[int]] = Field(
        alias="planetIndices", default_factory=list, description="List of planet indices."
    )

    def strout(self) -> str:
        formatv = {
            k: v
            for k, v in self.model_dump().items()
            if k not in ["message", "title", "retrieved_at", "time_delta"]
        }

        return ", ".join([f"{k}:`{v}`" for k, v in formatv.items()])

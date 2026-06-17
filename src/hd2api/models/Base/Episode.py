from typing import List, Optional, Tuple, Union

from pydantic import Field

from ...util.utils import hdml_parse
from ..ABC.model import BaseApiModel


from typing import List, Optional

from pydantic import Field

from ...util.utils import hdml_parse
from ..ABC.model import BaseApiModel


class EpisodeReward(BaseApiModel):
    mix_id: Optional[int] = Field(
        alias="mixId", default=None, description="The reward mix identifier."
    )
    amount: Optional[int] = Field(alias="amount", default=None, description="The amount awarded.")


class EpisodePhase(BaseApiModel):
    "A single episode phase in episodes"

    id32: Optional[int] = Field(
        alias="id32", default=None, description="The identifier of this phase."
    )

    intro_title: Optional[str] = Field(
        alias="introTitle", default=None, description="The title displayed when the phase begins."
    )

    intro_message: Optional[str] = Field(
        alias="introMessage", default=None, description="The phase introduction message."
    )

    outro_title: Optional[str] = Field(
        alias="outroTitle", default=None, description="The title displayed when the phase ends."
    )

    outro_message: Optional[str] = Field(
        alias="outroMessage", default=None, description="The phase completion message."
    )

    status: Optional[int] = Field(
        alias="status", default=None, description="The current status of the phase."
    )

    intro_media_id32: Optional[int] = Field(
        alias="introMediaId32", default=None, description="Media shown at the start of the phase."
    )

    outro_media_id32: Optional[int] = Field(
        alias="outroMediaId32", default=None, description="Media shown at the end of the phase."
    )

    entries: Optional[list] = Field(
        alias="entries", default=None, description="Phase entries/objectives."
    )

    rewards: Optional[List[EpisodeReward]] = Field(
        alias="rewards", default=None, description="Rewards granted for completing the phase."
    )


class Episode(BaseApiModel):
    """A single episode in episodes"""

    id32: Optional[int] = Field(
        alias="id32", default=None, description="The identifier of this episode."
    )

    title: Optional[str] = Field(
        alias="title", default=None, description="The title of this episode."
    )

    description: Optional[str] = Field(
        alias="description", default=None, description="The episode description."
    )

    intro_message: Optional[str] = Field(
        alias="introMessage", default=None, description="The introductory message."
    )

    outro_message: Optional[str] = Field(
        alias="outroMessage", default=None, description="The completion message."
    )

    race: Optional[int] = Field(
        alias="race", default=None, description="The faction/race associated with the episode."
    )

    start_war_time: Optional[int] = Field(
        alias="startWarTime", default=None, description="The war time at which the episode begins."
    )

    banner_image_id32: Optional[int] = Field(
        alias="bannerImageId32", default=None, description="Banner image identifier."
    )

    status: Optional[int] = Field(
        alias="status", default=None, description="The current status of the episode."
    )

    phases: Optional[List[EpisodePhase]] = Field(
        alias="phases", default=None, description="The phases that make up this episode."
    )

    rewards: Optional[List[EpisodeReward]] = Field(
        alias="rewards", default=None, description="Rewards granted for completing the episode."
    )


class Episodes(BaseApiModel):
    """
    Represents Episodes.
    """

    episodes: Optional[List[Episode]] = Field(
        alias="episodes", default=None, description="The list of episodes."
    )

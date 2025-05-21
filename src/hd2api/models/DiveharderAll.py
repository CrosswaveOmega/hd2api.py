from typing import List, Optional

from pydantic import Field

from .ABC.model import BaseApiModel
from .Base.Assignment import Assignment
from .Base.NewsFeedItem import NewsFeedItem
from .Base.SteamNewsRaw import SteamNewsRaw
from .Base.WarId import WarId
from .Base.WarInfo import WarInfo
from .Base.WarStatus import WarStatus
from .Base.WarSummary import WarSummary


class DiveharderAll(BaseApiModel):
    """
    Everything returned from the raw api in one convienent package.

    """

    status: Optional[WarStatus] = Field(
        alias="status",
        default=None,
        description="snapshot of the current status of the galactic war at the time of retrieval.",
    )

    war_info: Optional[WarInfo] = Field(
        alias="war_info",
        default=None,
        description="Mostly static information on the current galactic war.",
    )

    planet_stats: Optional[WarSummary] = Field(
        alias="planet_stats",
        default=None,
        description="general statistics about the galaxy and specific planets",
    )

    major_order: Optional[List[Assignment]] = Field(
        alias="major_order",
        default=None,
        description="List of major assignments given from Super Earth to the Helldivers.",
    )

    personal_order: Optional[List[Assignment]] = Field(
        alias="personal_order",
        default=None,
        description="List of smaller sub-assignments given to the Helldivers by Super Earth",
    )

    news_feed: Optional[List[NewsFeedItem]] = Field(
        alias="news_feed",
        default=None,
        description="All items within the newsfeed of Super Earth.",
    )

    updates: Optional[List[SteamNewsRaw]] = Field(
        alias="updates",
        default=None,
        description="List of news articles from a new article from Steam's news feed.",
    )

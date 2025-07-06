from typing import Dict, Optional

from ..models import Campaign, Campaign2, Planet, WarStatus


def build_campaign(planets: Dict[int, Optional[Planet]], campaign: Campaign):
    """
    Create a new Campaign2 instance based on the given Campaign and planet data.

    Args:
        planets (Dict[int, Planet]): A dictionary mapping planet IDs to Planet objects.
        campaign (Campaign): The campaign object that contains the data to create Campaign2.

    Returns:
        Campaign2: A new campaign object with the associated planet and other data.
    """

    planet = planets.get(campaign.planetIndex, None)  # type: ignore
    camp2 = Campaign2(
        retrieved_at=campaign.retrieved_at,
        id=campaign.id,
        planet=planet,
        count=campaign.count,
        type=campaign.type,
        faction=campaign.race,
    )
    return camp2


def build_all_campaigns(planets: Dict[int, Planet], warstatus: WarStatus):
    """
    Build a list of Campaign2 objects from the campaigns in the given WarStatus.

    Args:
        planets (Dict[int, Planet]): A dictionary mapping planet IDs to Planet objects.
        warstatus (WarStatus): The current WarStatus.
    Returns:
        List[Campaign2]: A list of Campaign2 objects built from the warstatus campaigns.
    """
    campaign_2 = []
    for c in warstatus.campaigns:
        campaign_2.append(build_campaign(planets, c))
    return campaign_2

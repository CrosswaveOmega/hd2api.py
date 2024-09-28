from typing import *

# pylint: disable=no-name-in-module
from pydantic import BaseModel, Field
from datetime import datetime, timezone, timedelta


class BaseApiModel(BaseModel):
    """Base model class for everything returend by the api.  Features the retrieved_at and time_delta fields."""

    retrieved_at: Optional[datetime] = Field(alias="retrieved_at", default=None)
    time_delta: Optional[timedelta] = Field(alias="time_delta", default=None)

    def __init__(self, **data):
        super().__init__(**data)
        if "retrieved_at" not in data:
            self.retrieved_at = datetime.now(tz=timezone.utc)
        else:
            if isinstance(data["retrieved_at"], str):
                self.retrieved_at = datetime.fromisoformat(data["retrieved_at"]).replace(
                    tzinfo=timezone.utc
                )
            elif isinstance(data["retrieved_at"], datetime):
                self.retrieved_at = data["retrieved_at"]

    def __getitem__(self, attr):
        """
        Get a field in the same manner as a dictionary.
        """
        return getattr(self, attr)

    def set(self, attr, new=None):
        if not hasattr(self, attr):
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{attr}'")
        setattr(self, attr, new)

    def get(self, attr, default=None):
        if not hasattr(self, attr):
            return default
        return getattr(self, attr)


class HealthMixin:
    health: int
    maxHealth: int

    def health_percent(self):
        """
        Calculate the health percentage based on current health and maximum health.

        Returns:
            float: The health percentage rounded to three decimal places.
        """
        value = self.health / max(self.maxHealth, 1)
        return round(value * 100.0, 3)

    def get_health_percent(self, health: Optional[int], roundby=5):
        """
        Get health divided by the current max health.

        Args:
            health (Optional[int]): The current health value to consider.
            roundby (int, optional): The number of decimal places to round the result. Defaults to 5.

        Returns:
            float: The health percentage rounded to the specified number of decimal places.
        """
        value = int(health) / max(int(self.maxHealth), 0)
        return round(value * 100.0, roundby)

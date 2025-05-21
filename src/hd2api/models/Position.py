import datetime
import math
from typing import List, Optional

from pydantic import Field

from .ABC.model import BaseApiModel


class Position(BaseApiModel):
    """
    A position on the galactic war map, relative to Super Earth.

    """

    x: Optional[float] = Field(alias="x", default=0.0, description="The X coordinate.")
    y: Optional[float] = Field(alias="y", default=0.0, description="The Y coordinate.")

    def __sub__(self, other: "Position") -> "Position":
        result_x = self.x - other.x if self.x is not None and other.x is not None else 0
        result_y = self.y - other.y if self.y is not None and other.y is not None else 0
        timedelta = self.get_time_delta(other)
        return Position(x=result_x, y=result_y, time_delta=timedelta)

    def mag(self) -> float:
        """
        Calculate the magnitude of the Position vector.

        Returns:
            float: The magnitude of the vector (x, y).
        """
        magnitude = math.sqrt(self.x**2 + self.y**2)
        return magnitude

    def distance(self, other: "Position") -> float:
        """
        Calculate the Euclidean distance between this Position and another.

        Args:
            other (Position): Another Position object.

        Returns:
            float: The calculated distance.
        """
        dpos = self - other
        distance = math.sqrt(dpos.x**2 + dpos.y**2)
        return distance

    def speed(self) -> float:
        """
        Calculate the speed based on the distance and time delta.

        Returns:
            float: The speed calculated as distance divided by time in seconds,
                   or 0.0 if time_delta is zero or not present.

        Raises:
            Exception: If delta_seconds is zero or negative.
        """
        if self.time_delta:
            dist = self.mag()
            delta_seconds = self.time_delta.total_seconds()
            if abs(delta_seconds) <= 0:
                return 0.0
                # raise Exception("Delta seconds is zero!")
            return dist / abs(delta_seconds)
        return 0.0

    def angle(self):
        """
        Calculate the current angle of the position with respect to the Y-axis.

        Returns:
            float: The angle in degrees, normalized to the [0, 360] range, where the Y-axis is 0°.
        """
        current_angle = math.degrees(math.atan2(self.x, self.y))  # Y-axis is 0°
        current_angle = (current_angle + 360) % 360  # Normalize to [0, 360] range
        return current_angle

    def estimate_time_to_target(
        self, target: "Position", speed: float, acceleration: Optional[float] = None
    ) -> Optional[datetime.timedelta]:
        """
        Estimate the time required to reach the target position given a speed and optional acceleration.

        Args:
            target (Position): The target Position to reach.
            speed (float): The current speed.
            acceleration (Optional[float]): The acceleration rate. Can be None if not applicable.

        Returns:
            Optional[datetime.timedelta]: The estimated time as a timedelta object if calculable, otherwise None.
        """
        target_diff = target - self
        target_mag = target_diff.mag()
        if speed > 0 and acceleration is not None and acceleration > 0:
            discriminant = speed**2 + 2 * acceleration * target_mag
            if discriminant >= 0:  # Ensure valid square root
                time_to_target = (-speed + math.sqrt(discriminant)) / acceleration
                time_to_target = (
                    time_to_target if time_to_target > 0 else None
                )  # Ensure positive time
                time_to_target = datetime.timedelta(seconds=time_to_target)
            else:
                time_to_target = None  # No valid solution
        elif speed > 0:
            time_to_target = target_mag / speed  # No acceleration case
            time_to_target = datetime.timedelta(seconds=time_to_target)
        else:
            time_to_target = None  # Avoid division by zero
        return time_to_target

    @staticmethod
    def average(positions_list: List["Position"]) -> "Position":
        """
        Average together a list of position differences over time.

        Args:
            positions_list (List[Position]): A list of Position objects to be averaged.

        Returns:
            Position: A new Position object representing the average position and
                      average time delta from the provided list of positions. If the
                      list is empty, returns Position with x, y, and time_delta of 0.
        """
        count = len(positions_list)
        if count == 0:
            return Position(x=0, y=0)

        avg_x = (
            sum(position.x for position in positions_list if position.x is not None)
            / count
        )
        avg_y = (
            sum(position.y for position in positions_list if position.y is not None)
            / count
        )

        avg_time = (
            sum(
                position.time_delta.total_seconds()
                for position in positions_list
                if position.time_delta is not None
            )
            / count
        )
        avg_position = Position(
            x=avg_x,
            y=avg_y,
            time_delta=datetime.timedelta(seconds=avg_time),
        )
        return avg_position

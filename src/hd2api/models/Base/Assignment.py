from typing import *

from pydantic import Field
from ..ABC.model import BaseApiModel

from .Setting import Setting


"""
"Assignment": {
        "type": "object",
        "description": "Represents an assignment given from Super Earth to the Helldivers.",
        "additionalProperties": false,
        "properties": {
          "id32": {
            "type": "integer",
            "description": "Internal identifier of this assignment.",
            "format": "int64"
          },
          "progress": {
            "type": "array",
            "description": "A list of numbers representing progress in the assignment.",
            "items": {
              "type": "integer",
              "format": "uint64"
            }
          },
          "expiresIn": {
            "type": "integer",
            "description": "The amount of seconds until this assignment expires.",
            "format": "int64"
          },
          "setting": {
            "description": "Contains detailed information on this assignment like briefing, rewards, ...",
            "oneOf": [
              {
                "$ref": "#/components/schemas/Setting"
              }
            ]
          }
        }
      },"""


class Assignment(BaseApiModel):
    """
    Raw Model representing an assignment given from Super Earth to the Helldivers.

    """

    id32: Optional[int] = Field(
        alias="id32", default=None, description="Internal identifier of this assignment."
    )

    progress: Optional[List[int]] = Field(
        alias="progress",
        default=None,
        description="A list of numbers representing progress in the assignment.",
    )

    expiresIn: Optional[int] = Field(
        alias="expiresIn",
        default=None,
        description="The amount of seconds until this assignment expires.",
    )

    setting: Optional[Setting] = Field(
        alias="setting",
        default=None,
        description="Contains detailed information on this assignment like briefing, rewards, ...",
    )

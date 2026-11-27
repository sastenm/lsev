"""Pydantic data models for the App Backend.

These types are the route validator: FastAPI checks every request body
against them and answers 422 when one does not match. They also define what
the backend can express at all. A route holds only a name and waypoints, and
a command is one of four values, so no request can carry a steering, throttle
or brake value.

Plain Pydantic only: this module must never import rclpy or FastAPI.
"""

from enum import Enum
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, AwareDatetime

MIN_WAYPOINTS = 2
MAX_WAYPOINTS = 500
MAX_NAME_LENGTH = 64

Latitude = Annotated[
    float, Field(ge=-90, le=90, allow_inf_nan=False, strict=True,
                 description="Decimal degrees, -90 to 90")
]
Longitude = Annotated[
    float, Field(ge=-180, le=180, allow_inf_nan=False, strict=True,
                 description="Decimal degrees, -180 to 180")
]


class _NoExtra(BaseModel):
    """Base for every model the backend accepts or sends. No extra fields permitted."""

    model_config = ConfigDict(extra="forbid")


# ------------------------------------------------------------------ routes --


class Waypoint(_NoExtra):
    latitude: Latitude
    longitude: Longitude


class RouteIn(_NoExtra):
    """Body of POST /api/routes and PUT /api/routes/{id} (front_back_req)."""

    name: Annotated[
        str,
        StringConstraints(strip_whitespace=True, min_length=1,
                          max_length=MAX_NAME_LENGTH),
        Field(description=f"1 to {MAX_NAME_LENGTH} characters after leading and trailing "
                          "spaces are removed; need not be unique"),
    ]
    waypoints: Annotated[
        list[Waypoint], Field(min_length=MIN_WAYPOINTS, max_length=MAX_WAYPOINTS,
                              description=f"{MIN_WAYPOINTS} to {MAX_WAYPOINTS} points, in driving order")
    ]


class Route(RouteIn):
    """A saved route as returned by the API (back_front_res)."""

    id: Annotated[int, Field(strict=True, description="Assigned by SQLite")]
    created_at: AwareDatetime
    updated_at: AwareDatetime


# ---------------------------------------------------------------- commands --


class Command(str, Enum):
    """The only commands the app can send (Decisions Log #4)."""

    START = "start"
    PAUSE = "pause"
    RESUME = "resume"
    CANCEL = "cancel"


class CommandRequest(_NoExtra):
    """Body of POST /api/mission/command. "load" is not accepted here: it has
    its own endpoint because it needs a route id."""

    command: Command


class GateAction(str, Enum):
    """What the command gate decides on: the four commands plus load.

    Internal only, never parsed from a request body. Convert explicitly,
    e.g. GateAction(command.value).
    """

    LOAD = "load"
    START = "start"
    PAUSE = "pause"
    RESUME = "resume"
    CANCEL = "cancel"


# ------------------------------------------------------- vehicle reporting --


class MissionState(str, Enum):
    """States Path Following may report (path_back_status). No STALE here, the
    Command Gate determines whether state is STALE."""

    IDLE = "IDLE"
    READY = "READY"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    FAULT = "FAULT"


class GateState(str, Enum):
    """State the command gate decides on: a reported MissionState, or STALE
    when status or position is 2.0 s old or more. Internal only.
    """

    IDLE = "IDLE"
    READY = "READY"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    FAULT = "FAULT"
    STALE = "STALE"


class FixQuality(str, Enum):
    """GNSS fix quality reported by Path Following.

    Must match lsev_interfaces."""

    NO_FIX = "NO_FIX"        # no position
    GNSS = "GNSS"            # plain GNSS
    RTK_FLOAT = "RTK_FLOAT"  # RTK corrections, ambiguities not fixed
    RTK_FIXED = "RTK_FIXED"  # RTK fixed


class VehicleStatus(_NoExtra):
    """Newest path_back_status, as relayed to the browser."""

    state: MissionState
    route_id: Annotated[int, Field(strict=True)] | None = None
    waypoint_index: Annotated[int, Field(ge=0, strict=True)] | None = None
    fault_text: str = ""


class VehiclePosition(_NoExtra):
    """Newest path_back_position, as relayed to the browser."""

    latitude: Latitude
    longitude: Longitude
    heading_deg: Annotated[
        float, Field(ge=0, le=360, allow_inf_nan=False, strict=True,
                     description="Degrees clockwise from true north")
    ]
    speed_mps: Annotated[
        float, Field(allow_inf_nan=False, strict=True,
                     description="Ground speed in m/s")
    ]
    fix_quality: FixQuality
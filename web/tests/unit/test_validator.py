"""Unit tests for the route validator.

Covers the unit/test_validator.py row of Table 3.4-6 (front_back_req: route
body), plus the command body and a few cases the table does not list:
unknown fields, non-number coordinates, and the status/position models.

These are plain Pydantic tests: a rejected body raises ValidationError here.
FastAPI turns that same error into a 422 response; the HTTP code itself is
checked in integration/test_frontend_api.py. No rclpy, no FastAPI app.
"""

import math

import pytest
from pydantic import ValidationError

from backend.models import (
    Command,
    CommandRequest,
    FixQuality,
    GateAction,
    GateState,
    MissionState,
    RouteIn,
    VehiclePosition,
    VehicleStatus,
)

# A valid point near Corvallis, used to pad routes to a given length.
LAT, LON = 44.5646, -123.2620


def route_body(**overrides):
    """A valid route body as the frontend would send it (plain dicts)."""
    body = {
        "name": "test loop",
        "waypoints": [
            {"latitude": LAT, "longitude": LON},
            {"latitude": LAT + 0.0001, "longitude": LON},
        ]
    }
    body.update(overrides)
    return body


def waypoints(n):
    return [{"latitude": LAT + i * 1e-5, "longitude": LON} for i in range(n)]


def with_point(latitude=LAT, longitude=LON):
    """Valid two-point route whose first point has the given coordinates."""
    return route_body(
        waypoints=[
            {"latitude": latitude, "longitude": longitude},
            {"latitude": LAT, "longitude": LON},
        ]
    )


# ---------------------------------------------------------------- accepted --


@pytest.mark.parametrize("n", [2, 3, 499, 500])
def test_waypoint_count_accepted(n):
    route = RouteIn.model_validate(route_body(waypoints=waypoints(n)))
    assert len(route.waypoints) == n


@pytest.mark.parametrize("latitude", [-90, -89, 89, 90])
def test_latitude_accepted(latitude):
    route = RouteIn.model_validate(with_point(latitude=latitude))
    assert route.waypoints[0].latitude == latitude


@pytest.mark.parametrize("longitude", [-180, -179, 179, 180])
def test_longitude_accepted(longitude):
    route = RouteIn.model_validate(with_point(longitude=longitude))
    assert route.waypoints[0].longitude == longitude


def test_waypoint_order_and_values_kept():
    body = route_body(waypoints=waypoints(5))
    route = RouteIn.model_validate(body)
    assert [w.model_dump() for w in route.waypoints] == body["waypoints"]


# ---------------------------------------------------------------- rejected --


@pytest.mark.parametrize("n", [0, 1, 501])
def test_waypoint_count_rejected(n):
    with pytest.raises(ValidationError):
        RouteIn.model_validate(route_body(waypoints=waypoints(n)))


@pytest.mark.parametrize("latitude", [-91, 91])
def test_latitude_rejected(latitude):
    with pytest.raises(ValidationError):
        RouteIn.model_validate(with_point(latitude=latitude))


@pytest.mark.parametrize("longitude", [-181, 181])
def test_longitude_rejected(longitude):
    with pytest.raises(ValidationError):
        RouteIn.model_validate(with_point(longitude=longitude))


@pytest.mark.parametrize("missing", ["name", "waypoints"])
def test_missing_field_rejected(missing):
    body = route_body()
    del body[missing]
    with pytest.raises(ValidationError):
        RouteIn.model_validate(body)


# -------------------------------------------------------------- test types --


@pytest.mark.parametrize("bad", ["45.5", True, None, [45.5]])
def test_non_number_coordinate_rejected(bad):
    # Default (lax) Pydantic reads "45.5" as 45.5 and true as 1.0.
    with pytest.raises(ValidationError):
        RouteIn.model_validate(with_point(latitude=bad))


def test_unknown_route_field_rejected():
    # Default Pydantic drops unknown fields silently. Rejecting them backs the
    # doc's claim that no request can carry a steering, throttle or brake value.
    with pytest.raises(ValidationError):
        RouteIn.model_validate(route_body(steer_left=5))


def test_unknown_waypoint_field_rejected():
    body = route_body()
    body["waypoints"][0]["throttle"] = 0.5
    with pytest.raises(ValidationError):
        RouteIn.model_validate(body)


def test_client_cannot_set_id():
    # The id is assigned by SQLite, never taken from the request body.
    with pytest.raises(ValidationError):
        RouteIn.model_validate(route_body(id=7))


# ------------------------------------------------------------ command body --


@pytest.mark.parametrize("value", ["start", "pause", "resume", "cancel"])
def test_command_accepted(value):
    assert CommandRequest.model_validate({"command": value}).command == Command(value)


@pytest.mark.parametrize(
    "value", ["load", "steer_left", "START", "stop", "", None, 1]
)
def test_command_rejected(value):
    with pytest.raises(ValidationError):
        CommandRequest.model_validate({"command": value})


def test_command_extra_field_rejected():
    with pytest.raises(ValidationError):
        CommandRequest.model_validate({"command": "start", "speed": 2.0})


def test_command_set_is_exactly_four():
    assert {c.value for c in Command} == {"start", "pause", "resume", "cancel"}


def test_gate_actions_are_commands_plus_load():
    assert {a.value for a in GateAction} == {c.value for c in Command} | {"load"}


# ---------------------------------------------- status and position models --


def test_gate_states_are_mission_states_plus_stale():
    assert {g.value for g in GateState} == {m.value for m in MissionState} | {"STALE"}


@pytest.mark.parametrize("value", ["STALE", "running", "UNKNOWN", ""])
def test_reported_state_outside_the_five_rejected(value):
    # A Path Following message must never be able to claim a backend-only
    # state; AB-06 turns this error into FAULT and logs it.
    with pytest.raises(ValidationError):
        VehicleStatus.model_validate({"state": value})


@pytest.mark.parametrize("heading", [0.0, 90.0, 360])
def test_heading_accepted(heading):
    p = VehiclePosition(
        latitude=LAT, longitude=LON, heading_deg=heading,
        speed_mps=1.2, fix_quality=FixQuality.RTK_FIXED,
    )
    assert p.heading_deg == heading


@pytest.mark.parametrize("heading", [-0.1, 360.1, math.nan])
def test_heading_rejected(heading):
    with pytest.raises(ValidationError):
        VehiclePosition(
            latitude=LAT, longitude=LON, heading_deg=heading,
            speed_mps=1.2, fix_quality=FixQuality.RTK_FIXED,
        )

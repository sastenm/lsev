"""Command gate (Table 3.4-4).

Decides whether the backend may forward an action to Path Following, given the
vehicle's state. The gate only narrows what goes out: Path Following can still
reject anything the gate allows.

Pause and cancel are allowed in every state, so the backend never blocks a
stop. Start and resume never go out while status or position is stale.
"""

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType

from backend.models import GateAction, GateState

# Read-only, so no other module (or test) can widen the gate at runtime.
ALLOWED_ACTIONS: Mapping[GateState, frozenset[GateAction]] = MappingProxyType({
    GateState.IDLE: frozenset({GateAction.LOAD, GateAction.PAUSE, GateAction.CANCEL}),
    GateState.READY: frozenset({GateAction.START, GateAction.LOAD,
                                GateAction.PAUSE, GateAction.CANCEL}),
    GateState.RUNNING: frozenset({GateAction.PAUSE, GateAction.CANCEL}),
    GateState.PAUSED: frozenset({GateAction.RESUME, GateAction.PAUSE, GateAction.CANCEL}),
    GateState.FAULT: frozenset({GateAction.PAUSE, GateAction.CANCEL}),
    GateState.STALE: frozenset({GateAction.PAUSE, GateAction.CANCEL}),
})


@dataclass(frozen=True)
class GateDecision:
    """Result of check(). reason is empty when allowed and says why when refused,
    it is shown to the operator (409 body) and written to command_log."""

    allowed: bool
    reason: str = ""


def check(state: GateState, action: GateAction) -> GateDecision:
    """Decide whether the backend may forward action while the vehicle is in state.

    Raises TypeError unless state is a GateState and action is a GateAction.
    Both enums are (str, Enum), so a MissionState, a Command or a plain string
    would otherwise match by accident; a MissionState would also mean the
    caller skipped the staleness step.
    """
    if not isinstance(state, GateState):
        raise TypeError(f"state must be a GateState, got {type(state).__name__}")
    if not isinstance(action, GateAction):
        raise TypeError(f"action must be a GateAction, got {type(action).__name__}")

    # A state missing from ALLOWED_ACTIONS raises KeyError on purpose: fail
    # loudly rather than refuse quietly. test_every_state_has_an_entry guards it.
    if action in ALLOWED_ACTIONS[state]:
        return GateDecision(allowed=True)

    if state is GateState.STALE:
        reason = f"{action.value} is not allowed while vehicle status or position is stale"
    else:
        reason = f"{action.value} is not allowed while the vehicle is {state.value}"
    return GateDecision(allowed=False, reason=reason)
 
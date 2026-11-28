"""Unit tests for the command gate (Table 3.4-4).

EXPECTED_ALLOWED is written out by hand from the table, not built from
gate.ALLOWED_ACTIONS, so a wrong mapping can't pass its own test.
"""

import pytest

from backend.gate import ALLOWED_ACTIONS, check
from backend.models import Command, GateAction, GateState, MissionState

S, A = GateState, GateAction

# Table 3.4-4: the actions the backend forwards in each state.
EXPECTED_ALLOWED = {
    S.IDLE: {A.LOAD, A.PAUSE, A.CANCEL},
    S.READY: {A.START, A.LOAD, A.PAUSE, A.CANCEL},
    S.RUNNING: {A.PAUSE, A.CANCEL},
    S.PAUSED: {A.RESUME, A.PAUSE, A.CANCEL},
    S.FAULT: {A.PAUSE, A.CANCEL},
    S.STALE: {A.PAUSE, A.CANCEL},
}

ALL_CASES = [(s, a) for s in GateState for a in GateAction]


@pytest.mark.parametrize(
    "state, action", ALL_CASES, ids=[f"{s.value}-{a.value}" for s, a in ALL_CASES]
)
def test_gate_matches_table(state, action):
    decision = check(state, action)
    if action in EXPECTED_ALLOWED[state]:
        assert decision.allowed
        assert decision.reason == ""
    else:
        assert not decision.allowed
        # Shown to the operator, so it must name both the action and the state.
        assert action.value in decision.reason
        assert state.value.lower() in decision.reason.lower()


def test_every_state_has_an_entry():
    # Adding a GateState without updating the gate must fail here.
    assert set(ALLOWED_ACTIONS) == set(GateState)


def test_safety_rules():
    # Checked apart from the table, so editing the table and the gate
    # together can't quietly break them.
    for state in GateState:
        assert check(state, A.PAUSE).allowed
        assert check(state, A.CANCEL).allowed
    assert not check(S.STALE, A.START).allowed
    assert not check(S.STALE, A.RESUME).allowed


@pytest.mark.parametrize(
    "state, action",
    [
        (MissionState.RUNNING, A.PAUSE),
        (S.RUNNING, Command.PAUSE),
        ("RUNNING", "pause"),
    ],
    ids=["MissionState", "Command", "str"],
)
def test_wrong_types_rejected(state, action):
    # Pause is allowed in every state, so each of these would get through
    # without the type check ((str, Enum) members compare equal to strings).
    with pytest.raises(TypeError):
        check(state, action)

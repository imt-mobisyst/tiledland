"""Behavioral regressions: run with pytest -q tests/06-regressions.

Failures deliberately expose unresolved defects; do not hide them with xfail.
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import src.tiledland as tild

def coordinates(shape):
    return [coordinate for point in shape.points() for coordinate in point.asTuple()]


def test_fast_agent_perceives_its_body_separately_from_tabletop():
    body = tild.Unit()
    tabletop = tild.Map().initLine(2)
    agent = Agent(body, tabletop)
    assert agent.perceivedTabletop() is tabletop
    assert agent.perceivedBody() is body


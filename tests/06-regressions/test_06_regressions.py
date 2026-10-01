"""Behavioral regressions: run with pytest -q tests/06-regressions.

Failures deliberately expose unresolved defects; do not hide them with xfail.
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.tiledland import Action, Agent, Convex, Entity, Land, Point, Tabletop


def coordinates(shape):
    return [coordinate for point in shape.points() for coordinate in point.asTuple()]


def test_fast_agent_perceives_its_body_separately_from_tabletop():
    body = Entity(name="robot")
    tabletop = Tabletop().initLine(2)
    agent = Agent(body, tabletop)
    assert agent.perceivedTabletop() is tabletop
    assert agent.perceivedBody() is body


def ttest_fast_agent_copy_with_tabletop_preserves_independent_perception():
    body = Entity(name="robot").setCoordinates(2.0, 3.0)
    tabletop = Tabletop().initLine(2)
    original = Agent(body, tabletop)
    clone = original.copy()
    assert clone.perceivedBody() is not body
    assert clone.perceivedBody().name() == "robot"
    assert clone.perceivedTabletop() is not tabletop
    assert clone.perceivedTabletop().numberOfTiles() == 2
    clone.perceivedBody().setCoordinates(9.0, 8.0)
    clone.perceivedTabletop().clear()
    assert body.position().asTuple() == (2.0, 3.0)
    assert tabletop.numberOfTiles() == 2


@pytest.mark.parametrize("size,theta", [(0.6, 0.0), (1.5, 0.4)])
def ttest_fast_entity_arrow_tip_setter_matches_shape_constructor(size, theta):
    entity = Entity().setCoordinates(2.0, -1.0)
    entity.setShapeArrowTip(size, theta)
    expected = Convex().initArrowTip(size, theta)
    assert coordinates(entity.referenceShape()) == pytest.approx(coordinates(expected))
    expected.translate(Point(2.0, -1.0))
    assert coordinates(entity.projectedShape()) == pytest.approx(coordinates(expected))


def ttest_fast_projected_shape_replaces_previous_orientation_consistently():
    entity = Entity(orientation=0.7)
    shape = Convex().initArrowTip(1.2)
    shape.rotate(0.3)
    shape.translate(Point(4.0, -2.0))
    expected = coordinates(shape)
    entity.setOutline(shape)
    assert entity.orientation() == pytest.approx(0.0)
    assert coordinates(entity.projectedShape()) == pytest.approx(expected)
    # Reapplying the declared pose must not rotate the shape a second time.
    entity.setPose(entity.position(), entity.orientation())
    assert coordinates(entity.projectedShape()) == pytest.approx(expected)


def ttest_fast_default_land_banks_do_not_share_list_mutations():
    first, second = Land(), Land()
    bank = first.bankOfEntities()
    initial_size = len(second.bankOfEntities())
    bank.append(Entity(name="extra"))
    try:
        assert len(second.bankOfEntities()) == initial_size
    finally:
        bank.pop()  # Restore the shared default even while the regression fails.


def ttest_fast_default_land_templates_do_not_share_mutable_entities():
    first, second = Land(), Land()
    template = first.bankEntity()
    original_name = template.name()
    second_name = second.bankEntity().name()
    try:
        template.setName("modified-template")
        assert second.bankEntity().name() == second_name
    finally:
        template.setName(original_name)


def ttest_fast_entity_copy_can_move_without_moving_original():
    original = Entity(name="robot").setCoordinates(2.0, 3.0)
    before = coordinates(original.projectedShape())
    clone = original.copy()
    clone.translate(Point(5.0, -1.0))
    assert clone.position().asTuple() == pytest.approx((7.0, 2.0))
    assert original.position().asTuple() == pytest.approx((2.0, 3.0))
    assert coordinates(original.projectedShape()) == pytest.approx(before)

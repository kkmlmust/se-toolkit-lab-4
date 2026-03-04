"""AI-generated unit tests for interaction filtering logic (curated)."""

from app.models.interaction import InteractionLog
from app.routers.interactions import filter_by_max_item_id


def _make_log(id: int, learner_id: int, item_id: int, kind: str = "attempt") -> InteractionLog:
    """Helper to create InteractionLog instances."""
    return InteractionLog(id=id, learner_id=learner_id, item_id=item_id, kind=kind)


# KEPT: tests filter with max_item_id = 0 (boundary case, not in existing tests)
def test_filter_with_max_item_id_zero() -> None:
    """Test filtering with max_item_id = 0."""
    interactions = [
        _make_log(1, 1, 0),
        _make_log(2, 2, 1),
        _make_log(3, 3, -1),
    ]
    result = filter_by_max_item_id(interactions=interactions, max_item_id=0)
    assert len(result) == 2  # items with item_id <= 0 (0 and -1)
    assert {i.id for i in result} == {1, 3}


# KEPT: tests negative max_item_id (edge case)
def test_filter_with_negative_max_item_id() -> None:
    """Test filtering with negative max_item_id."""
    interactions = [
        _make_log(1, 1, -5),
        _make_log(2, 2, -1),
        _make_log(3, 3, 0),
        _make_log(4, 4, 1),
    ]
    result = filter_by_max_item_id(interactions=interactions, max_item_id=-2)
    assert len(result) == 1  # only item_id = -5
    assert result[0].id == 1


# KEPT: tests when all items are above max_item_id
def test_filter_returns_empty_when_all_above_max() -> None:
    """Test when all item_id > max_item_id returns empty list."""
    interactions = [
        _make_log(1, 1, 5),
        _make_log(2, 2, 6),
        _make_log(3, 3, 7),
    ]
    result = filter_by_max_item_id(interactions=interactions, max_item_id=4)
    assert result == []


# KEPT: tests when all items are below max_item_id
def test_filter_returns_all_when_all_below_max() -> None:
    """Test when all item_id < max_item_id returns all items."""
    interactions = [
        _make_log(1, 1, 1),
        _make_log(2, 2, 2),
        _make_log(3, 3, 3),
    ]
    result = filter_by_max_item_id(interactions=interactions, max_item_id=5)
    assert len(result) == 3
    assert result == interactions


# KEPT: tests large max_item_id (all items pass)
def test_filter_with_large_max_item_id() -> None:
    """Test with max_item_id larger than any item_id."""
    interactions = [
        _make_log(1, 1, 100),
        _make_log(2, 2, 200),
        _make_log(3, 3, 300),
    ]
    result = filter_by_max_item_id(interactions=interactions, max_item_id=999)
    assert len(result) == 3
    assert result == interactions


# KEPT: tests preservation of original order
def test_filter_preserves_order() -> None:
    """Test that filtering preserves the original order of items."""
    interactions = [
        _make_log(1, 1, 3),  # above
        _make_log(2, 2, 1),  # below
        _make_log(3, 3, 2),  # equal
        _make_log(4, 4, 0),  # below
        _make_log(5, 5, 4),  # above
    ]
    result = filter_by_max_item_id(interactions=interactions, max_item_id=2)
    expected_ids = [2, 3, 4]  # original order: 2(1),3(2),4(0)
    assert [i.id for i in result] == expected_ids


# KEPT: tests handling of duplicate item_id values
def test_filter_with_duplicate_item_ids() -> None:
    """Test filtering when multiple logs have same item_id."""
    interactions = [
        _make_log(1, 1, 2),
        _make_log(2, 2, 2),
        _make_log(3, 3, 3),
        _make_log(4, 4, 2),
    ]
    result = filter_by_max_item_id(interactions=interactions, max_item_id=2)
    assert len(result) == 3  # all with item_id=2
    assert {i.id for i in result} == {1, 2, 4}

# FIXED: corrected the large integer test
def test_filter_with_max_int_values() -> None:
    """Test filtering with large integer values."""
    interactions = [
        _make_log(1, 1, 1000),
        _make_log(2, 2, 2000),
        _make_log(3, 3, 3000),
    ]
    result = filter_by_max_item_id(interactions=interactions, max_item_id=2000)
    assert len(result) == 2
    assert {i.id for i in result} == {1, 2}
    assert all(i.item_id <= 2000 for i in result)


# KEPT: tests with max_item_id = 1 (boundary case, complements existing tests)
def test_filter_boundary_max_item_id_one() -> None:
    """Test boundary condition with max_item_id = 1."""
    interactions = [
        _make_log(1, 1, 0),
        _make_log(2, 2, 1),
        _make_log(3, 3, 2),
    ]
    result = filter_by_max_item_id(interactions=interactions, max_item_id=1)
    assert len(result) == 2
    assert {i.id for i in result} == {1, 2}


# KEPT: tests mixed values with some above, some below, some equal
def test_filter_mixed_values() -> None:
    """Test with mix of values above, below, and equal to max_item_id."""
    interactions = [
        _make_log(1, 1, 10),  # above
        _make_log(2, 2, 5),   # below
        _make_log(3, 3, 7),   # equal
        _make_log(4, 4, 8),   # above
        _make_log(5, 5, 6),   # below
        _make_log(6, 6, 7),   # equal
    ]
    result = filter_by_max_item_id(interactions=interactions, max_item_id=7)
    assert len(result) == 4  # items with item_id <= 7
    expected_ids = [2, 3, 5, 6]  # item_ids: 5,7,6,7
    assert [i.id for i in result] == expected_ids


# DISCARDED: tests with different interaction kinds - but function filters only by item_id
# def test_filter_with_different_kinds() -> None:
#     """Test filtering with various interaction kinds."""
#     interactions = [
#         _make_log(1, 1, 1, kind="attempt"),
#         _make_log(2, 2, 2, kind="view"),
#         _make_log(3, 3, 1, kind="complete"),
#     ]
#     result = filter_by_max_item_id(interactions=interactions, max_item_id=1)
#     assert len(result) == 2
#     assert {i.id for i in result} == {1, 3}
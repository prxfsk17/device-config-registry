from app.diff import diff_parameters


def test_identical_parameters_have_no_differences():
    result = diff_parameters({"a": 1, "b": 2}, {"a": 1, "b": 2})
    assert result == {"added": {}, "removed": {}, "changed": {}}


def test_added_removed_and_changed():
    old = {"threshold": 10, "mode": "auto", "legacy": True}
    new = {"threshold": 12, "mode": "auto", "timeout": 30}
    assert diff_parameters(old, new) == {
        "added": {"timeout": 30},
        "removed": {"legacy": True},
        "changed": {"threshold": {"old": 10, "new": 12}},
    }


def test_nested_values_are_compared_as_a_whole():
    result = diff_parameters({"limits": {"min": 1}}, {"limits": {"min": 2}})
    assert result["changed"] == {"limits": {"old": {"min": 1}, "new": {"min": 2}}}

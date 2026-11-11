from typing import Any


def diff_parameters(old: dict[str, Any], new: dict[str, Any]) -> dict[str, Any]:
    """Compare two sets of parameters (top-level keys only).

    - added:   keys that exist only in `new`
    - removed: keys that exist only in `old`
    - changed: keys that exist in both but have different values
    """
    added_keys = sorted(new.keys() - old.keys())
    removed_keys = sorted(old.keys() - new.keys())
    changed_keys = sorted(k for k in old.keys() & new.keys() if old[k] != new[k])

    return {
        "added": {k: new[k] for k in added_keys},
        "removed": {k: old[k] for k in removed_keys},
        "changed": {k: {"old": old[k], "new": new[k]} for k in changed_keys},
    }

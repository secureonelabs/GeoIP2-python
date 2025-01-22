"""This package contains internal utilities"""

# pylint: disable=too-few-public-methods
from abc import ABCMeta
from typing import Any


class Model(metaclass=ABCMeta):
    """Shared methods for MaxMind model classes"""

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)

    # pylint: disable=too-many-branches
    def to_dict(self):
        """Returns a dict of the object suitable for serialization"""
        result = {}
        for key, value in self.__dict__.items():
            if key.startswith("_"):
                continue
            if hasattr(value, "to_dict") and callable(value.to_dict):
                if d := value.to_dict():
                    result[key] = d
            elif isinstance(value, (list, tuple)):
                ls = []
                for e in value:
                    if hasattr(e, "to_dict") and callable(e.to_dict):
                        if e := e.to_dict():
                            ls.append(e)
                    elif e is not None:
                        ls.append(e)
                if ls:
                    result[key] = ls
            # We only have dicts of strings currently. Do not bother with
            # the general case.
            elif isinstance(value, dict):
                if value:
                    result[key] = value
            elif value is not None and value is not False:
                result[key] = value

        # network is a property for performance reasons
        # pylint: disable=no-member
        if hasattr(self, "network") and self.network is not None:
            result["network"] = str(self.network)

        return result

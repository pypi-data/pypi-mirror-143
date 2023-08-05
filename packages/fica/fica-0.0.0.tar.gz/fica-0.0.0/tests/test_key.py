"""Tests for ``figurator.key``"""

import pytest

from figurator import EMPTY, Key, SUBKEYS

from .utils import assert_object_attrs


class TestKey:
    """
    Tests for ``figurator.key.Key``.
    """

    def test_constructor(self):
        """
        """
        default_attrs = {
            "description": None,
            "default": EMPTY,
            "subkeys": None,
            "type_": None,
            "allow_none": False,
        }

        name = "foo"
        key = Key(name)
        assert_object_attrs(key, {**default_attrs, "name": name})

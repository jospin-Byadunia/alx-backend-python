#!/usr/bin/env python3

"""
Unit tests for utils.py module.

This file contains unittests for:
- access_nested_map
- get_json
- memoize
"""

import unittest
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize
from unittest.mock import patch, Mock


# TestAccessNestedMap
# Test the access_nested_map function


class TestAccessNestedMap(unittest.TestCase):
    """Tests for access_nested_map function."""
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test access_nested_map with valid inputs."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Test access_nested_map raises KeyError for invalid paths."""
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(str(cm.exception), repr(path[-1]))

# TestGetJson
# Test the get_json function
# - Use the parameterized.expand decorator to parametrize test cases


class TestGetJson(unittest.TestCase):
    """Tests for get_json function."""
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch("utils.requests.get")
    def test_get_json(self, test_url, test_payload, mock_get):
        """Test get_json returns the expected payload."""
        mock_get.return_value = Mock()
        mock_get.return_value.json.return_value = test_payload

        result = get_json(test_url)

        mock_get.assert_called_once_with(test_url)
        self.assertEqual(result, test_payload)

# TestMemoize
# Test the memoize decorator
# - Create a class with a method that returns a constant value
# - Decorate a property with the memoize decorator that calls the method


class TestMemoize(unittest.TestCase):
    """Tests for memoize decorator."""

    def test_memoize(self):
        """Test that memoize calls the wrapped method only once."""
        class TestClass:
            """Helper class for testing memoize."""

            def a_method(self):
                return 42
            """Return 42."""
            @memoize
            def a_property(self):
                """Memoized property that calls a_method."""
                return self.a_method()
        with patch.object(TestClass, "a_method",
                          return_value=42) as mock_method:
            obj = TestClass()

            result1 = obj.a_property
            result2 = obj.a_property

            # Ensure the return values are correct
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

            # Ensure a_method was called only once (cached)
            mock_method.assert_called_once()

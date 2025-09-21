#!/usr/bin/env python3
"""0. Parameterize a unit test"""
import unittest
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from typing import Mapping, Sequence, Union
from unittest.mock import patch, PropertyMock
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Test suite for task 5 - 8"""
    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch('client.get_json', return_value="example.com")
    def test_org(self, org, get_json):
        """test that GithubOrgClient.org returns the correct value."""
        orgClient = GithubOrgClient(org)
        self.assertEqual(orgClient.org, get_json.return_value)
        get_json.assert_called_once()

    def test_public_repos_url(self):
        """Implement the test_public_repos_url method to unit-test
        GithubOrgClient._public_repos_url."""

        with patch.object(GithubOrgClient, 'org', new_callable=PropertyMock)\
                as mocker:
            mocker.return_value = {
                'repos_url': 'https://api.github.com/orgs/myorg/repos'
            }
            client = GithubOrgClient('myorg')
            result = client._public_repos_url
            self.assertEqual(result, 'https://api.github.com/orgs/myorg/repos')

    @patch('client.get_json', return_value=[
        {'name': 'repo1'},
        {'name': 'repo2'}
    ])
    def test_public_repos(self, smada):
        """Implement TestGithubOrgClient.test_public_repos to
        unit-test GithubOrgClient.public_repos."""
        with patch.object(GithubOrgClient, '_public_repos_url',
                          new_callable=PropertyMock,
                          return_value="https://api.github.com/myorg/repos"
                          ) as m:
            client = GithubOrgClient("alx")
            repos = client.public_repos()
            print(repos)
            self.assertEqual(repos, ['repo1', 'repo2'])
            smada.assert_called_once_with('https://api.github.com/myorg/repos')
            m.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, license, license_key, expected):
        """Implement TestGithubOrgClient.test_has_license
        to unit-test GithubOrgClient.has_license."""
        client = GithubOrgClient("org")
        res = client.has_license(license, license_key)
        self.assertEqual(res, expected)


def requests_get(*args, **kwargs):
    """
    Function that mocks requests.get function
    Returns the correct json data based on the given input url
    """
    class MockResponse:
        """
        Mock response
        """

        def __init__(self, json_data):
            self.json_data = json_data

        def json(self):
            return self.json_data

    if args[0] == "https://api.github.com/orgs/google":
        return MockResponse(TEST_PAYLOAD[0][0])
    if args[0] == TEST_PAYLOAD[0][0]["repos_url"]:
        return MockResponse(TEST_PAYLOAD[0][1])


@parameterized_class(
    ('org_payload', 'repos_payload', 'expected_repos', 'apache2_repos'),
    [(TEST_PAYLOAD[0][0], TEST_PAYLOAD[0][1], TEST_PAYLOAD[0][2],
      TEST_PAYLOAD[0][3])]
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration test for the GithubOrgClient.public_repos method
    """
    @classmethod
    def setUpClass(cls):
        """
        Set up function for TestIntegrationGithubOrgClient class
        Sets up a patcher to be used in the class methods
        """
        cls.get_patcher = patch('utils.requests.get', side_effect=requests_get)
        cls.get_patcher.start()
        cls.client = GithubOrgClient('google')

    @classmethod
    def tearDownClass(cls):
        """
        Tear down resources set up for class tests.
        Stops the patcher that had been started
        """
        cls.get_patcher.stop()

    def test_public_repos(self):
        """
        Test public_repos method without license
        """
        self.assertEqual(self.client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """
        Test public_repos method with license
        """
        self.assertEqual(
            self.client.public_repos(license="apache-2.0"),
            self.apache2_repos)

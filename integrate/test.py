"""Integration tests for `maas.client`."""

from http import HTTPStatus
import io
from itertools import repeat
import random

from maas.client import (
    bones,
    viscera,
)
from maas.client.testing import (
    make_name_without_spaces,
    TestCase,
)
from maas.client.utils import (
    creds,
    profiles,
)
from testtools.matchers import (
    AllMatch,
    Equals,
    IsInstance,
    MatchesAll,
    MatchesStructure,
)


kiB = 2 ** 10
MiB = 2 ** 20


def scenarios():
    with profiles.ProfileStore.open() as config:
        return tuple(
            (profile.name, dict(profile=profile))
            for profile in map(config.load, config)
        )


class IntegrationTestCase(TestCase):

    scenarios = scenarios()

    def setUp(self):
        super(IntegrationTestCase, self).setUp()
        self.session = bones.SessionAPI.fromProfile(self.profile)
        self.origin = viscera.Origin(self.session)


class TestAccount(IntegrationTestCase):

    def test__create_and_delete_credentials(self):
        credentials = self.origin.Account.create_credentials()
        self.assertThat(credentials, IsInstance(creds.Credentials))
        self.origin.Account.delete_credentials(credentials)


class TestBootResources(IntegrationTestCase):

    def test__list_boot_resources(self):
        boot_resources = self.origin.BootResources.read()
        self.assertThat(boot_resources, MatchesAll(
            IsInstance(self.origin.BootResources),
            AllMatch(IsInstance(self.origin.BootResource)),
        ))

    def test__create_and_delete_boot_resource(self):
        chunk = random.getrandbits(8 * 128).to_bytes(128, "big")
        content = b"".join(repeat(chunk, 5 * MiB // len(chunk)))
        boot_resource = self.origin.BootResources.create(
            make_name_without_spaces("ubuntu", "/"), "amd64/generic",
            io.BytesIO(content))
        self.assertThat(boot_resource, IsInstance(self.origin.BootResource))
        boot_resource.delete()
        error = self.assertRaises(
            bones.CallError, self.origin.BootResource.read, boot_resource.id)
        self.assertThat(error, MatchesStructure(
            status=Equals(HTTPStatus.NOT_FOUND)))


class TestBootSources(IntegrationTestCase):

    def test__create_and_delete_source_with_keyring_filename(self):
        source_url = make_name_without_spaces("http://maas.example.com/")
        keyring_filename = make_name_without_spaces("keyring-filename")
        boot_source = self.origin.BootSources.create(
            source_url, keyring_filename=keyring_filename)
        self.assertThat(boot_source, IsInstance(self.origin.BootSource))
        boot_source.delete()
        error = self.assertRaises(
            bones.CallError, self.origin.BootSource.read, boot_source.id)
        self.assertThat(error, MatchesStructure(
            status=Equals(HTTPStatus.NOT_FOUND)))

    def test__create_and_delete_source_with_keyring_data(self):
        source_url = make_name_without_spaces("http://maas.example.com/")
        keyring_data = make_name_without_spaces("keyring-data").encode()
        boot_source = self.origin.BootSources.create(
            source_url, keyring_data=io.BytesIO(keyring_data))
        self.assertThat(boot_source, IsInstance(self.origin.BootSource))
        boot_source.delete()
        error = self.assertRaises(
            bones.CallError, self.origin.BootSource.read, boot_source.id)
        self.assertThat(error, MatchesStructure(
            status=Equals(HTTPStatus.NOT_FOUND)))


# TestBootSourceSelections
# TestControllers
# TestDevices


class TestEvents(IntegrationTestCase):

    def test__query_events(self):
        events = self.origin.Events.query()
        self.assertThat(events, IsInstance(self.origin.Events))
        events = events.prev()
        self.assertThat(events, IsInstance(self.origin.Events))
        events = events.next()
        self.assertThat(events, IsInstance(self.origin.Events))


# TestFiles
# TestMAAS
# TestMachines
# TestTags
# TestTesting
# TestUsers
# TestVersion
# TestZones


# End.

# PyTest Documentation: https://docs.pytest.org/en/8.2.x/how-to/index.html

import unittest
from unittest.mock import Mock, patch

import xml.etree.ElementTree as ET
from requests.exceptions import Timeout

from services.bgg_service import (
    BGGClient,
    BGGCollectionItem,
    BGGException,
    BGGUser,
)


class TestBGGClient(unittest.TestCase):
    @patch("services.bgg_service.requests.get")
    def test_get_xml_data_success(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = (
            '<user id="123" name="testuser" termsofuse="example"></user>'
        )
        mock_get.return_value = mock_response
        response = BGGClient.get_xml_data("user", {"username": "testuser"})
        self.assertEqual(
            response.attrib.get("name"),
            ET.fromstring(mock_response.content).attrib.get("name"),
        )

    @patch("services.bgg_service.requests.get")
    def test_get_xml_data_failure(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        with self.assertRaises(BGGException) as context:
            BGGClient.get_xml_data("user", {"username": "invaliduser"})

        self.assertEqual(str(context.exception), "Error fetching data: 404")

    @patch("services.bgg_service.requests.get")
    def test_get_xml_data_timeout(self, mock_get):
        mock_get.side_effect = Timeout

        with self.assertRaises(Timeout):
            BGGClient.get_xml_data("user", {"username": "testuser"})


class TestBGGUser(unittest.TestCase):
    def setUp(self):
        self.xml_data = ET.fromstring("""
        <user id="123" name="testuser" termsofuse="example">
            <firstname value="John" />
            <lastname value="Doe" />
            <avatarlink value="http://example.com/avatar.jpg" />
            <yearregistered value="2020" />
            <lastlogin value="2021-01-01" />
            <stateorprovince value="SomeState" />
            <country value="SomeCountry" />
            <webaddress value="http://example.com" />
            <xboxaccount value="johnxbox" />
            <wiiaccount value="johnwii" />
            <psnaccount value="johnpsn" />
            <battlenetaccount value="johnbattlenet" />
            <steamaccount value="johnsteam" />
            <traderating value="100" />
            <buddies>
                <buddy buddy_id="1" name="buddy1" />
            </buddies>
            <guilds>
                <guild guild_id="1" name="guild1" />
            </guilds>
            <hot>
                <item id="1" type="boardgame" rank="1" name="Game1" />
            </hot>
            <top>
                <item id="1" type="boardgame" rank="1" name="TopGame1" />
            </top>
        </user>
        """)
        self.user = BGGUser(self.xml_data)

    def test_user_initialization(self):
        self.assertEqual(self.user.user_id, "123")
        self.assertEqual(self.user.name, "testuser")
        self.assertEqual(self.user.firstname, "John")
        self.assertEqual(self.user.lastname, "Doe")
        self.assertEqual(self.user.avatarlink, "http://example.com/avatar.jpg")
        self.assertEqual(self.user.yearregistered, "2020")
        self.assertEqual(self.user.lastlogin, "2021-01-01")
        self.assertEqual(self.user.stateorprovince, "SomeState")
        self.assertEqual(self.user.country, "SomeCountry")
        self.assertEqual(self.user.webaddress, "http://example.com")
        self.assertEqual(self.user.xboxaccount, "johnxbox")
        self.assertEqual(self.user.wiiaccount, "johnwii")
        self.assertEqual(self.user.psnaccount, "johnpsn")
        self.assertEqual(self.user.battlenetaccount, "johnbattlenet")
        self.assertEqual(self.user.steamaccount, "johnsteam")
        self.assertEqual(self.user.traderating, "100")

        self.assertEqual(len(self.user.buddies), 1)
        self.assertEqual(self.user.buddies[0].buddy_id, "1")
        self.assertEqual(self.user.buddies[0].name, "buddy1")

        self.assertEqual(len(self.user.guilds), 1)
        self.assertEqual(self.user.guilds[0].guild_id, "1")
        self.assertEqual(self.user.guilds[0].name, "guild1")

        self.assertEqual(len(self.user.hot), 1)
        self.assertEqual(self.user.hot[0].id, "1")
        self.assertEqual(self.user.hot[0].type, "boardgame")
        self.assertEqual(self.user.hot[0].rank, "1")
        self.assertEqual(self.user.hot[0].name, "Game1")

        self.assertEqual(len(self.user.top), 1)
        self.assertEqual(self.user.top[0].id, "1")
        self.assertEqual(self.user.top[0].type, "boardgame")
        self.assertEqual(self.user.top[0].rank, "1")
        self.assertEqual(self.user.top[0].name, "TopGame1")

    @patch("services.bgg_service.BGGClient.get_xml_data")
    def test_get_user_info(self, mock_get_xml_data):
        mock_response = Mock()
        mock_response.content = self.xml_data
        mock_get_xml_data.return_value = self.xml_data

        user = BGGUser.get_user_info("testuser", buddies=1, guilds=1, hot=1, top=1)
        self.assertEqual(user.name, "testuser")


class TestBGGCollectionItem(unittest.TestCase):
    @patch("services.bgg_service.requests.get")
    @patch("services.bgg_service.BGGClient.get_xml_data")
    def test_fetch_collection_success(self, mock_fromstring, mock_get):
        xml_response = """
        <items>
            <item objectid="1">
                <name>Game One</name>
                <yearpublished>2020</yearpublished>
                <image>http://example.com/image1.jpg</image>
                <thumbnail>http://example.com/thumbnail1.jpg</thumbnail>
                <numplays>5</numplays>
                <stats>
                    <rating value="8.0"/>
                </stats>
            </item>
            <item objectid="2">
                <name>Game Two</name>
                <yearpublished>2019</yearpublished>
                <image>http://example.com/image2.jpg</image>
                <thumbnail>http://example.com/thumbnail2.jpg</thumbnail>
                <numplays>10</numplays>
                <stats>
                    <rating value="7.5"/>
                </stats>
            </item>
        </items>
        """

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = xml_response
        mock_get.return_value = mock_response

        mock_root = ET.fromstring(xml_response)
        mock_fromstring.return_value = mock_root

        items = BGGCollectionItem.fetch_collection("testuser", own=1, rated=1)

        self.assertEqual(len(items), 2)
        self.assertEqual(items[0].name, "Game One")
        self.assertEqual(items[0].yearpublished, "2020")
        self.assertEqual(items[0].numplays, "5")

        self.assertEqual(items[1].name, "Game Two")
        self.assertEqual(items[1].yearpublished, "2019")
        self.assertEqual(items[1].numplays, "10")

    @patch("services.bgg_service.requests.get")
    @patch("services.bgg_service.ET.fromstring")
    def test_fetch_collection_error(self, mock_fromstring, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        with self.assertRaises(BGGException):
            BGGCollectionItem.fetch_collection("testuser", own=1, rated=1)

    @patch("services.bgg_service.requests.get")
    @patch("services.bgg_service.BGGClient.get_xml_data")
    def test_fetch_collection_queued(self, mock_fromstring, mock_get):
        mock_get.side_effect = [
            Mock(status_code=202),
            Mock(
                status_code=200,
                content="""
                <items>
                    <item objectid="1">
                        <name>Game One</name>
                    </item>
                </items>
                """,
            ),
        ]

        mock_root = ET.fromstring("""
        <items>
            <item objectid="1">
                <name>Game One</name>
            </item>
        </items>
        """)
        mock_fromstring.return_value = mock_root

        items = BGGCollectionItem.fetch_collection("testuser", own=1, rated=1)

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].name, "Game One")


if __name__ == "__main__":
    unittest.main()

import time
import xml.etree.ElementTree as ET
import requests


class BGGException(Exception):
    pass


class BGGClient:
    BASE_URL = "https://boardgamegeek.com/xmlapi2/"

    @classmethod
    def get_xml_data(cls, endpoint: str, params: dict):
        while True:
            url = f"{cls.BASE_URL}{endpoint}"
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 202:
                time.sleep(5)
            elif response.status_code != 200:
                raise BGGException(f"Error fetching data: {response.status_code}")
            else:
                break

        return ET.fromstring(response.content)


class BGGUser(BGGClient):
    class Buddy:
        def __init__(self, **kwargs):
            self.buddy_id = kwargs.get("buddy_id")
            self.name = kwargs.get("name")

    class Guild:
        def __init__(self, **kwargs):
            self.guild_id = kwargs.get("guild_id")
            self.name = kwargs.get("name")

    class Hot:
        def __init__(self, **kwargs):
            self.id = kwargs.get("id")
            self.type = kwargs.get("type")
            self.rank = kwargs.get("rank")
            self.name = kwargs.get("name")

    class Top:
        def __init__(self, **kwargs):
            self.id = kwargs.get("id")
            self.type = kwargs.get("type")
            self.rank = kwargs.get("rank")
            self.name = kwargs.get("name")

    def __init__(self, root: ET.Element):
        self.user_id = root.attrib.get("id")
        self.name = root.attrib.get("name")
        self.terms_of_use = root.attrib.get("termsofuse")

        self.firstname = self.get_element_value(root, "firstname")
        self.lastname = self.get_element_value(root, "lastname")
        self.avatarlink = self.get_element_value(root, "avatarlink")
        self.yearregistered = self.get_element_value(root, "yearregistered")
        self.lastlogin = self.get_element_value(root, "lastlogin")
        self.stateorprovince = self.get_element_value(root, "stateorprovince")
        self.country = self.get_element_value(root, "country")
        self.webaddress = self.get_element_value(root, "webaddress")
        self.xboxaccount = self.get_element_value(root, "xboxaccount")
        self.wiiaccount = self.get_element_value(root, "wiiaccount")
        self.psnaccount = self.get_element_value(root, "psnaccount")
        self.battlenetaccount = self.get_element_value(root, "battlenetaccount")
        self.steamaccount = self.get_element_value(root, "steamaccount")
        self.traderating = self.get_element_value(root, "traderating")

        self.buddies = (
            [self.Buddy(**buddy.attrib) for buddy in root.find("buddies")]
            if root.find("buddies") is not None
            else []
        )
        self.guilds = (
            [self.Guild(**guild.attrib) for guild in root.find("guilds")]
            if root.find("guilds") is not None
            else []
        )
        self.hot = (
            [self.Hot(**hot.attrib) for hot in root.find("hot")]
            if root.find("hot") is not None
            else []
        )
        self.top = (
            [self.Top(**top.attrib) for top in root.find("top")]
            if root.find("top") is not None
            else []
        )

    @staticmethod
    def get_element_value(root: ET.Element, tag: str) -> str:
        element = root.find(tag)
        return element.attrib.get("value") if element is not None else ""

    @classmethod
    def get_user_info(cls, username, **filters):
        url_params = {"username": username} | filters
        data = cls.get_xml_data("user", url_params)
        return BGGUser(data)


class BGGCollectionItem(BGGClient):
    def __init__(self, xml_item: ET.Element):
        self.id = xml_item.attrib.get("objectid")
        self.name = self.get_element_text(xml_item, "name")
        self.yearpublished = self.get_element_text(xml_item, "yearpublished")
        self.image = self.get_element_text(xml_item, "image")
        self.thumbnail = self.get_element_text(xml_item, "thumbnail")
        self.numplays = self.get_element_text(xml_item, "numplays")

    @staticmethod
    def get_element_text(parent: ET.Element, tag: str) -> str:
        element = parent.find(tag)
        return element.text if element is not None else ""

    @classmethod
    def fetch_collection(cls, username, **filters):
        params = {"username": username} | filters
        data = cls.get_xml_data("collection", params)
        return [BGGCollectionItem(item) for item in data.iter("item")]

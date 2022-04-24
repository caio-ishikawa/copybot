import requests
import io
import os
from dotenv import load_dotenv
from PIL import Image


class SlackClient:
    load_dotenv()
    tesseract_path = os.getenv("TESSERACT_PATH")
    client_id = os.getenv("CLIENT_ID")
    base_url = os.getenv("BASE_URL")
    auth_url = os.getenv("AUTH_URL")
    auth_token = os.getenv("AUTH_TOKEN")


    @classmethod
    def get_file_link(cls, channel_id: str, index: int):
        """
        Returns list of files per channel ID
        """
        url = f"{cls.base_url}/api/files.list?channel={channel_id}"

        headers = {
            "Authorization": f"Bearer {cls.auth_token}",
        }

        response = requests.get(url=url, headers=headers)

        if response.status_code != 200:
            return None

        files = response.json()["files"]
        return files[-1]["url_private"]


    @classmethod
    def get_img(cls, url: str):
        """
        Makes GET request to slack image URL and converts to Pillow Image object
        """
        headers = {
            "Authorization": f"Bearer {cls.auth_token}",
        }

        res = requests.get(url, headers=headers)

        if res.status_code != 200:
            return None 

        return Image.open(io.BytesIO(res.content))


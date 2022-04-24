from exceptions import unexpected_err
from services import parse_image
from slack_client import SlackClient

from exceptions import FileNotFoundErr, ImageNotFoundErr


def convert(channel_id: str, index: int):
    file_link = SlackClient().get_file_link(channel_id, index)
    if file_link is None:
        return FileNotFoundErr

    image = SlackClient().get_img(file_link)
    if image is None:
        return ImageNotFoundErr
    
    try:
        return parse_image(image)
    except Exception as e:
        return unexpected_err(e)

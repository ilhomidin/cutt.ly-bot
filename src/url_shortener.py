from typing import Union

import urllib3
import orjson


def _api_call(api_key: str, url: str) -> urllib3.HTTPResponse:
    """Make API call to cutt.ly

    Args:
        api_key (str): user API key
        url (str): URL you want to shorten

    Returns:
        urllib3.HTTPResponse: urrlib repsponse
    """
    http = urllib3.PoolManager()
    return http.request(
        "GET",
        "http://cutt.ly/api/api.php?key={}&short={}".format(api_key, url),
    )


def _parse_json(raw: Union[str, bytes, bytearray]) -> dict:
    """Parse json

    Args:
        raw (Union[str, bytes, bytearray]): data

    Returns:
        dict: serialized json
    """
    try:
        json = orjson.loads(raw)
    except orjson.JSONDecodeError:
        json = {"url": {"status": 8}}
    return json


def shorten(api_key: str, url: str) -> str:
    """Try to make given url shorten

    Args:
        api_key (str): user API key
        url (str): URL you want to shorten

    Raises:
        ValueError: cutt.ly API error
        SystemError: invalid status ID

    Returns:
        str: url
    """
    api_response = _parse_json(_api_call(api_key, url).data)
    status = api_response["url"]["status"]
    if status == 1:
        return url
    elif status == 2:
        raise ValueError(f"{url} is not a link.")
    elif status == 5:
        raise ValueError(
            f"{url} has not passed the validation. Includes invalid characters."
        )
    elif status == 6:
        raise ValueError(f"{url} provided is from a blocked domain.")
    elif status == 7:
        return api_response["url"]["shortLink"]
    elif status == 8:
        raise ValueError(f"Can't make {url} shorten.")
    else:
        raise SystemError(f"Internal bot error. Please come back in 5 minutes.")


__all__ = ["shorten"]

import requests
from opet.exceptions import Http200Error
import json


def http_get(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Origin': 'https://www.opet.com.tr',
        'Host': 'api.opet.com.tr',
        'Channel': 'Web',
        'Accept-Language': 'tr-TR'
    }
    r = requests.get(url, headers=headers, verify=True)
    if r.status_code != 200:
        raise Http200Error("HttpStatusCode is not 200.")
    return r.json()


def to_json(data):
    return json.dumps(data, ensure_ascii=False, indent=2)


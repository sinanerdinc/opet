from datetime import datetime, timezone, timedelta
import requests
from opet.exceptions import Http200Error
import json


def yesterday():
    now_datetime = datetime.now(timezone.utc)
    six_hours_delta = timedelta(days=1)
    target_datetime = now_datetime - six_hours_delta
    output_datetime_str = target_datetime.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    return output_datetime_str


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


if __name__ == '__main__':
    print(yesterday())

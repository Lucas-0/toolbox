# credit: https://github.com/daidr/paimon-webext
# credit: https://github.com/xwwwb/GenshinResinAlert
import json
from typing import Literal, Any
import hashlib
import random
import time
from typing import List, Tuple

import requests

session = requests.session()

def get_server(uid: int) -> str:
    if str(uid).startswith('1'):
        return 'cn_gf01'  # 天空岛
    elif str(uid).startswith('2'):
        return 'cn_gf01'  # 天空岛
    elif str(uid).startswith('5'):
        return 'cn_qd01'  # 世界树
    else:
        return ''


class Headers:
    def __init__(self) -> None:
        pass

    @staticmethod
    def md5(text: str) -> str:
        md5 = hashlib.md5()
        md5.update(text.encode())
        return md5.hexdigest()

    def getCookie(self) -> Tuple[str, int]:
        return self.cookies[self.cookie_idx], self.cookie_idx

    def create_dynamic_secret(self, query: dict, body: str) -> str:
        parameters: List[str] = [
            f'{k}={query[k]}' for k in sorted(query.keys())]
        q = '&'.join(parameters)

        salt: str = 'xV8v4Qu54lUKrEYFZkJhB8cuOh9Asafs'
        time_: str = str(int(time.time()))
        random_ = str(random.randint(100000, 199999))

        check: str = self.md5(
            f"salt={salt}&t={time_}&r={random_}&b={body}&q={q}")

        return ','.join((time_, random_, check))

    def new(self, cookie: str, query: dict, body: str = '') -> dict:
        ds = self.create_dynamic_secret(query, body)
        version: str = '2.11.1'
        return {
            'Accept': 'application/json, text/plain, */*',
            'DS': ds,
            'Origin': 'https://webstatic.mihoyo.com',
            'x-rpc-app_version': version,
            'User-Agent': f'Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.70 Mobile Safari/537.36 miHoYoBBS/{version}',
            'x-rpc-client_type': '5',
            'cookie': cookie,
            'Referer': 'https://webstatic.mihoyo.com/app/community-game-records/index.html?v=6',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,en-US;q=0.8',
            'X-Requested-With': 'com.mihoyo.hyperion'
        }

headers = Headers()

def request(url: str, cookie: str, method: Literal['GET', 'POST'] = 'GET', **kwargs: Any):
    query: dict = kwargs.get('params', {})
    body = kwargs.get('data', '')
    response = session.request(method, url, headers=headers.new(
        cookie, query, body), **kwargs)
    return response


def main() -> None:

    uid = '' # Fill in these two
    cookie = ''
    server: str = 'cn_gf01'
    body: dict = {
        'server': server,
        'role_id': uid
    }

    url = 'https://api-takumi-record.mihoyo.com/game_record/app/genshin/api/dailyNote'
    # url = 'https://api-takumi.mihoyo.com/binding/api/getUserGameRolesByCookie?game_biz=hk4e_cn' # RoleInfo
    data = request(url, params=body, cookie=cookie).text
    data = json.loads(data)
    resin = data.get('data').get('current_resin')

    seconds = int(data.get('data').get('resin_recovery_time'))
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    message = f"现有{resin}个树脂，预计回满需要{h}小时{m}分钟。"
    print(message)
    # return message

if __name__ == '__main__':
    main()

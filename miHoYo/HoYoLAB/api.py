
import json
import requests

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.62'
}

api = {
    'ContentList': {
        'bh3': 'https://bh3.mihoyo.com/content/bh3Cn/getContentList',
        'bh3_global': 'https://honkaiimpact3.mihoyo.com/content/bh3Sea/getContentList',
        'ys': "https://ys.mihoyo.com/content/ysCn/getContentList"
    },
    'getContent': {
        'ys': "https://ys.mihoyo.com/content/ysCn/getContent"
    }
}


def getContentList(params: dict):
    data = {
        'total': 0,
        'list': []
    }
    url: str
    if params['channelId'] == 177:
        url = api['ContentList']['bh3']
    elif params['channelId'] == 10:
        url = api['ContentList']['ys']
    else:
        url = api['ContentList']['bh3_global']

    while True:
        jsn = json.loads(
            requests.get(
                url=url,
                params=params,
                headers=header
            ).content
        )

        # 请求失败
        if jsn['retcode'] != 0:
            print(jsn['retcode'], "\t", jsn['message'])
            print(f'\turl={url} params={params}')
            cnt = -1
            break

        # 合并
        data['total'] = jsn['data']['total']
        data['list'].extend(jsn['data']['list'])

        # 空列表
        if not jsn['data']['list']:
            break

        # 页面递增
        params["pageNum"] += 1
    return data


def getContent(params: dict):
    resp = json.loads(
        requests.get(
            url=api['getContent']['ys'],
            headers=header,
            params=params
        ).content
    )
    # 请求失败
    if resp['retcode'] != 0:
        return resp
    return resp['data']


if __name__ == "__main__":
    param = {
        "pageSize": 20,
        "pageNum": 1,
        "channelId": 10
    }
    data = getContentList(params=param)
    print(data['total'])
    print(len(data['list']))

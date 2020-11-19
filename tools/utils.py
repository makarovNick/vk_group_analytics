from datetime import datetime, timedelta
import asyncio
import time
import json

import requests
import aiohttp
from rich.progress import track

from config import VK_API_VERSION, VK_ACCESS_TOKEN

asyncio.coroutines._DEBUG = True

class VKException(Exception):
    '''Ошибка VKAPI'''
    pass


class VKBadRequest(VKException):
    '''Ошибка запроса/сервера'''
    pass

class VKGroupError(VKException):
    '''Ошибка при запросе информации о группе'''
    pass


async def async_get(method, session, **kwargs):
    async with session.get(f'https://api.vk.com/method/{method}', params=kwargs) as response:
        return await response.read()

async def async_vk_request(method, session, **kwargs):
    '''VK API async'''
    response = await async_get(method, session, **kwargs)
    ACCESS_DENIED = 15
    GROUP_BLOCKED = 203
    try:
        result = json.loads(response.decode('utf-8'))
    except:
        raise VKBadRequest(response.decode('utf-8'))

    if 'error' in result:
        raise VKBadRequest(result['error']['error_msg'])

    if 'execute_errors' in result:
        if result['execute_errors'][0]['error_code'] in [ACCESS_DENIED, GROUP_BLOCKED]:
            raise VKGroupError(result['execute_errors'][0]['error_msg'])
        raise VKBadRequest(result['execute_errors'][0]['error_msg'])

    return result

async def __async_get_members(group_id, session, count, offset=0, fields=[]):
    max_api_calls = 25 # Внутри code может содержаться не более 25 обращений к методам API.
    if len(fields) > 7:
        max_api_calls = 20
    if len(fields) > 3:
        max_api_calls = 22 # API ограничивает длину request URI

    members = []

    code = f'''
        var offset = {offset};
        var i = 0;
        var p= [];
        var temp = 1001;
        while (offset < {count} && i < {max_api_calls})
        {{
            if ({count} - offset > 1000)
            {{
                temp = 1000;
            }}
            else
            {{
                temp = {count} - offset;
            }}
            p = p + [API.groups.getMembers({{group_id:{group_id},offset:offset,count:temp,fields:{fields}}})];
            offset = offset + temp;
            i = i + 1;
        }}
        return p;'''
    try:
        response = await async_vk_request('execute',
                                          session,
                                          code=code,
                                          access_token=VK_ACCESS_TOKEN,
                                          v=VK_API_VERSION)
    except VKBadRequest as e:
        print('EXCEPTION : ', e)
        # time.sleep(2) # crutch
        await asyncio.sleep(2)
        response = await async_vk_request('execute',
                                          session,
                                          code=code,
                                          access_token=VK_ACCESS_TOKEN,
                                          v=VK_API_VERSION)

    for r in response['response']:
        members.extend(r['items'])

    return members

async def async_get_members(group_id, count=-1, offset=0, fields=[]):
    max_api_calls = 25 # Внутри code может содержаться не более 25 обращений к методам API.
    req_per_sec = 3 # magic constant
    if len(fields) > 7:
        req_per_sec = 5
        max_api_calls = 20
    if len(fields) > 3:
        req_per_sec = 4
        max_api_calls = 22
    COUNT_AT_TIME = max_api_calls * req_per_sec * 1000
    members = []
    if count == -1:
        count = get_group_info(group_id, fields=['members_count'])['members_count']
    async with aiohttp.ClientSession() as session:
        for j in track(range(0, count, COUNT_AT_TIME), description='Requesting members...'):
            members.extend(await asyncio.gather(
                *[__async_get_members(group_id, session, count=count, offset=i, fields=fields)
                  for i in range(j, min(count, j + COUNT_AT_TIME), max_api_calls * 1000)]
            ))
            await asyncio.sleep(1)
    members = [item for sublist in members for item in sublist]

    return members


def get_group_stats(group_id,
                    timestamp_from,
                    timestamp_to=datetime.today().timestamp()):#.replace(hour=0, minute=0, second=0, microsecond=0).timestamp()):
    try:
        response = vk_request('stats.get',
                              group_id=group_id,
                              timestamp_from=timestamp_from,
                              timestamp_to=timestamp_to,
                              access_token=VK_ACCESS_TOKEN,
                              v=VK_API_VERSION)
    except:
        return [] # no access

    return response['response']

def vk_request(method, **kwargs):
    '''VK API'''
    response = requests.get(f'https://api.vk.com/method/{method}', params=kwargs)
    ACCESS_DENIED = 15
    GROUP_BLOCKED = 203

    try:
        result = response.json()
    except:
        raise VKBadRequest(response.text)

    if 'error' in result:
        raise VKBadRequest(result['error']['error_msg'])

    if 'execute_errors' in result:
        if result['execute_errors'][0]['error_code'] in [ACCESS_DENIED, GROUP_BLOCKED]:
            raise VKGroupError(result['execute_errors'][0]['error_msg'])
        raise VKBadRequest(result['execute_errors'][0]['error_msg'])

    return result


def get_group_info(group_id, fields=[]):
    response = vk_request('groups.getById',
                          access_token=VK_ACCESS_TOKEN,
                          fields=','.join(fields),
                          group_id=group_id,
                          v=VK_API_VERSION)

    return response['response'][0]

def get_group_posts(group_id, count=100, offset=0):
    '''Возвращает список записей со стены пользователя или сообщества. vk.api : wall.get'''
    current_count = 0
    posts = []
    while current_count < count:
        response = vk_request('wall.get',
                              owner_id=f'-{group_id}',
                              count=min(count - current_count, 100),
                              access_token=VK_ACCESS_TOKEN,
                              offset=offset + current_count,
                              filter='owner',
                              extended=0,
                              v=VK_API_VERSION)
        posts.extend(response['response']['items'])
        if response['response']['count'] < 100:
            break


        current_count += 100

    return posts

def get_group_id(screen_name):
    '''Определяет тип объекта (пользователь, сообщество, приложение)
        и его идентификатор по короткому имени screen_name.
    vk.api : utils.resolveScreenName'''
    response = vk_request('utils.resolveScreenName',
                          access_token=VK_ACCESS_TOKEN,
                          screen_name=screen_name,
                          v=VK_API_VERSION)

    return response['response']['object_id']

def get_group_members(group_id, count=-1, offset=0, fields=[]):
    '''Возвращает список участников сообщества. vk.api : groups.getMembers
    count -- количество участников сообщества, информацию о которых необходимо получить. -1 - все
    sort -- сортировка, с которой необходимо вернуть список участников. Может принимать значения
    offset -- смещение, необходимое для выборки определенного подмножества участников.
    fields -- список дополнительных полей, которые необходимо вернуть.
    '''
    max_api_calls = 25 # Внутри code может содержаться не более 25 обращений к методам API.
    if len(fields) > 7:
        max_api_calls = 20
    if len(fields) > 3:
        max_api_calls = 22 # API ограничивает память

    members = []

    if count == -1:
        count = get_group_info(group_id, fields=['members_count'])['members_count']
    for _ in track(range(0, count, max_api_calls * 1000), description="Requesting members..."):
        code = f'''
            var offset = {offset};
            var i = 0;
            var p= [];
            var temp = 1001;
            while (offset < {count} && i < {max_api_calls})
            {{
                if ({count} - offset > 1000)
                {{
                    temp = 1000;
                }}
                else
                {{
                    temp = {count} - offset;
                }}
                p = p + [API.groups.getMembers({{group_id:{group_id},offset:offset,count:temp,fields:{fields}}})];
                offset = offset + temp;
                i = i + 1;
            }}
            return p;'''
        response = vk_request('execute',
                              code=code,
                              access_token=VK_ACCESS_TOKEN,
                              v=VK_API_VERSION)
        offset += 1000 * max_api_calls

        for r in response['response']:
            members.extend(r['items'])

    return members

def get_users_info(user_ids, fields=[]):
    max_count = 500 # ограничение request URI
    if len(fields) < 8:
        max_count = 400

    users_info = []
    for i in track(range(0, len(user_ids), max_count)):
        response = vk_request('users.get',
                              user_ids=','.join(list(map(str, user_ids[i:i + max_count]))),
                              access_token=VK_ACCESS_TOKEN,
                              v=VK_API_VERSION,
                              fields=fields)
        users_info.extend(response['response'])
        time.sleep(0.1)

    return users_info

def date_n_days_ago(n):
    return datetime.today() - timedelta(days=n)

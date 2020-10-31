from rich.progress import track
from tqdm import tqdm

from config import VK_API_VERSION, VK_ACCESS_TOKEN
import json
from datetime import datetime, timedelta
import requests

def get_group_stats(group_id, timestamp_from, timestamp_to=datetime.timestamp(datetime.today()), stats_groups=[]):
    try:
        response = vk_request('stats.get', 
                group_id=group_id,
                timestamp_from = timestamp_from,
                timestamp_to = timestamp_to,
                stats_groups = stats_groups,
                access_token = VK_ACCESS_TOKEN,
                v = VK_API_VERSION)
    except:
        response = {'response' : None} # no access

    return response['response']

def vk_request(method, **kwargs):
    '''VK API'''
    response = requests.get(f'https://api.vk.com/method/{method}', params = kwargs)
    result = response.json()
    if 'error' in result:
        raise Exception(result['error']['error_msg'])

    return result

def get_group_info(group_id, fields = []):
    response = vk_request('groups.getById', 
                              access_token = VK_ACCESS_TOKEN,
                              fields = ','.join(fields),
                              group_id = group_id,
                              v = VK_API_VERSION)

    return response['response'][0]

def get_group_posts(group_id, count=100, offset=0):
    '''Возвращает список записей со стены пользователя или сообщества. vk.api : wall.get'''
    current_count = 0
    posts = []
    while current_count < count:
        response = vk_request('wall.get', 
                           owner_id = f'-{group_id}', 
                           count = min(count - current_count, 100), 
                           access_token = VK_ACCESS_TOKEN, 
                           offset = offset + current_count,
                           filter = 'owner',
                           extended = 0,
                           v = VK_API_VERSION)
        if response['response']['count'] < 100:
            break

        posts.extend(response['response']['items'])
        
        current_count += min(count - current_count, 100)
        
    return posts

def get_group_id(screen_name):
    '''Определяет тип объекта (пользователь, сообщество, приложение) и его идентификатор по короткому имени screen_name.
    vk.api : utils.resolveScreenName'''
    response = vk_request('utils.resolveScreenName', 
                              access_token = VK_ACCESS_TOKEN,
                              screen_name = screen_name,
                              v = VK_API_VERSION)

    return response['response']['object_id']

def get_group_members_2(group_id, count = -1, offset=0, fields=[]):
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
        count = get_group_info(group_id, fields = ['members_count'])['members_count']
    for _ in tqdm(range(0, count, max_api_calls * 1000), desc="Requesting members..."):
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
                           code = code,
                           access_token = VK_ACCESS_TOKEN,
                           v = VK_API_VERSION)
        offset += 1000 * max_api_calls
        
        for r in response['response']:
            members.extend(r['items'])
        
    return members

def inactive_users(users, days=31):
    date_N_days_ago = int((datetime.now() - timedelta(days=days)).timestamp())
    return users.loc[users.last_seen < date_N_days_ago].shape[0]

def posts_per_day(group_id, days=7):
    limit = int((datetime.today() - timedelta(days=days)).timestamp())
    offset = 100
    posts = get_group_posts(group_id)
    while True:
        temp = get_group_posts(group_id, offset = offset)
        if len(temp) == 0:
            break
        posts.extend(temp)
        if posts[-1]['date'] < limit:
            break
        offset += len(temp)

    while len(posts) != 0 and posts[-1]['date'] < limit:
        posts.pop()
    
    return len(posts) / days
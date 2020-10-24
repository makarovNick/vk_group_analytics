from config import VK_API_VERSION, VK_ACCESS_TOKEN
import json
import time
from datetime import datetime
import requests

def vk_request(method, **kwargs):
    '''VK API'''
    response = requests.get(f'https://api.vk.com/method/{method}', params = kwargs)
    result = response.json()
    if 'error' in result:
        raise Exception(result['error']['error_msg'])
    return response.json()

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

    if len(response['response']) == 0:
        raise Exception(f'No group or user with screen_name : {screen_name}')
#     elif response['response']['type'] == 'user':
#         raise Exception(f'{screen_name} is user')
    return response['response']['object_id']

def get_group_members(group_id, count = 1000, offset=0, sort='id_asc', fields=[]):
    '''Возвращает список участников сообщества. vk.api : groups.getMembers
    count -- количество участников сообщества, информацию о которых необходимо получить. -1 - все
    sort -- сортировка, с которой необходимо вернуть список участников. Может принимать значения
    offset -- смещение, необходимое для выборки определенного подмножества участников. 
    fields -- список дополнительных полей, которые необходимо вернуть.
    '''
    current_count = 0
    members = []
    if count == -1:
        response = vk_request('groups.getMembers', 
                   group_id = group_id, 
                   count = 0, 
                   access_token = VK_ACCESS_TOKEN,
                   v = VK_API_VERSION)
        count = response['response']['count']

    while current_count < count:
        response = vk_request('groups.getMembers', 
                           group_id = group_id, 
                           count = min(count - current_count, 1000), 
                           access_token = VK_ACCESS_TOKEN,
                           sort = sort,
                           fields = ','.join(fields),
                           offset = offset + current_count,
                           v = VK_API_VERSION)
        
        # print(current_count)
        members.extend(response['response']['items'])

        current_count += min(count - current_count, 1000)
#         time.sleep(0.2) # (VK api doc) Если приложение установило меньше 10 000 человек, то можно совершать 5 запросов в секунду
        
    return members

def parse_post(post_json):
    post = {}
    post.update({
         'date' :           post_json['date']              if 'date'          in post_json else None, 
         'text' :           post_json['text']              if 'text'          in post_json else None, 
         'is_add' :         post_json['marked_as_ads']     if 'marked_as_ads' in post_json else '0',  
         'comments_count' : post_json['comments']['count'] if 'comments'      in post_json else None,
         'likes_count' :    post_json['comments']['count'] if 'comments'      in post_json else '0',
         'reposts_count' :  post_json['reposts']['count']  if 'reposts'       in post_json else '0',
         'views_count' :    post_json['views']['count']    if 'views'         in post_json else '0',
         'attachments' :    
[parse_attachment(a) for a in post_json['attachments']]    if 'attachments'   in post_json else [],
    })
    
    return post

def parse_user(user_json):
    user = {}
    user.update({
        'first_name' : user_json['first_name'],
        'last_name' : user_json['last_name'],
        'sex' : user_json['sex'] if 'sex' in user_json else None,
#         'bdate' : user_json['bdate'] if 'bdate' in user_json else None ,
        'years_old' : parse_years_old(user_json['bdate']) if 'bdate' in user_json else None,
        'city' : user_json['city']['title'] if 'city' in user_json else None,
        'country' : user_json['country']['title'] if 'country' in user_json else None,
        'last_seen' : user_json['last_seen']['time'] if 'last_seen' in user_json else None,
    })
    
    return user

def parse_attachment(attachment_json):
    '''Возвращает тип вложения. TODO'''
    attachment = {}
    attachment.update({
        'type' : attachment_json['type'],
    })
    
    return attachment

def parse_years_old(date):
    '''Возвращает возраст пользователся в годах или '' '''
    date = date.split('.')
    if len(date) != 3:
        return None
    else:
        return datetime.today().year - int(date[2])

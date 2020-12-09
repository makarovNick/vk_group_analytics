from datetime import datetime


def parse_attachment(attachment_json):
    '''Возвращает тип вложения. TODO'''

    return attachment_json['type']

def parse_age(date):
    '''Возвращает возраст пользователся в годах или '' '''
    if date is None:
        return None
    date = date.split('.')
    if len(date) != 3:
        return None

    return datetime.today().year - int(date[2])

def parse_post(post_json):
    post = {
        'date' :           post_json.get('date'),
        'text' :           post_json.get('text'),
        'is_add' :         post_json.get('marked_as_ads'),
        'comments_count' : post_json.get('comments', {}).get('count'),
        'likes_count' :    post_json.get('likes', {}).get('count'),
        'reposts_count' :  post_json.get('reposts', {}).get('count'),
        'views_count' :    post_json.get('views', {}).get('count'),
        'attachments' :    [parse_attachment(a) for a in post_json.get('attachments', [])],
    }

    return post

def parse_user(user_json):
    user = {
        'id' :              user_json.get('id'),
        'first_name' :      user_json.get('first_name'),
        'last_name' :       user_json.get('last_name'),
        'sex' :             user_json.get('sex'),
        'bdate' :           user_json.get('bdate'),
        'age' :             parse_age(user_json.get('bdate')),
        'city' :            user_json.get('city', {}).get('title'),
        'country' :         user_json.get('country', {}).get('title'),
        'last_seen' :       user_json.get('last_seen', {}).get('time'),
    }

    return user

def parse_stats(statistics):
    if not statistics:
        return [{}]
    stats = [{
        'comments'          : a.get('activity', {}).get('comments', 0),
        'likes'             : a.get('activity', {}).get('likes', 0),
        'subscribed'        : a.get('activity', {}).get('subscribed', 0),
        'unsubscribed'      : a.get('activity', {}).get('unsubscribed', 0),
        'total_views'       : a.get('visitors', {}).get('views', 0),
        'mobile_views'      : a.get('visitors', {}).get('mobile_views'),
        'total_visitors'    : a.get('visitors', {}).get('visitors'),
        'mobile_reach'      : a.get('reach', {}).get('mobile_reach', 0),
        'total_reach'       : a.get('reach', {}).get('reach', 0),
        'reach_subscribers' : a.get('reach', {})['reach_subscribers'],
        'f_visitors'        : a.get('visitors', {}).get('sex', [{'count' : 0} for _ in range(2)])[0]['count'],
        'm_visitors'        : a.get('visitors', {}).get('sex', [{'count' : 0} for _ in range(2)])[1]['count'],
        '18-21_visitors'    : a.get('visitors', {}).get('age', [{'count' : 0} for _ in range(7)])[0]['count'],
        '21-24_visitors'    : a.get('visitors', {}).get('age', [{'count' : 0} for _ in range(7)])[1]['count'],
        '24-27_visitors'    : a.get('visitors', {}).get('age', [{'count' : 0} for _ in range(7)])[2]['count'],
        '27-30_visitors'    : a.get('visitors', {}).get('age', [{'count' : 0} for _ in range(7)])[3]['count'],
        '30-35_visitors'    : a.get('visitors', {}).get('age', [{'count' : 0} for _ in range(7)])[4]['count'],
        '35-45_visitors'    : a.get('visitors', {}).get('age', [{'count' : 0} for _ in range(7)])[5]['count'],
        '45-100_visitors'   : a.get('visitors', {}).get('age', [{'count' : 0} for _ in range(7)])[6]['count'],
        'RU_visitors'       : a.get('visitors', {}).get('countries', [{'count': 0}])[0]['count'],
        'NOTRU_visitors'    : sum(c['count'] for c in a.get('visitors', {}).get('countries', [{'count' : 0} for i in range(2)])[1:]),
        'f_reach'           : a.get('reach', {}).get('sex', [{'count' : 0} for _ in range(2)])[0]['count'],
        'm_reach'           : a.get('reach', {}).get('sex', [{'count' : 0} for _ in range(2)])[1]['count'],
        '18-21_reach'       : a.get('reach', {}).get('age', [{'count' : 0} for _ in range(7)])[0]['count'],
        '21-24_reach'       : a.get('reach', {}).get('age', [{'count' : 0} for _ in range(7)])[1]['count'],
        '24-27_reach'       : a.get('reach', {}).get('age', [{'count' : 0} for _ in range(7)])[2]['count'],
        '27-30_reach'       : a.get('reach', {}).get('age', [{'count' : 0} for _ in range(7)])[3]['count'],
        '30-35_reach'       : a.get('reach', {}).get('age', [{'count' : 0} for _ in range(7)])[4]['count'],
        '35-45_reach'       : a.get('reach', {}).get('age', [{'count' : 0} for _ in range(7)])[5]['count'],
        '45-100_reach'      : a.get('reach', {}).get('age', [{'count' : 0} for _ in range(7)])[6]['count'],
        'RU_reach'          : a.get('reach', {}).get('countries', [{'count' : 0}])[0]['count'],
        'NOTRU_reach'       : sum([c['count'] for c in a.get('reach', {}).get('countries', [{'count' : 0} for i in range(2)])[1:]])
    } for a in statistics]

    return stats

def parse_info(group_json):
    group = {
        'id' :             group_json.get('id'),
        'name' :           group_json.get('name'),
        'members_count' :  group_json.get('members_count'),
        'description' :    group_json.get('description'),
        'photos_count' :   group_json.get('counters', {}).get('photos'),
        'albums_count' :   group_json.get('counters', {}).get('albums'),
        'videos_count' :   group_json.get('counters', {}).get('videos'),
        'articles_count' : group_json.get('counters', {}).get('articles'),
    }

    return group

from datetime import datetime, timedelta


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
    else:
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
    if len(statistics) == 0:
        return [{}]
    stats = [{
        'comments'          : a['activity']['comments'],
        'likes'             : a['activity']['likes'],
        'subscribed'        : a['activity']['subscribed'],
        'unsubscribed'      : a['activity']['unsubscribed'],
        'total_views'       : a['visitors']['views'],
        'mobile_views'      : a['visitors']['mobile_views'],
        'total_visitors'    : a['visitors']['visitors'],
        'mobile_reach'      : a['reach']['mobile_reach'],
        'total_reach'       : a['reach']['reach'],
        'reach_subscribers' : a['reach']['reach_subscribers'],
        'f_visitors'        : a['visitors']['sex'][0]['count'],
        'm_visitors'        : a['visitors']['sex'][1]['count'],
        '18-21_visitors'    : a['visitors']['age'][0]['count'],
        '21-24_visitors'    : a['visitors']['age'][1]['count'],
        '24-27_visitors'    : a['visitors']['age'][2]['count'],
        '27-30_visitors'    : a['visitors']['age'][3]['count'],
        '30-35_visitors'    : a['visitors']['age'][4]['count'],
        '35-45_visitors'    : a['visitors']['age'][5]['count'],
        '45-100_visitors'   : a['visitors']['age'][6]['count'],
        'RU_visitors'       : a['visitors']['countries'][0]['count'],
        'NOTRU_visitors'    : sum(c['count'] for c in a['visitors']['countries'][1:]),
        'f_reach'           : a['reach']['sex'][0]['count'],
        'm_reach'           : a['reach']['sex'][1]['count'],
        '18-21_reach'       : a['reach']['age'][0]['count'],
        '21-24_reach'       : a['reach']['age'][1]['count'],
        '24-27_reach'       : a['reach']['age'][2]['count'],
        '27-30_reach'       : a['reach']['age'][3]['count'],
        '30-35_reach'       : a['reach']['age'][4]['count'],
        '35-45_reach'       : a['reach']['age'][5]['count'],
        '45-100_reach'      : a['reach']['age'][6]['count'],
        'RU_reach'          : a['reach']['countries'][0]['count'],
        'NOTRU_reach'       : sum([c['count'] for c in a['reach']['countries'][1:]])
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

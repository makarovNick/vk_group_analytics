from datetime import datetime, timedelta


def parse_attachment(attachment_json):
    '''Возвращает тип вложения. TODO'''
    # attachment = {}
    # attachment.update({
    #     'type' : attachment_json['type'],
    # })
    
    return attachment_json['type']

def parse_years_old(date):
    '''Возвращает возраст пользователся в годах или '' '''
    date = date.split('.')
    if len(date) != 3:
        return None
    else:
        return datetime.today().year - int(date[2])

def parse_post(post_json):
    post = {}
    post.update({
         'date' :           post_json['date']              if 'date'          in post_json else None, 
         'text' :           post_json['text']              if 'text'          in post_json else None, 
         'is_add' :         post_json['marked_as_ads']     if 'marked_as_ads' in post_json else None,  
         'comments_count' : post_json['comments']['count'] if 'comments'      in post_json else None,
         'likes_count' :    post_json['likes']['count']    if 'likes'         in post_json else None,
         'reposts_count' :  post_json['reposts']['count']  if 'reposts'       in post_json else None,
         'views_count' :    post_json['views']['count']    if 'views'         in post_json else None,
         'attachments' :    
[parse_attachment(a) for a in post_json['attachments']]    if 'attachments'   in post_json else [],
    })
    
    return post

def parse_user(user_json):
    user = {}
    user.update({
        'id' :              user_json['id']                if 'id'         in user_json else None,
        'first_name' :      user_json['first_name']        if 'first_name' in user_json else None,
        'last_name' :       user_json['last_name']         if 'last_name'  in user_json else None,
        'sex' :             user_json['sex']               if 'sex'        in user_json else None,
        'bdate' :           user_json['bdate']             if 'bdate'      in user_json else None,
        'years_old' :  parse_years_old(user_json['bdate']) if 'bdate'      in user_json else None,
        'city' :            user_json['city']['title']     if 'city'       in user_json else None,
        'country' :         user_json['country']['title']  if 'country'    in user_json else None,
        'last_seen' :       user_json['last_seen']['time'] if 'last_seen'  in user_json else None,
    })
    
    return user

def parse_stats(activities):
    stats = {}
    stats.update({
        'comments'          : (sum(a['activity']['comments']                            for a in activities)  / len(activities)) if activities is not None else "No access",
        'likes'             : (sum(a['activity']['likes']                               for a in activities)  / len(activities)) if activities is not None else "No access",
        'subscribed'        : (sum(a['activity']['subscribed']                          for a in activities)  / len(activities)) if activities is not None else "No access",
        'unsubscribed'      : (sum(a['activity']['unsubscribed']                        for a in activities)  / len(activities)) if activities is not None else "No access",
        'total_views'       : (sum(a['visitors']['views']                               for a in activities)  / len(activities)) if activities is not None else "No access",
        'mobile_views'      : (sum(a['visitors']['mobile_views']                        for a in activities)  / len(activities)) if activities is not None else "No access",
        'total_visitors'    : (sum(a['visitors']['visitors']                            for a in activities)  / len(activities)) if activities is not None else "No access",
        'mobile_reach'      : (sum(a['reach']['mobile_reach']                           for a in activities)  / len(activities)) if activities is not None else "No access",
        'total_reach'       : (sum(a['reach']['reach']                                  for a in activities)  / len(activities)) if activities is not None else "No access",
        'reach_subscribers' : (sum(a['reach']['reach_subscribers']                      for a in activities)  / len(activities)) if activities is not None else "No access",
        'f_visitors'        : (sum([a['visitors']['sex'][0]['count']                    for a in activities]) / len(activities)) if activities is not None else "No access",
        'm_visitors'        : (sum([a['visitors']['sex'][1]['count']                    for a in activities]) / len(activities)) if activities is not None else "No access",
        '18-21_visitors'    : (sum([a['visitors']['age'][0]['count']                    for a in activities]) / len(activities)) if activities is not None else "No access",
        '21-24_visitors'    : (sum([a['visitors']['age'][1]['count']                    for a in activities]) / len(activities)) if activities is not None else "No access",
        '24-27_visitors'    : (sum([a['visitors']['age'][2]['count']                    for a in activities]) / len(activities)) if activities is not None else "No access",
        '27-30_visitors'    : (sum([a['visitors']['age'][3]['count']                    for a in activities]) / len(activities)) if activities is not None else "No access",
        '30-35_visitors'    : (sum([a['visitors']['age'][4]['count']                    for a in activities]) / len(activities)) if activities is not None else "No access",
        '35-45_visitors'    : (sum([a['visitors']['age'][5]['count']                    for a in activities]) / len(activities)) if activities is not None else "No access",
        '45-100_visitors'   : (sum([a['visitors']['age'][6]['count']                    for a in activities]) / len(activities)) if activities is not None else "No access",
        'RU_visitors'       : (sum([a['visitors']['countries'][0]['count']              for a in activities]) / len(activities)) if activities is not None else "No access",
        'NOTRU_visitors'    : (sum([sum(c['count'] for c in a['visitors']['countries']) for a in activities]) / len(activities)) if activities is not None else "No access",
        'f_visitors'        : (sum([a['visitors']['sex'][0]['count']                    for a in activities]) / len(activities)) if activities is not None else "No access",
        'm_visitors'        : (sum([a['visitors']['sex'][1]['count']                    for a in activities]) / len(activities)) if activities is not None else "No access",
        '18-21_reach'       : (sum([a['reach']['age'][0]['count']                       for a in activities]) / len(activities)) if activities is not None else "No access",
        '21-24_reach'       : (sum([a['reach']['age'][1]['count']                       for a in activities]) / len(activities)) if activities is not None else "No access",
        '24-27_reach'       : (sum([a['reach']['age'][2]['count']                       for a in activities]) / len(activities)) if activities is not None else "No access",
        '27-30_reach'       : (sum([a['reach']['age'][3]['count']                       for a in activities]) / len(activities)) if activities is not None else "No access",
        '30-35_reach'       : (sum([a['reach']['age'][4]['count']                       for a in activities]) / len(activities)) if activities is not None else "No access",
        '35-45_reach'       : (sum([a['reach']['age'][5]['count']                       for a in activities]) / len(activities)) if activities is not None else "No access",
        '45-100_reach'      : (sum([a['reach']['age'][6]['count']                       for a in activities]) / len(activities)) if activities is not None else "No access",
        'RU_reach'          : (sum([a['reach']['countries'][0]['count']                 for a in activities]) / len(activities)) if activities is not None else "No access",
        'NOTRU_reach'       : (sum([sum([c['count'] for c in a['reach']['countries']])  for a in activities]) / len(activities)) if activities is not None else "No access"})

    return stats

def parse_info(group_json):
    group = {}
    group.update({
        'id' :             group_json['id']                   if 'id'               in group_json else None,
        'name' :           group_json['name']                 if 'name'             in group_json else None,
        'members_count' :  group_json['members_count']        if 'members_count'    in group_json else None,
        'description' :    group_json['description']          if 'description'      in group_json else None,
        'photos_count' :   group_json['counters']['photos']   if 'counters'         in group_json else None,
        'albums_count' :   group_json['counters']['albums']   if 'city'             in group_json else None,
        'videos_count' :   group_json['counters']['videos']   if 'country'          in group_json else None,
        'articles_count' : group_json['counters']['articles'] if 'last_seen'        in group_json else None,
    })

    return group
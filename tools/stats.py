from tools.utils import (date_n_days_ago, 
                         async_get_members, 
                         get_group_info, 
                         get_group_stats,
                         get_group_posts)
from parser.parser import parse_stats, parse_user, parse_post
import numpy as np
import sortednp as snp


async def get_members_stats(groups_id
                    , members_count=False
                    , mean_age=False
                    , inactive_users=False
                    , common_users=False
                    , n_days=7):
    
    stats = [{} for _ in groups_id]

    fields = ['status', 'start_date', 'members_count', 'description', 'counters', 'country', 'activity']
    infos = [get_group_info(id, fields) for id in groups_id]

    fields = ['sex', 'bdate', 'city', 'country', 'online', 'education', 'last_seen']
    members = [list(map(parse_user, await async_get_members(g, count=-1, fields=fields))) for g in groups_id]

    if common_users and len(groups_id) == 2:
        stats[0]['common_users'] = len(snp.kway_intersect(np.array([i['id'] for i in members[0]]), np.array([i['id'] for i in members[1]]), assume_sorted=True))
        stats[1]['common_users'] = stats[0]['common_users']

    for i in range(len(groups_id)):
        if members_count:
            stats[i]['members_count'] = infos[i]['members_count']
        if mean_age:
            stats[i]['mean_age'] = np.mean([m['age'] for m in members[i] if m['age'] is not None])
        if inactive_users:
            date_N_days_ago = date_n_days_ago(n_days).timestamp()
            stats[i]['inactive_users'] = sum(t['last_seen'] < date_N_days_ago for t in members[i] if t['last_seen'] is not None)

    return stats

def get_posts_stats(groups_id
                  , posts_per_day=False
                  , views_per_post=False
                  , likes_per_post=False
                  , n_posts=100
                  , n_days=7):
    stats = [{} for _ in groups_id]
    posts = [list(map(parse_post, get_group_posts(id, count=n_posts))) for id in groups_id]
    date_N_days_ago = date_n_days_ago(n_days).timestamp()

    for i in range(len(groups_id)):
        if posts_per_day:
            temp = 0
            while len(posts[i]) > temp and posts[i][temp]['date'] > date_N_days_ago:
                temp += 1
            stats[i]['posts_per_day'] = (temp) / n_days
        if views_per_post:
            stats[i]['views_per_post'] = np.mean([p['views_count'] for p in posts[i]][1:])
        if likes_per_post:
            stats[i]['likes_per_post'] = np.mean([p['likes_count'] for p in posts[i]][1:])

    return stats

def get_info_stats(groups_id
                  , comments=False
                  , likes=False
                  , subscribed=False
                  , unsubscribed=False
                  , total_views=False
                  , mobile_views=False
                  , total_visitors=False
                  , mobile_reach=False
                  , total_reach=False
                  , reach_subscribers=False
                  , f_visitors=False
                  , m_visitors=False
                  , _18_21_visitors=False
                  , _21_24_visitors=False
                  , _24_27_visitors=False
                  , _27_30_visitors=False
                  , _30_35_visitors=False
                  , _35_45_visitors=False
                  , _45_100_visitors=False
                  , RU_visitors=False
                  , NOTRU_visitors=False
                  , f_reach=False
                  , m_reach=False
                  , _18_21_reach=False
                  , _21_24_reach=False
                  , _24_27_reach=False
                  , _27_30_reach=False
                  , _30_35_reach=False
                  , _35_45_reach=False
                  , _45_100_reach=False
                  , RU_reach=False
                  , NOTRU_reach=False
                  , n_days=7):
    date_N_days_ago = date_n_days_ago(n_days).timestamp()
    stats = [parse_stats(get_group_stats(id, date_N_days_ago)) for id in groups_id]
    stats_ = [{} for _ in stats]
    for i in range(len(stats)):
        if len(stats[i][0].keys()) == 0:
            continue
        if comments:
            stats_[i]['comments'] = np.mean([a['comments'] for a in stats[i][:n_days]])
        if likes:
            stats_[i]['likes'] = np.mean([a['likes'] for a in stats[i][:n_days]])
        if subscribed:
            stats_[i]['subscribed'] = np.mean([a['subscribed'] for a in stats[i][:n_days]])
        if unsubscribed:
            stats_[i]['unsubscribed'] = np.mean([a['unsubscribed'] for a in stats[i][:n_days]])
        if total_views:
            stats_[i]['total_views'] = np.mean([a['total_views'] for a in stats[i][:n_days]])
        if mobile_views:
            stats_[i]['mobile_views'] = np.mean([a['mobile_views'] for a in stats[i][:n_days]])
        if total_visitors:
            stats_[i]['total_visitors'] = np.mean([a['total_visitors'] for a in stats[i][:n_days]])
        if mobile_reach:
            stats_[i]['mobile_reach'] = np.mean([a['mobile_reach'] for a in stats[i][:n_days]])
        if total_reach:
            stats_[i]['total_reach'] = np.mean([a['total_reach'] for a in stats[i][:n_days]])
        if reach_subscribers:
            stats_[i]['reach_subscribers'] = np.mean([a['reach_subscribers'] for a in stats[i][:n_days]])
        if f_visitors:
            stats_[i]['f_visitors'] = np.mean([a['f_visitors'] for a in stats[i][:n_days]])
        if m_visitors:
            stats_[i]['m_visitors'] = np.mean([a['m_visitors'] for a in stats[i][:n_days]])
        if _18_21_visitors:
            stats_[i]['18-21_visitors'] = np.mean([a['18-21_visitors'] for a in stats[i][:n_days]])
        if _21_24_visitors:
            stats_[i]['21-24_visitors'] = np.mean([a['21-24_visitors'] for a in stats[i][:n_days]])
        if _24_27_visitors:
            stats_[i]['24-27_visitors'] = np.mean([a['24-27_visitors'] for a in stats[i][:n_days]])
        if _27_30_visitors:
            stats_[i]['27-30_visitors'] = np.mean([a['27-30_visitors'] for a in stats[i][:n_days]])
        if _30_35_visitors:
            stats_[i]['30-35_visitors'] = np.mean([a['30-35_visitors'] for a in stats[i][:n_days]])
        if _35_45_visitors:
            stats_[i]['35-45_visitors'] = np.mean([a['35-45_visitors'] for a in stats[i][:n_days]])
        if _45_100_visitors:
            stats_[i]['45-100_visitors'] = np.mean([a['45-100_visitors'] for a in stats[i][:n_days]])
        if RU_visitors:
            stats_[i]['RU_visitors'] = np.mean([a['RU_visitors'] for a in stats[i][:n_days]])
        if NOTRU_visitors:
            stats_[i]['NOTRU_visitors'] = np.mean([a['NOTRU_visitors'] for a in stats[i][:n_days]])
        if f_reach:
            stats_[i]['f_reach'] = np.mean([a['f_reach'] for a in stats[i][:n_days]])
        if m_reach:
            stats_[i]['m_reach'] = np.mean([a['m_reach'] for a in stats[i][:n_days]])
        if _18_21_reach:
            stats_[i]['18-21_reach'] = np.mean([a['18-21_reach'] for a in stats[i][:n_days]])
        if _21_24_reach:
            stats_[i]['21-24_reach'] = np.mean([a['21-24_reach'] for a in stats[i][:n_days]])
        if _24_27_reach:
            stats_[i]['24-27_reach'] = np.mean([a['24-27_reach'] for a in stats[i][:n_days]])
        if _27_30_reach:
            stats_[i]['27-30_reach'] = np.mean([a['27-30_reach'] for a in stats[i][:n_days]])
        if _30_35_reach:
            stats_[i]['30-35_reach'] = np.mean([a['30-35_reach'] for a in stats[i][:n_days]])
        if _35_45_reach:
            stats_[i]['35-45_reach'] = np.mean([a['35-45_reach'] for a in stats[i][:n_days]])
        if _45_100_reach:
            stats_[i]['45-100_reach'] = np.mean([a['45-100_reach'] for a in stats[i][:n_days]])
        if RU_reach:
            stats_[i]['RU_reach'] = np.mean([a['RU_reach'] for a in stats[i][:n_days]])
        if NOTRU_reach:
            stats_[i]['NOTRU_reach'] = np.mean([a['NOTRU_reach'] for a in stats[i][:n_days]])
    
    return stats_
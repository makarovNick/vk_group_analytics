from utils import *
from parser import *
from rich.console import Console
from rich.table import Table
from datetime import datetime, timedelta
import argparse
import pandas as pd
from time import sleep

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--groups', action='store', type=str, nargs='+')
    args = parser.parse_args()
    groups = args.groups
    ids = list(map(get_group_id, groups))

    fields = ['sex', 'bdate', 'city', 'country', 'online', 'education', 'last_seen']
    users = [list(map(parse_user, get_group_members_2(g, count=-1, fields=fields))) for g in ids]
    dfs = list(map(pd.DataFrame, users))
    fields = ['status', 'start_date', 'members_count', 'description', 'counters', 'country', 'activity']
    infos = [get_group_info(id, fields) for id in ids]
    
    date_N_days_ago = int((datetime.now() - timedelta(days=10)).timestamp())
    fields = ['visitors', 'reach', 'activity']
    stats = [parse_stats(get_group_stats(id, timestamp_from=date_N_days_ago, stats_groups=fields)) for id in ids]
    posts = [list(map(parse_post, get_group_posts(id))) for id in ids]

    ppd = [str(posts_per_day(id)) for id in ids]
    members_counts = [i['members_count'] for i in infos]
    views = [[] for _ in ids]
    likes = [[] for _ in ids]
    for i, group in enumerate(posts):
        for post in group:
            views[i].append(post['views_count'])
            likes[i].append(post['likes_count'])
    
    inactive_user= [inactive_users(df) for df in dfs]
    mean_views = [sum(j) / len(j) if len(j) != 0 else '0' for j in views]
    mean_likes = [sum(j) / len(j) if len(j) != 0 else '0' for j in likes]
    mean_age = [df.years_old.mean() for df in dfs]
    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    
    table.add_column('feature/screen_name')
    for r in groups:
        table.add_column(r)
    result_header = ['members_count'
                   , 'views per post'   
                   , 'likes per post'
                   , 'mean age'
                   , 'posts per day'
                   , 'inactive users'
                   , 'comments daily'
                   , 'subscribers daily'
                   , 'unsubscribers daily'
                   , 'total_reach' 
                   , 'f_visitors'
                   , 'm_visitors']
    results = list(map(lambda x: [str(round(i, 2)) if (type(i) is not str) else i for i in x], [members_counts
             , mean_views
             , mean_likes
             , mean_age
             , ppd
             , inactive_user
             , [s['comments'] for s in stats]
             , [s['subscribed'] for s in stats]
             , [s['unsubscribed'] for s in stats]
             , [s['total_reach'] for s in stats]
             , [s['f_visitors'] for s in stats]
             , [s['m_visitors'] for s in stats]]))
    for i, z in enumerate(result_header):
        table.add_row(
            z, *results[i]
        )
    console.print(table)

if __name__ == '__main__':
    main()

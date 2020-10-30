from utils import *
from rich.console import Console
from rich.table import Table
from datetime import datetime, timedelta
import argparse
import pandas as pd
from time import sleep

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

def posts_per_day(group_id, days=7):
    today = int(datetime.timestamp(datetime.today()))
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
    while posts[-1]['date'] < limit:
        posts.pop()
    
    return len(posts) / days

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', action='store', type=str, nargs='+')
    args = parser.parse_args()
    groups = args.input
    fields = ['sex', 'bdate', 'city', 'country', 'online', 'education', 'last_seen']
    ids = list(map(get_group_id, groups))
    users = [list(map(parse_user, get_group_members_2(g, count=-1, fields=fields))) for g in ids]
    dfs = list(map(pd.DataFrame, users))
    fields = ['status', 'start_date', 'members_count', 'description', 'counters', 'country', 'activity']
    infos = [get_group_info(id, fields) for id in ids]

    posts = [list(map(parse_post, get_group_posts(id))) for id in ids]

    ppd = [posts_per_day(id) for id in ids]
    members_counts = [i['members_count'] for i in infos]
    views = [[] for _ in ids]
    likes = [[] for _ in ids]
    for i, group in enumerate(posts):
        for post in group:
            views[i].append(post['views_count'])
            likes[i].append(post['likes_count'])
    
    mean_views = [sum(j) / len(j) for j in views]
    mean_likes = [sum(j) / len(j) for j in likes]

    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    
    result_header = ['screen_name', 'members_count', 'mean views', 'mean likes', 'mean age', 'posts_per_day']
    for r in result_header:
        table.add_column(r)

    for i, g in enumerate(groups):
        table.add_row(
            g, str(members_counts[i]), str(mean_views[i]), str(mean_likes[i]), str(dfs[i].years_old.mean()), str(ppd[i])
        )
    console.print(table)

if __name__ == '__main__':
    main()

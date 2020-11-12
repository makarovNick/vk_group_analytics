import termplotlib as tpl
import numpy as np
from utils import *
from parser import *
from rich.console import Console
from rich.table import Table
from datetime import datetime, timedelta
import argparse
import pandas as pd
from time import sleep

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--groups', action='store', type=str, nargs='+')
    args = parser.parse_args()
    groups = args.groups
    ids = list(map(get_group_id, groups))

    fields = ['sex', 'bdate', 'city', 'country', 'online', 'education', 'last_seen']
    users = [list(map(parse_user, await async_get_members(g, count=-1, fields=fields))) for g in ids]
    dfs = list(map(pd.DataFrame, users))
    fields = ['status', 'start_date', 'members_count', 'description', 'counters', 'country', 'activity']
    infos = [get_group_info(id, fields) for id in ids]
    
    date_N_days_ago = int((datetime.now() - timedelta(days=7)).timestamp())
    # fields = ['visitors', 'reach', 'activity']
    stats = [parse_stats(get_group_stats(id, timestamp_from=date_N_days_ago)) for id in ids]
    posts = [list(map(parse_post, get_group_posts(id))) for id in ids]

    ppd = [posts_per_day(id) for id in ids]
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
    results = list(map(lambda x: [str(round(i, 2)) if (type(i) is not str and i is not None) else 'No access' for i in x], [members_counts
             , mean_views
             , mean_likes
             , mean_age
             , ppd
             , inactive_user
             , [s[0].get('comments') for s in stats]
             , [s[0].get('subscribed') for s in stats]
             , [s[0].get('unsubscribed') for s in stats]
             , [s[0].get('total_reach') for s in stats]
             , [s[0].get('f_visitors') for s in stats]
             , [s[0].get('m_visitors') for s in stats]]))
    for name, result in zip(result_header, results):
        table.add_row(
            name, *result
        )
    if len(groups) == 2:
        table.add_row("common_users", str(pd.merge(dfs[0], dfs[1], how='inner', on='id', suffixes=['', '_']).loc[:, dfs[0].columns].shape[0]))
    console.print(table)
    for i, stat in enumerate(stats):
        if len(stat[0].keys()) != 0:
            console.print(f"Russian visitors for {groups[i]}", style="bold red")
            fig = tpl.figure()
            fig.plot(y = [a['RU_visitors'] for a in stat], x = list(range(7)), width=20, height=20)
            fig.show()

if __name__ == '__main__':
    # asyncio.run(main()) 
    loop = asyncio.get_event_loop()
    # loop.set_exception_handler(ignore_ssl_error)
    task = loop.create_task(main())
    loop.run_until_complete(task)
    loop.close()

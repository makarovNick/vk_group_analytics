from tools.utils import *
from tools.stats import *
from parser.parser import *
from ui import cli, webui

import pandas as pd
import numpy as np
import argparse
import warnings

warnings.filterwarnings("ignore")

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--groups', action='store', type=str, nargs='+')
    parser.add_argument('-w', '--web', help='Generate interactive web ui', action='store_true')
    args = parser.parse_args()
    groups = args.groups
    web = args.web

    ids = list(map(get_group_id, groups))

    members_stats = await get_members_stats(ids,
                                      members_count=True, 
                                      mean_age=True, 
                                      inactive_users=True,
                                      common_users=True)
    
    post_stats = get_posts_stats(ids, 
                                 posts_per_day=True, 
                                 views_per_post=True, 
                                 likes_per_post=True,
                                 n_posts=100,
                                 n_days=2)

    info_stats = get_info_stats(ids
                  , comments=False
                  , likes=True
                  , subscribed=True
                  , unsubscribed=True
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
                  , RU_visitors=True
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
                  , NOTRU_reach=False)

    if not web:
        cli.draw_table(groups, post_stats, members_stats, info_stats)
        date_N_days_ago = date_n_days_ago(3).timestamp()
        stats = [parse_stats(get_group_stats(id, date_N_days_ago)) for id in ids]
        cli.draw_plot(list(range(3)), [a['likes'] for a in stats[0]], x_label="days_ago", label="likes daily", y_label='likes')
    else:
        webui.make_dash(groups, post_stats=post_stats, member_stats=members_stats, info_stats=info_stats)



if __name__ == '__main__':
    asyncio.run(main())

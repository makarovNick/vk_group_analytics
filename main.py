#!/usr/bin/python
# -*- coding: utf-8 -*-
import asyncio
import argparse
import warnings

from tools.utils import get_group_id
from tools.stats import (get_info_stats,
                        get_members_stats,
                        get_posts_stats)
from config import Config
from ui import cli, webui

warnings.filterwarnings('ignore')


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('groups', action='store', type=str, nargs='+')
    parser.add_argument('-w', '--web', help='Generate interactive web ui', action='store_true')
    parser.add_argument('-t', '--token', help='Access token', action='store', type=str)
    parser.add_argument('-d', '--n_days', type=int, default=7, action='store', help='Days for statistics')
    parser.add_argument('-mc', '--members_count', help='Show members count in table', action='store_true')
    parser.add_argument('-ma', '--mean_age', help='Show member\'s mean age in table', action='store_true')
    parser.add_argument('-iu', '--inactive_users', help='Show inactive_users in table', action='store_true')
    parser.add_argument('-cu', '--common_users', help='Show common_users of two groups in table', action='store_true')
    parser.add_argument('-ppd', '--posts_per_day', help='Show posts_per_day in table', action='store_true')
    parser.add_argument('-vpp', '--views_per_post', help='Show views_per_post in table', action='store_true')
    parser.add_argument('-lpp', '--likes_per_post', help='Show likes_per_post in table', action='store_true')
    parser.add_argument('-l', '--likes', help='Show daily count in table', action='store_true')
    parser.add_argument('-s', '--subscribed', help='Show subcribers daily in table', action='store_true')
    parser.add_argument('-c', '--comments', help='Show comments daily in table', action='store_true')
    parser.add_argument('-u', '--unsubscribed', help='Show unsubscribed count daily in table', action='store_true')

    parser.add_argument('-tv', '--total_views', help='Show total_views count daily in table', action='store_true')
    parser.add_argument('-mv', '--mobile_views', help='Show mobile_views count daily in table', action='store_true')
    parser.add_argument('-tvis', '--total_visitors', help='Show total_visitors count daily in table', action='store_true')
    parser.add_argument('-mobr', '--mobile_reach', help='Show mobile_reach count daily in table', action='store_true')
    parser.add_argument('-tr', '--total_reach', help='Show total_reach count daily in table', action='store_true')
    parser.add_argument('-r', '--reach_subscribers', help='Show reach_subscribers count daily in table', action='store_true')
    parser.add_argument('-fvis', '--f_visitors', help='Show f_visitors count daily in table', action='store_true')
    parser.add_argument('-mvis', '--m_visitors', help='Show m_visitors count daily in table', action='store_true')
    parser.add_argument('-1v', '--_18_21_visitors', help='Show 18_21_visitors count daily in table', action='store_true')
    parser.add_argument('-2v', '--_21_24_visitors', help='Show 21_24_visitors count daily in table', action='store_true')
    parser.add_argument('-3v', '--_24_27_visitors', help='Show 24_27_visitors count daily in table', action='store_true')
    parser.add_argument('-4v', '--_27_30_visitors', help='Show 27_30_visitors count daily in table', action='store_true')
    parser.add_argument('-5v', '--_30_35_visitors', help='Show 30_35_visitors count daily in table', action='store_true')
    parser.add_argument('-6v', '--_35_45_visitors', help='Show 35_45_visitors count daily in table', action='store_true')
    parser.add_argument('-7v', '--_45_100_visitors', help='Show 45_100_visitors count daily in table', action='store_true')
    parser.add_argument('-RUv', '--RU_visitors', help='Show RU_visitors count daily in table', action='store_true')
    parser.add_argument('-NRv', '--NOTRU_visitors', help='Show NOTRU_visitors count daily in table', action='store_true')
    parser.add_argument('-fr', '--f_reach', help='Show f_reach count daily in table', action='store_true')
    parser.add_argument('-mr', '--m_reach', help='Show m_reach count daily in table', action='store_true')
    parser.add_argument('-1r', '--_18_21_reach', help='Show 18_21_reach count daily in table', action='store_true')
    parser.add_argument('-2r', '--_21_24_reach', help='Show 21_24_reach count daily in table', action='store_true')
    parser.add_argument('-3r', '--_24_27_reach', help='Show 24_27_reach count daily in table', action='store_true')
    parser.add_argument('-4r', '--_27_30_reach', help='Show 27_30_reach count daily in table', action='store_true')
    parser.add_argument('-5r', '--_30_35_reach', help='Show 30_35_reach count daily in table', action='store_true')
    parser.add_argument('-6r', '--_35_45_reach', help='Show 35_45_reach count daily in table', action='store_true')
    parser.add_argument('-7r', '--_45_100_reach', help='Show 45_100_reach count daily in table', action='store_true')
    parser.add_argument('-RUr', '--RU_reach', help='Show RU_reach count daily in table', action='store_true')
    parser.add_argument('-NRr', '--NOTRU_reach', help='Show NOTRU_reach count daily in table', action='store_true')
    parser.add_argument('--all', help='Show all statistics table', action='store_true')
    args = parser.parse_args()

    if args.all:
        for arg in vars(args):
            if isinstance(getattr(args, arg), bool) and arg != 'web':
                setattr(args, arg, True)

    days = args.n_days
    groups = args.groups
    web = args.web
    if args.token is not None:
        Config.VK_ACCESS_TOKEN = args.token

    ids = list(map(get_group_id, groups))

    members_stats = await get_members_stats(ids,
                                            members_count=args.members_count,
                                            mean_age=args.mean_age,
                                            inactive_users=args.inactive_users,
                                            common_users=args.common_users)

    post_stats = get_posts_stats(ids,
                                 posts_per_day=args.posts_per_day,
                                 views_per_post=args.views_per_post,
                                 likes_per_post=args.likes_per_post,
                                 n_posts=100,
                                 n_days=2)

    info_stats = get_info_stats(
        ids,
        comments=args.comments,
        likes=args.likes,
        subscribed=args.subscribed,
        unsubscribed=args.unsubscribed,
        total_views=args.total_views,
        mobile_views=args.mobile_views,
        total_visitors=args.total_visitors,
        mobile_reach=args.mobile_reach,
        total_reach=args.total_reach,
        reach_subscribers=args.reach_subscribers,
        f_visitors=args.f_visitors,
        m_visitors=args.m_visitors,
        _18_21_visitors=args._18_21_visitors,
        _21_24_visitors=args._21_24_visitors,
        _24_27_visitors=args._24_27_visitors,
        _27_30_visitors=args._27_30_visitors,
        _30_35_visitors=args._30_35_visitors,
        _35_45_visitors=args._35_45_visitors,
        _45_100_visitors=args._45_100_visitors,
        RU_visitors=args.RU_visitors,
        NOTRU_visitors=args.NOTRU_visitors,
        f_reach=args.f_reach,
        m_reach=args.m_reach,
        _18_21_reach=args._18_21_reach,
        _21_24_reach=args._21_24_reach,
        _24_27_reach=args._24_27_reach,
        _27_30_reach=args._27_30_reach,
        _30_35_reach=args._30_35_reach,
        _35_45_reach=args._35_45_reach,
        _45_100_reach=args._45_100_reach,
        RU_reach=args.RU_reach,
        NOTRU_reach=args.NOTRU_reach,
        n_days=days)

    if not web:
        cli.draw_table(groups, post_stats, members_stats, info_stats)
    else:
        webui.make_dash(groups,
                        post_stats=post_stats,
                        member_stats=members_stats,
                        info_stats=info_stats)


if __name__ == '__main__':
    asyncio.run(main())

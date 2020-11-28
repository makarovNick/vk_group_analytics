#!/usr/bin/env python3

import os
import json
import time

from tools.utils import get_group_info
from tools.utils import get_group_posts


def dump_group_info(ids, output_path):
    fields = [
        "id",
        "name",
        "screen_name",
        "is_closed",
        "deactivated",
        "type",
        "has_photo",
        "photo_50",
        "photo_100",
        "photo_200",
        "activity",
        "age_limits",
        "city",
        "contacts",
        "counters",
        "country",
        "cover",
        "description",
        "fixed_post",
        "links",
        "members_count",
        "place",
        "site",
        "status",
        "trending",
        "verified",
        "wiki_page"
    ]

    data = []

    for group_id in ids:
        group_info = get_group_info(group_id, fields)
        data.append(group_info)

        time.sleep(1)

    output_filename = os.path.join(output_path, 'group_info.json')

    with open(output_filename, 'w') as fout:
        json.dump(data, fout, ensure_ascii=False, indent=4)


def dump_group_posts(ids, output_path):
    posts_path = os.path.join(output_path, 'posts')
 
    if not os.path.exists(posts_path):
        os.makedirs(posts_path)

    for group_id in ids:
        output_filename = os.path.join(posts_path, 'posts_%s.json' % group_id)
        data = get_group_posts(group_id, 5000)

        with open(output_filename, 'w') as fout:
            json.dump(data, fout, ensure_ascii=False, indent=4)

        time.sleep(1)


def dump_raw_data(ids, output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    dump_group_info(ids, output_path)
    dump_group_posts(ids, output_path)

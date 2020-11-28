#!/usr/bin/env python3

import argparse
import os
from datetime import datetime
import ast
from collections import Counter
import json

import pandas as pd

from charts_utils.population_pyramid import build_chart_population_pyramid
from charts_utils.geo_sunburst import build_chart_geo_sunburst
from charts_utils.media_radar import build_chart_media_radar
from charts_utils.edu_wordcloud import build_chart_edu_wordcloud
from charts_utils.calendar_heatmap import build_chart_calendar_heatmap


def main_rating(groups, status, likes_ranks, posts_ranks, activity_ranks):
    js_tables_elements = []
    html_elements = []

    html_element = """
    <div class="d-block" style="margin: 10px; text-align: center; padding: 20px;">
    <h4> 🏆 Groups Rating</h4>
    <div id="table_main_rating"></div>
    </div>
    <p></p>
    """

    html_elements.append(html_element)

    table_rows = []

    members_top = sorted([
        group['members_count'] for group in groups], reverse=True)[:3]

    for group in groups:
        if len(members_top) > 0 and group['members_count'] == members_top[0]:
            status[group['id']].append("🥇")
        elif len(members_top) > 1 and group['members_count'] == members_top[1]:
            status[group['id']].append("🥈")
        elif len(members_top) > 2 and group['members_count'] == members_top[2]:
            status[group['id']].append("🥉")

        table_rows.append(str([
            "club%s" % group['id'],
            group['members_count'],
            likes_ranks[group['id']],
            posts_ranks[group['id']],
            activity_ranks[group['id']],
            "".join(status[group['id']]) if group['id'] in status else "",
            group['name']]))

    js_element = """
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'club');
        data.addColumn('number', 'members');
        data.addColumn('number', 'likes per view');
        data.addColumn('number', 'posts per day');
        data.addColumn('number', 'active users rank');
        data.addColumn('string', 'status');
        data.addColumn('string', 'name');

        data.addRows([
            {ROWS}
        ]);

        var table = new google.visualization.Table(document.getElementById('table_main_rating'));

        table.draw(data, {{showRowNumber: true, width: '100%', height: '100%'}});
    """.format(ROWS=",\n".join(table_rows))

    js_tables_elements.append(js_element)

    print("Created: main rating")

    return {
        "js_tables": "\n".join(js_tables_elements),
        "html": "\n".join(html_elements)
    }


def charts_likes(groups, data_source_posts):
    ranks_info = {}
    status = {}

    js_tables_elements = []
    js_charts_elements = []

    html_elements = []

    html_element = """
    <div class="d-block" style="margin: 10px; text-align: center; padding: 20px;">
    <h4>👍 Likes</h4>
    <div id="table_likes"></div>
    </div>
    <p></p>
    """

    html_elements.append(html_element)

    table_rows = []
    stat = {}

    for group in groups:
        filename = os.path.join(
            data_source_posts, "posts_%s.json" % group['id'])

        with open(filename, 'r') as fin:
            data = json.load(fin)

        stat[group['id']] = {
            'views_1': 0,
            'views_2': 0,
            'views_3': 0,
            'likes_1': 0,
            'likes_2': 0,
            'likes_3': 0,
            'reposts_1': 0,
            'reposts_2': 0,
            'reposts_3': 0,
            'comments_1': 0,
            'comments_2': 0,
            'comments_3': 0
        }

        ind = 0

        for post in data:
            if 'is_pinned' not in post and 'views' in post:
                if ind < 100:
                    stat[group['id']]['views_1'] += post['views']['count']
                    stat[group['id']]['likes_1'] += post['likes']['count']
                    stat[group['id']]['reposts_1'] += post['reposts']['count']
                    stat[group['id']]['comments_1'] += post['comments']['count']
                elif 100 <= ind < 200:
                    stat[group['id']]['views_2'] += post['views']['count']
                    stat[group['id']]['likes_2'] += post['likes']['count']
                    stat[group['id']]['reposts_2'] += post['reposts']['count']
                    stat[group['id']]['comments_2'] += post['comments']['count']
                elif 200 <= ind < 300:
                    stat[group['id']]['views_3'] += post['views']['count']
                    stat[group['id']]['likes_3'] += post['likes']['count']
                    stat[group['id']]['reposts_3'] += post['reposts']['count']
                    stat[group['id']]['comments_3'] += post['comments']['count']

                ind += 1

    color = {
        'views': '#007bff',
        'likes': '#28a745',
        'reposts': '#fd7e14',
        'comments': '#ffc107'
    }

    max_views = max([stat[group_id]['views_1'] for group_id in stat])
    max_likes = max([stat[group_id]['likes_1'] for group_id in stat])
    max_reposts = max([stat[group_id]['reposts_1'] for group_id in stat])
    max_comments = max([stat[group_id]['comments_1'] for group_id in stat])

    max_likes_per_view = max([
        stat[group_id]['likes_1'] / max(stat[group_id]['views_1'], 1)
        for group_id in stat])

    for group in groups:
        for activity in ['views', 'likes', 'reposts', 'comments']:
            items = [
                str([
                    'old period',
                    stat[group['id']][activity + '_3'],
                    color[activity]
                ]),
                str([
                    'previous period',
                    stat[group['id']][activity + '_2'],
                    color[activity]
                ]),
                str([
                    'recent period',
                    stat[group['id']][activity + '_1'],
                    color[activity]
                ])
            ]

            js_element = """
            var data = google.visualization.arrayToDataTable([
                ['period',  '{ACTIVITY}', {{ role: 'style' }}],
                {ITEMS}
            ]);

            var options = {{
                title: '{TITLE_ACTIVITY} in Time',
                legend: {{ position: "none" }},
                bar: {{groupWidth: "66%"}},
                vAxis: {{
                    viewWindowMode: 'explicit',
                    viewWindow: {{
                        min: 0,
                    }}
                }}
            }};

            var chart = new google.visualization.ColumnChart(document.getElementById('{ACTIVITY}_chart_club{ID}'));
            chart.draw(data, options);
            """.format(
                ITEMS=",\n".join(items),
                ID=group['id'],
                ACTIVITY=activity,
                TITLE_ACTIVITY=activity.capitalize()
            )

            js_charts_elements.append(js_element)

        img_src = group['photo_50']
        img = """
            <img src="%s" class="mr-3" style="max-width: 30px;" />
        """ % img_src if img_src else ""

        html_element = """
        <div class="club{ID} d-inline-block">
        <div class="d-block" style="margin: 10px;">
        <div class="media" style="max-width: 400px;">
        {IMG}
        <div class="media-body">
        <h5 style="max-width: 350px;">{NAME}</h5>
        <h6 style="max-width: 350px;"><a href="https://vk.com/club{ID}">club{ID}</a> {GROUP}</h6>
        </div>
        </div>
        <div style="width: 400px; height; 400px;">
        <div class="row">
        <div id="views_chart_club{ID}" style="width: auto; height: auto;"></div>
        </div>
        <div class="row">
        <div id="likes_chart_club{ID}" style="width: auto; height: auto;"></div>
        </div>
        <div class="row">
        <div id="reposts_chart_club{ID}" style="width: auto; height: auto;"></div>
        </div>
        <div class="row">
        <div id="comments_chart_club{ID}" style="width: auto; height: auto;"></div>
        </div>
        </div>
        </div>
        </div>
        """.format(
            ID=group['id'],
            GROUP="👥",
            NAME=group['name'],
            IMG=img
        )

        html_elements.append(html_element)

        likes_per_view_1 = stat[group['id']]['likes_1'] / max(
            stat[group['id']]['views_1'], 1)

        likes_per_view_2 = stat[group['id']]['likes_2'] / max(
            stat[group['id']]['views_2'], 1)

        ranks_info[group['id']] = likes_per_view_1

        group_status = ""

        if stat[group['id']]['views_1'] == max_views:
            group_status += "👁"
        if stat[group['id']]['likes_1'] == max_likes:
            group_status += "👍"
        if stat[group['id']]['reposts_1'] == max_reposts:
            group_status += "📢"
        if stat[group['id']]['comments_1'] == max_comments:
            group_status += "💬"
        if (stat[group['id']]['likes_1'] /
                max(stat[group['id']]['views_1'], 1) == max_likes_per_view):
            group_status += "❤️"

        if (stat[group['id']]['likes_1'] > stat[group['id']]['likes_2'] and
                likes_per_view_1 > likes_per_view_2):
            group_status += "➕"

        if (stat[group['id']]['likes_1'] < stat[group['id']]['likes_2'] and
                likes_per_view_1 < likes_per_view_2):
            group_status += "➖"

        status[group['id']] = group_status

        table_rows.append(
            str([
                "club%s" % group['id'],
                stat[group['id']]['views_1'],
                stat[group['id']]['likes_1'],
                stat[group['id']]['reposts_1'],
                stat[group['id']]['comments_1'],
                likes_per_view_1,
                (stat[group['id']]['likes_1'] -
                    stat[group['id']]['likes_2']),
                likes_per_view_1 - likes_per_view_2,
                group_status,
                group['name']
            ])
        )

    js_element = """
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'club');
        data.addColumn('number', 'views [100]');
        data.addColumn('number', 'likes [100]');
        data.addColumn('number', 'reposts [100]');
        data.addColumn('number', 'comments [100]');
        data.addColumn('number', 'likes per view [100]');
        data.addColumn('number', 'likes diff');
        data.addColumn('number', 'likes per view diff');
        data.addColumn('string', 'status');
        data.addColumn('string', 'name');

        data.addRows([
            {ROWS}
        ]);

        var table = new google.visualization.Table(document.getElementById('table_likes'));

        table.draw(data, {{showRowNumber: true, width: '100%', height: '100%'}});
    """.format(ROWS=",\n".join(table_rows))

    js_tables_elements.append(js_element)

    print("Created: likes bars")

    return {
        "js_tables": "\n".join(js_tables_elements),
        "js_charts": "\n".join(js_charts_elements),
        "html": "\n".join(html_elements),
        "status": status,
        "ranks": ranks_info
    }


def charts_posts_activity(groups, data_source_posts, section_path):
    if not os.path.exists(section_path):
        os.makedirs(section_path)

    status = {}
    ranks_info = {}

    js_tables_elements = []

    html_elements = []

    html_element = """
    <div class="d-block" style="margin: 10px; text-align: center; padding: 20px;">
    <h4> ⭐ Posts Activity </h4>
    <div id="table_posts_activity"></div>
    </div>
    <p></p>
    """

    html_elements.append(html_element)

    table_rows = []
    table_rows_prepared = []

    max_date = 0

    for group in groups:
        filename = os.path.join(
            data_source_posts, "posts_%s.json" % group['id'])

        with open(filename, 'r') as fin:
            data = json.load(fin)

        for post in data:
            if 'is_pinned' not in post:
                max_date = max(max_date, post['date'])
                break

    last_month_min_date = max_date - 30 * 24 * 60 * 60
    prev_month_min_date = max_date - 2 * 30 * 24 * 60 * 60

    min_dt = (
        datetime.fromtimestamp(prev_month_min_date - 30 * 24 * 60 * 60)
        .replace(hour=0, minute=0, second=0)
    )

    max_dt = datetime.fromtimestamp(max_date)

    for group in groups:
        filename = os.path.join(
            data_source_posts, "posts_%s.json" % group['id'])

        with open(filename, 'r') as fin:
            data = json.load(fin)

        last_month_posts = 0
        prev_month_posts = 0

        calendar_posts = {}

        for post in data:
            if last_month_min_date <= post['date'] <= max_date:
                last_month_posts += 1
            elif prev_month_min_date <= post['date'] < last_month_min_date:
                prev_month_posts += 1

            tmp_dt = (
                datetime.fromtimestamp(post['date'])
                .replace(hour=0, minute=0, second=0)
            )

            dt = datetime.strftime(tmp_dt, '%Y-%m-%d')

            if tmp_dt > min_dt:
                if dt not in calendar_posts:
                    calendar_posts[dt] = 1
                else:
                    calendar_posts[dt] += 1

        tmp_dt = datetime.strftime(min_dt, '%Y-%m-%d')

        if tmp_dt not in calendar_posts:
            calendar_posts[tmp_dt] = 0

        tmp_dt = datetime.strftime(max_dt, '%Y-%m-%d')

        if tmp_dt not in calendar_posts:
            calendar_posts[tmp_dt] = 0

        df = pd.DataFrame({
            'dt': list(calendar_posts.keys()),
            'value': list(calendar_posts.values())
        })

        output_path = os.path.join(
            section_path, 'calendar_heatmap_%s.svg' % group['id']
        )

        build_chart_calendar_heatmap(df, output_path)

        group_status = ""

        if last_month_posts > prev_month_posts:
            group_status += "↗️"

        if last_month_posts < prev_month_posts:
            group_status += "↘️"

        table_rows_prepared.append([
            "club%s" % group['id'],
            last_month_posts / 30,
            prev_month_posts / 30,
            (last_month_posts - prev_month_posts) / 30,
            group_status,
            group['name']
        ])

        ranks_info[group['id']] = last_month_posts / 30

        status[group['id']] = group_status

        rel_path = "calendar_heatmap/calendar_heatmap_%s.svg" % group['id']

        img_src = group['photo_50']
        img = """
            <img src="%s" class="mr-3" style="max-width: 30px;" />
        """ % img_src if img_src else ""

        html_element = """
        <div class="club{ID} d-inline-block">
        <div class="d-block" style="margin: 10px;">
        <div class="media" style="max-width: 400px;">
        {IMG}
        <div class="media-body">
        <h5 style="max-width: 350px;">{NAME}</h5>
        <h6 style="max-width: 350px;"><a href="https://vk.com/club{ID}">club{ID}</a> {GROUP}</h6>
        </div>
        </div>
        <iframe src="{SRC}" scorlling="no" style="width: 400px; height: 250px;" frameBorder="0">
        </iframe>
        </div>
        </div>
        """.format(
            ID=group['id'],
            GROUP="🗓️",
            NAME=group['name'],
            IMG=img,
            SRC=rel_path
        )

        html_elements.append(html_element)

    for item in table_rows_prepared:
        table_rows.append(str(item))

    js_element = """
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'club');
        data.addColumn('number', 'recent month posts per day');
        data.addColumn('number', 'previous month posts per day');
        data.addColumn('number', 'diff posts per day');
        data.addColumn('string', 'status');
        data.addColumn('string', 'name');

        data.addRows([
            {ROWS}
        ]);

        var table = new google.visualization.Table(document.getElementById('table_posts_activity'));

        table.draw(data, {{showRowNumber: true, width: '100%', height: '100%'}});
    """.format(ROWS=",\n".join(table_rows))

    js_tables_elements.append(js_element)

    print("Created: posts activity charts")

    return {
        "js_tables": "\n".join(js_tables_elements),
        "html": "\n".join(html_elements),
        "status": status,
        "ranks": ranks_info
    }


def charts_media(groups, data_source_posts, section_path):
    if not os.path.exists(section_path):
        os.makedirs(section_path)

    status = {}

    js_tables_elements = []
    html_elements = []

    html_element = """
    <div class="d-block" style="margin: 10px; text-align: center; padding: 20px;">
    <h4> 🎨 Media </h4>
    <div id="table_media"></div>
    </div>
    <p></p>
    """

    html_elements.append(html_element)

    for group in groups:
        filename = os.path.join(
            data_source_posts, "posts_%s.json" % group['id'])

        with open(filename, 'r') as fin:
            data = json.load(fin)

        stat = {}

        for post in data:
            if 'attachments' in post:
                for attachment in post['attachments']:
                    if 'type' in attachment:
                        attachment_type = attachment['type']

                        if attachment_type in stat:
                            stat[attachment_type] += 1
                        else:
                            stat[attachment_type] = 1

        output_path = os.path.join(
            section_path, 'media_radar_%s.html' % group['id'])

        build_chart_media_radar(stat, output_path)

        rel_path = "media_radar/media_radar_%s.html" % group['id']

        img_src = group['photo_50']
        img = """
            <img src="%s" class="mr-3" style="max-width: 30px;" />
        """ % img_src if img_src else ""

        html_element = """
        <div class="club{ID} d-inline-block">
        <div class="d-block" style="margin: 10px;">
        <div class="media" style="max-width: 400px;">
        {IMG}
        <div class="media-body">
        <h5 style="max-width: 350px;">{NAME}</h5>
        <h6 style="max-width: 350px;"><a href="https://vk.com/club{ID}">club{ID}</a> {GROUP}</h6>
        </div>
        </div>
        <iframe src="{SRC}" scorlling="no" style="width: 400px; height: 400px;" frameBorder="0">
        </iframe>
        </div>
        </div>
        """.format(
            ID=group['id'],
            SRC=rel_path,
            GROUP="📎",
            NAME=group['name'],
            IMG=img
        )

        html_elements.append(html_element)

    media_resources = {
        "pictures": [],
        "video": [],
        "audio": [],
        "text": [],
        "topics": [],
        "links": []
    }

    for group in groups:
        media_resources["pictures"].append(
            group['counters'].get('photos', 0))

        media_resources["video"].append(
            group['counters'].get('videos', 0))

        media_resources["audio"].append(
            group['counters'].get('audios', 0) +
            group['counters'].get('podcasts', 0))

        media_resources["text"].append(
            group['counters'].get('articles', 0) +
            group['counters'].get('topics', 0) +
            group['counters'].get('docs', 0))

        media_resources["topics"].append(
            group['counters'].get('topics', 0))

        media_resources["links"].append(
            len(group.get('links', [])))

    table_rows = []

    for group in groups:
        group_status = ""

        if max(media_resources["pictures"]) > 0:
            if (group['counters'].get('photos', 0) >=
                    min(max(media_resources["pictures"]), 1000)):
                group_status += "🖼"

        if max(media_resources["video"]) > 0:
            if (group['counters'].get('videos', 0) >=
                    min(max(media_resources["video"]), 500)):
                group_status += "🎬"

        if max(media_resources["audio"]) > 0:
            if (group['counters'].get('audios', 0) +
                    group['counters'].get('podcasts', 0) >=
                    min(max(media_resources["audio"]), 100)):
                group_status += "🎧"

        if max(media_resources["text"]) > 0:
            if (group['counters'].get('articles', 0) +
                    group['counters'].get('docs', 0) >=
                    max(media_resources["text"])):
                group_status += "📝"

        if max(media_resources["topics"]) > 0:
            if (group['counters'].get('topics', 0) >=
                    min(max(media_resources["topics"]), 10)):
                group_status += "✍️"

        if max(media_resources["links"]) > 0:
            if (len(group.get('links', [])) >=
                    min(max(media_resources["links"]), 10)):
                group_status += "🔗"

        if group['counters'].get('market', 0) > 0:
            group_status += "🛒"

        table_rows.append(str([
            "club%s" % group['id'],
            group['counters'].get('photos', 0),
            group['counters'].get('albums', 0),
            group['counters'].get('videos', 0),
            group['counters'].get('audios', 0),
            group['counters'].get('audio_playlists', 0),
            group['counters'].get('podcasts', 0),
            group['counters'].get('articles', 0),
            group['counters'].get('topics', 0),
            group['counters'].get('docs', 0),
            group['counters'].get('market', 0),
            len(group.get("links", [])),
            group_status,
            group['name']]))

        status[group['id']] = group_status

    js_element = """
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'club');
        data.addColumn('number', 'photos');
        data.addColumn('number', 'albums');
        data.addColumn('number', 'videos');
        data.addColumn('number', 'audios');
        data.addColumn('number', 'audio_playlists');
        data.addColumn('number', 'podcasts');
        data.addColumn('number', 'articles');
        data.addColumn('number', 'topics');
        data.addColumn('number', 'docs');
        data.addColumn('number', 'market');
        data.addColumn('number', 'links');
        data.addColumn('string', 'status');
        data.addColumn('string', 'name');

        data.addRows([
            {ROWS}
        ]);

        var table = new google.visualization.Table(document.getElementById('table_media'));

        table.draw(data, {{showRowNumber: true, width: '100%', height: '100%'}});
    """.format(ROWS=",\n".join(table_rows))

    js_tables_elements.append(js_element)

    print("Created: media charts")

    return {
        "js_tables": "\n".join(js_tables_elements),
        "html": "\n".join(html_elements),
        "status": status
    }


def charts_population_pyramid(groups, data_source_users, section_path):
    if not os.path.exists(section_path):
        os.makedirs(section_path)

    status = {}

    js_tables_elements = []
    html_elements = []

    html_element = """
    <div class="d-block" style="margin: 10px; text-align: center; padding: 20px;">
    <h4> 👪 Users. Gender/Age Rating</h4>
    <div id="table_population_pyramid"></div>
    </div>
    <p></p>
    """

    html_elements.append(html_element)

    table_rows = []

    for group in groups:
        input_path = os.path.join(
            data_source_users, 'users_%s.csv.gz' % group['id'])

        output_path = os.path.join(
            section_path, 'population_pyramid_%s.html' % group['id'])

        df = pd.read_csv(input_path)[['sex', 'bdate']]

        df['sex'] = df['sex'] - 1

        df['bdate'] = df['bdate'].apply(
            lambda x:
                int(x.split(".")[2])
                if not pd.isnull(x) and len(x.split(".")) > 2 else None)

        df['age'] = df['bdate'].apply(
            lambda x:
                datetime.now().year - x
                if not pd.isnull(x) else None
        )

        df = df[
            (~pd.isnull(df.age)) &
            (~pd.isnull(df.sex)) &
            (df.age < 90) &
            (df.age > 5)
        ]

        if df[df.sex == 0].shape[0] > df[df.sex == 1].shape[0]:
            groups_stat = {
                "👧": df[(df.age <= 25)].shape[0],
                "👩": df[(df.age > 25) & (df.age <= 55)].shape[0],
                "👵": df[(df.age > 55)].shape[0],
            }
        else:
            groups_stat = {
                "👦": df[(df.age <= 25)].shape[0],
                "👨": df[(df.age > 25) & (df.age <= 55)].shape[0],
                "👴": df[(df.age > 55)].shape[0],
            }

        top_group = sorted(
            groups_stat.items(), key=lambda x: x[1], reverse=True)[0][0]

        table_rows.append(str([
            "club%s" % group['id'],
            df[df.sex == 0].shape[0] / df.shape[0],
            df[df.sex == 1].shape[0] / df.shape[0],
            df[df.age <= 25].shape[0] / df.shape[0],
            df[(df.age > 25) & (df.age <= 55)].shape[0] / df.shape[0],
            df[(df.age > 55)].shape[0] / df.shape[0],
            top_group,
            group['name']]))

        status[group['id']] = top_group

        build_chart_population_pyramid(df, output_path)

        rel_path = "population_pyramid/population_pyramid_%s.html" % group['id']

        img_src = group['photo_50']
        img = """
            <img src="%s" class="mr-3" style="max-width: 30px;" />
        """ % img_src if img_src else ""

        html_element = """
        <div class="club{ID} d-inline-block">
        <div class="d-block" style="margin: 10px;">
        <div class="media" style="max-width: 400px;">
        {IMG}
        <div class="media-body">
        <h5 style="max-width: 350px;">{NAME}</h5>
        <h6 style="max-width: 350px;"><a href="https://vk.com/club{ID}">club{ID}</a> {GROUP}</h6>
        </div>
        </div>
        <iframe src="{SRC}" scorlling="no" style="width: 395px; height: 395px;" frameBorder="0">
        </iframe>
        </div>
        </div>
        """.format(
            ID=group['id'],
            SRC=rel_path,
            GROUP=top_group,
            NAME=group['name'],
            IMG=img
        )

        html_elements.append(html_element)

    js_element = """
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'club');
        data.addColumn('number', 'female rate');
        data.addColumn('number', 'male rate');
        data.addColumn('number', 'young rate');
        data.addColumn('number', 'adult rate');
        data.addColumn('number', 'elderly rate');
        data.addColumn('string', 'status');
        data.addColumn('string', 'name');

        data.addRows([
            {ROWS}
        ]);

        var table = new google.visualization.Table(document.getElementById('table_population_pyramid'));

        table.draw(data, {{showRowNumber: true, width: '100%', height: '100%'}});
    """.format(ROWS=",\n".join(table_rows))

    js_tables_elements.append(js_element)

    print("Created: population pyramid")

    return {
        "js_tables": "\n".join(js_tables_elements),
        "html": "\n".join(html_elements),
        "status": status
    }


def charts_geo_sunburst(groups, data_source_users, section_path):
    if not os.path.exists(section_path):
        os.makedirs(section_path)

    status = {}

    js_tables_elements = []

    html_elements = []

    html_element = """
    <div class="d-block" style="margin: 10px; text-align: center; padding: 20px;">
    <h4>🌎 Users. Geo Rating</h4>
    <div id="table_geo"></div>
    </div>
    <p></p>
    """

    html_elements.append(html_element)

    table_rows = []

    for group in groups:
        input_path = os.path.join(
            data_source_users, 'users_%s.csv.gz' % group['id'])

        output_path = os.path.join(
            section_path, 'geo_sunburst_%s.html' % group['id'])

        df = pd.read_csv(input_path)[['id', 'country', 'city']]

        df['country'] = df['country'].apply(
            lambda x:
                ast.literal_eval(x)['title']
                if not pd.isnull(x) else "Unknown"
        )

        df['city'] = df['city'].apply(
            lambda x:
                ast.literal_eval(x)['title']
                if not pd.isnull(x) else "Unknown"
        )

        df = df[df.country != 'Unknown']

        ru_rate = df[df.country == 'Россия'].shape[0]
        msk_rate = df[df.city == 'Москва'].shape[0]

        table_rows.append(str([
            "club%s" % group['id'],
            ru_rate / df.shape[0],
            1 - ru_rate / df.shape[0],
            msk_rate / df.shape[0],
            "🇷🇺" if ru_rate / df.shape[0] > 2 / 3 else "🌐",
            group['name']]))

        status[group['id']] = (
            "🇷🇺" if ru_rate / df.shape[0] > 2 / 3 else "🌐"
        )

        build_chart_geo_sunburst(df, output_path)

        rel_path = "geo_sunburst/geo_sunburst_%s.html" % group['id']

        img_src = group['photo_50']
        img = """
            <img src="%s" class="mr-3" style="max-width: 30px;" />
        """ % img_src if img_src else ""

        html_element = """
        <div class="club{ID} d-inline-block">
        <div class="d-block" style="margin: 10px;">
        <div class="media" style="max-width: 400px;">
        {IMG}
        <div class="media-body">
        <h5 style="max-width: 350px;">{NAME}</h5>
        <h6 style="max-width: 350px;"><a href="https://vk.com/club{ID}">club{ID}</a> {GROUP}</h6>
        </div>
        </div>
        <iframe src="{SRC}" scorlling="no" style="width: 400px; height: 400px;" frameBorder="0">
        </iframe>
        </div>
        </div>
        """.format(
            ID=group['id'],
            SRC=rel_path,
            GROUP="🌎",
            NAME=group['name'],
            IMG=img
        )

        html_elements.append(html_element)

    js_element = """
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'club');
        data.addColumn('number', 'RU rate');
        data.addColumn('number', 'foreign countries rate');
        data.addColumn('number', 'MSK rate');
        data.addColumn('string', 'status');
        data.addColumn('string', 'name');

        data.addRows([
            {ROWS}
        ]);

        var table = new google.visualization.Table(document.getElementById('table_geo'));

        table.draw(data, {{showRowNumber: true, width: '100%', height: '100%'}});
    """.format(ROWS=",\n".join(table_rows))

    js_tables_elements.append(js_element)

    print("Created: geo sunburst")

    return {
        "js_tables": "\n".join(js_tables_elements),
        "html": "\n".join(html_elements),
        "status": status
    }


def charts_vk_activity(groups, data_source_users):

    ranks_info = {}
    status = {}

    def activity_group(x, last_timestamp):
        if x['deactivated'] == 'banned':
            return '6. banned'
        elif x['deactivated'] == 'deleted':
            return '5. deleted'
        elif (last_timestamp - x['last_seen']) < 24 * 60 * 60:
            return '1. last day'
        elif (last_timestamp - x['last_seen']) < 7 * 24 * 60 * 60:
            return '2. last week'
        elif (last_timestamp - x['last_seen']) < 30 * 24 * 60 * 60:
            return '3. last month'
        else:
            return '4. not active for a month'

    js_tables_elements = []
    js_charts_elements = []

    html_elements = []

    html_element = """
    <div class="d-block" style="margin: 10px; text-align: center; padding: 20px;">
    <h4>👥 Users. VK Activity Rating</h4>
    <div id="table_vk_acivity"></div>
    </div>
    <p></p>
    """

    html_elements.append(html_element)

    table_rows = []

    for group in groups:
        input_path = os.path.join(
            data_source_users, 'users_%s.csv.gz' % group['id'])

        df = pd.read_csv(input_path)[['id', 'last_seen', 'deactivated']]

        df['last_seen'] = df['last_seen'].apply(
            lambda x:
                int(ast.literal_eval(x)['time']) if not pd.isnull(x) else 0)

        last_timestamp = df.last_seen.max()

        df['activity_group'] = df.apply(
            lambda x: activity_group(x, last_timestamp),
            axis=1)

        df = (
            df.groupby('activity_group')['id'].count()
            .reset_index()
            .rename(columns={"id": "count"})
            .sort_values(by="activity_group")
        )

        stat = df.to_dict(orient='records')

        items = []

        active_cnt = 0
        all_cnt = 0

        for record in stat:
            items.append(str([record['activity_group'], record['count']]))

            if record['activity_group'][0] in {"1", "2", "3"}:
                active_cnt += record['count']

            all_cnt += record['count']

        table_rows.append(str([
            "club%s" % group['id'],
            active_cnt / all_cnt,
            1 - active_cnt / all_cnt,
            "😊" if active_cnt / all_cnt >= 0.5 else "☠️",
            group['name']]))

        status[group['id']] = "😊" if active_cnt / all_cnt >= 0.5 else "☠️"

        ranks_info[group['id']] = active_cnt / all_cnt

        js_element = """
        var data = google.visualization.arrayToDataTable([
            ['activity', 'count'],
            {ITEMS}
        ]);

        var options = {{
            title: 'User Last Activity',
            is3D: true,
            slices: {{
                0: {{color: '#28a745'}},
                1: {{color: '#007bff'}},
                2: {{color: '#ffc107'}},
                3: {{color: '#fd7e14', offset: 0.2}},
                4: {{color: '#6c757d', offset: 0.2}},
                5: {{color: '#dc3545', offset: 0.2}}
            }},
        }};

        var chart = new google.visualization.PieChart(document.getElementById('vk_activity_pie_club{ID}'));
        chart.draw(data, options);
        """.format(ITEMS=",\n".join(items), ID=group['id'])

        js_charts_elements.append(js_element)

        img_src = group['photo_50']
        img = """
            <img src="%s" class="mr-3" style="max-width: 30px;" />
        """ % img_src if img_src else ""

        html_element = """
        <div class="club{ID} d-inline-block">
        <div class="d-block" style="margin: 10px;">
        <div class="media" style="max-width: 400px;">
        {IMG}
        <div class="media-body">
        <h5 style="max-width: 350px;">{NAME}</h5>
        <h6 style="max-width: 350px;"><a href="https://vk.com/club{ID}">club{ID}</a> {GROUP}</h6>
        </div>
        </div>
        <div id="vk_activity_pie_club{ID}" style="width: 395px; height: auto;"></div>
        </div>
        </div>
        """.format(
            ID=group['id'],
            GROUP="👥",
            NAME=group['name'],
            IMG=img
        )

        html_elements.append(html_element)

    js_element = """
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'club');
        data.addColumn('number', 'active rate');
        data.addColumn('number', 'inactive rate');
        data.addColumn('string', 'status');
        data.addColumn('string', 'name');

        data.addRows([
            {ROWS}
        ]);

        var table = new google.visualization.Table(document.getElementById('table_vk_acivity'));

        table.draw(data, {{showRowNumber: true, width: '100%', height: '100%'}});
    """.format(ROWS=",\n".join(table_rows))

    js_tables_elements.append(js_element)

    print("Created: vk activity pie")

    return {
        "js_tables": "\n".join(js_tables_elements),
        "js_charts": "\n".join(js_charts_elements),
        "html": "\n".join(html_elements),
        "ranks": ranks_info,
        "status": status
    }


def charts_edu_wordcloud(groups, data_source_users, section_path):
    if not os.path.exists(section_path):
        os.makedirs(section_path)

    js_tables_elements = []
    html_elements = []

    html_element = """
    <div class="d-block" style="margin: 10px; text-align: center; padding: 20px;">
    <h4> 🎓 Users. Education rating</h4>
    <div id="table_education"></div>
    </div>
    <p></p>
    """

    html_elements.append(html_element)

    table_rows = []

    for group in groups:
        input_path = os.path.join(
            data_source_users, 'users_%s.csv.gz' % group['id'])

        output_path = os.path.join(
            section_path, 'edu_wordcloud_%s.svg' % group['id'])

        df = pd.read_csv(input_path)[['is_closed', 'university_name']]

        df = df[df['is_closed'] == False]

        titles = df[~pd.isnull(df.university_name)]['university_name'].values

        edu_rate = df[~pd.isnull(df.university_name)].shape[0]
        top_university = Counter(titles).most_common(1)

        table_rows.append(str([
            "club%s" % group['id'],
            edu_rate / df.shape[0],
            top_university[0][0] if len(top_university) else "",
            "🎓" if edu_rate / df.shape[0] > 1 / 4 else "",
            group['name']]))

        build_chart_edu_wordcloud(df, output_path)

        rel_path = "edu_wordcloud/edu_wordcloud_%s.svg" % group['id']

        img_src = group['photo_50']
        img = """
            <img src="%s" class="mr-3" style="max-width: 30px;" />
        """ % img_src if img_src else ""

        html_element = """
        <div class="club{ID} d-inline-block">
        <div class="d-block" style="margin: 10px;">
        <div class="media" style="max-width: 400px;">
        {IMG}
        <div class="media-body">
        <h5 style="max-width: 350px;">{NAME}</h5>
        <h6 style="max-width: 350px;"><a href="https://vk.com/club{ID}">club{ID}</a> {GROUP}</h6>
        </div>
        </div>
        <iframe src="{SRC}" scorlling="no" style="width: 400px; height: 400px;" frameBorder="0">
        </iframe>
        </div>
        </div>
        """.format(
            ID=group['id'],
            SRC=rel_path,
            GROUP="🎓",
            NAME=group['name'],
            IMG=img
        )

        html_elements.append(html_element)

    js_element = """
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'club');
        data.addColumn('number', 'education rate');
        data.addColumn('string', 'top university');
        data.addColumn('string', 'status');
        data.addColumn('string', 'name');

        data.addRows([
            {ROWS}
        ]);

        var table = new google.visualization.Table(document.getElementById('table_education'));

        table.draw(data, {{showRowNumber: true, width: '100%', height: '100%'}});
    """.format(ROWS=",\n".join(table_rows))

    js_tables_elements.append(js_element)

    print("Created: edu wordcloud")

    return {
        "js_tables": "\n".join(js_tables_elements),
        "html": "\n".join(html_elements)
    }


def build_dashboard(name, input_path, output_path):

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    group_info_path = os.path.join(input_path, 'group_info.json')

    with open(group_info_path, 'r') as fin:
        groups = json.load(fin)

    data_source_users = os.path.join(input_path, 'users')
    data_source_posts = os.path.join(input_path, 'posts')

    sections = {
        "likes":
            charts_likes(
                groups,
                data_source_posts
            ),
        "posts_activity":
            charts_posts_activity(
                groups,
                data_source_posts,
                os.path.join(output_path, 'calendar_heatmap')
            ),
        "media":
            charts_media(
                groups,
                data_source_posts,
                os.path.join(output_path, 'media_radar')
            ),
        "population_pyramid":
            charts_population_pyramid(
                groups,
                data_source_users,
                os.path.join(output_path, 'population_pyramid')
            ),
        "geo_location":
            charts_geo_sunburst(
                groups,
                data_source_users,
                os.path.join(output_path, 'geo_sunburst')
            ),
        "vk_activity":
            charts_vk_activity(
                groups,
                data_source_users
            ),
        "edu_wordcloud":
            charts_edu_wordcloud(
                groups,
                data_source_users,
                os.path.join(output_path, 'edu_wordcloud')
            ),
    }

    status = {}

    sections_with_statuses = [
        "geo_location",
        "population_pyramid",
        "vk_activity",
        "media",
        "likes",
        "posts_activity"
    ]

    for section in sections_with_statuses:
        for group_id, sign in sections[section]["status"].items():
            if group_id not in status:
                status[group_id] = [sign]
            else:
                status[group_id].append(sign)

    likes_ranks = sections["likes"]["ranks"]
    posts_ranks = sections["posts_activity"]["ranks"]
    activity_ranks = sections["vk_activity"]["ranks"]

    sections["main_rating"] = main_rating(
        groups,
        status,
        likes_ranks,
        posts_ranks,
        activity_ranks
    )

    dirname = os.path.dirname(os.path.abspath(__file__))

    html_template_path = os.path.join(dirname, 'static', 'index.html')
    html_output_path = os.path.join(output_path, 'index.html')

    with open(html_template_path, 'r') as fin, \
            open(html_output_path, 'w') as fout:

        data = fin.read()

        data = data.format(
            TITLE=name,
            SECTION_MAIN=sections["main_rating"]["html"],
            GOOGLE_TABLES_MAIN=sections["main_rating"]["js_tables"],
            SECTION_LIKES=sections["likes"]["html"],
            GOOGLE_TABLES_LIKES=sections["likes"]["js_tables"],
            GOOGLE_CHARTS_LIKES=sections["likes"]["js_charts"],
            SECTION_POSTS_ACTIVITY=sections["posts_activity"]["html"],
            GOOGLE_TABLES_POSTS_ACTIVITY=sections["posts_activity"]["js_tables"],
            SECTION_MEDIA=sections["media"]["html"],
            GOOGLE_TABLES_MEDIA=sections["media"]["js_tables"],
            SECTION_POPULATION_PYRAMID=sections["population_pyramid"]["html"],
            GOOGLE_TABLES_POPULATION_PYRAMID=sections["population_pyramid"]["js_tables"],
            SECTION_GEO=sections["geo_location"]["html"],
            GOOGLE_TABLES_GEO=sections["geo_location"]["js_tables"],
            SECTION_VK_ACTIVITY=sections["vk_activity"]["html"],
            GOOGLE_TABLES_VK_ACTIVITY=sections["vk_activity"]["js_tables"],
            GOOGLE_CHARTS_VK_ACTIVITY=sections["vk_activity"]["js_charts"],
            SECTION_EDUCATION=sections["edu_wordcloud"]["html"],
            GOOGLE_TABLES_EDUCATION=sections["edu_wordcloud"]["js_tables"]
        )

        fout.write(f"{data}\n")

    print(f"Generated: {html_output_path}")


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--data", help="source data", required=True)
    parser.add_argument(
        "--dashboard", help="output path", required=True)
    parser.add_argument(
        "--dashboard_name", help="dashboard name", default="Dashboard")

    args = parser.parse_args()

    build_dashboard(args.dashboard_name, args.data, args.dashboard)


if __name__ == '__main__':
    main()

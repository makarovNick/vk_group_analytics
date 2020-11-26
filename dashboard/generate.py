#!/usr/bin/env python3

import argparse
import os
import datetime
import ast
from collections import Counter
import json

import pandas as pd

from charts_utils.population_pyramid import build_chart_population_pyramid
from charts_utils.geo_sunburst import build_chart_geo_sunburst
from charts_utils.edu_wordcloud import build_chart_edu_wordcloud


def main_rating(groups, status, activity_ranks):
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

    for group in groups:
        table_rows.append(str([
            "club%s" % group['id'],
            activity_ranks[group['id']],
            "".join(status[group['id']]) if group['id'] in status else "",
            group['name']]))

    js_element = """
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'club');
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
                datetime.datetime.now().year - x
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

        html_element = """
        <div class="club{ID} d-inline-block">
        <div class="d-block" style="margin: 10px;">
        <h5 style="max-width: 400px;">{GROUP} <a href="https://vk.com/club{ID}">club{ID}</a></h5>
        <h6 style="max-width: 400px;">{NAME}</h6>
        <iframe src="{SRC}" scorlling="no" style="width: 395px; height: 395px;" frameBorder="0">
        </iframe>
        </div>
        </div>
        """.format(
            ID=group['id'], SRC=rel_path, GROUP=top_group, NAME=group['name'])

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

        build_chart_geo_sunburst(df, output_path)

        rel_path = "geo_sunburst/geo_sunburst_%s.html" % group['id']

        html_element = """
        <div class="club{ID} d-inline-block">
        <div class="d-block" style="margin: 10px;">
        <h5 style="max-width: 400px;">{GROUP} <a href="https://vk.com/club{ID}">club{ID}</a></h5>
        <h6 style="max-width: 400px;">{NAME}</h6>
        <iframe src="{SRC}" scorlling="no" style="width: 400px; height: 400px;" frameBorder="0">
        </iframe>
        </div>
        </div>
        """.format(
            ID=group['id'], SRC=rel_path, GROUP="🌎", NAME=group['name'])

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
        "html": "\n".join(html_elements)
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

        html_element = """
        <div class="club{ID} d-inline-block">
        <div class="d-block" style="margin: 10px;">
        <h5 style="max-width: 400px;">{GROUP} <a href="https://vk.com/club{ID}">club{ID}</a></h5>
        <h6 style="max-width: 400px;">{NAME}</h6>
        <div id="vk_activity_pie_club{ID}" style="width: 400px; height: 400px;"></div>
        </div>
        </div>
        """.format(ID=group['id'], GROUP="👥", NAME=group['name'])

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

        html_element = """
        <div class="club{ID} d-inline-block">
        <div class="d-block" style="margin: 10px;">
        <h5 style="max-width: 400px;">{GROUP} <a href="https://vk.com/club{ID}">club{ID}</a></h5>
        <h6 style="max-width: 400px;">{NAME}</h6>
        <iframe src="{SRC}" scorlling="no" style="width: 400px; height: 400px;" frameBorder="0">
        </iframe>
        </div>
        </div>
        """.format(
            ID=group['id'], SRC=rel_path, GROUP="🎓", NAME=group['name'])

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

    sections = {
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

    for section in {"population_pyramid", "vk_activity"}:
        for group_id, sign in sections[section]["status"].items():
            if group_id not in status:
                status[group_id] = [sign]
            else:
                status[group_id].append(sign)

    activity_ranks = sections["vk_activity"]["ranks"]

    sections["main_rating"] = main_rating(groups, status, activity_ranks)

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

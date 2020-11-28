#!/usr/bin/env python3

import plotly.express as px


def build_chart_geo_sunburst(df, output_file):
    all_cnt = df.shape[0]

    df = (
        df.groupby(['country', 'city'])['id'].count()
        .reset_index()
        .rename(columns={'id': 'count'})
    )

    df_countries = df.groupby('country')['count'].sum().reset_index()

    exclude_contries = set(
        df_countries[df_countries['count'] < all_cnt * 0.005]['country'].values
    )

    df['country'] = df[['country', 'count']].apply(
        lambda x:
            x['country']
            if x['country'] not in exclude_contries else "Other",
        axis=1
    )

    df['city'] = df[['city', 'count']].apply(
        lambda x:
            ('' if x['city'] != 'Москва' else '★ ') + x['city']
            if x['count'] >= all_cnt * 0.005 else "Other",
        axis=1
    )

    df = (
        df.groupby(['country', 'city'])['count'].sum()
        .reset_index()
    )

    df['city'] = df['city'].apply(lambda x: None if x == "" else x)

    fig = px.sunburst(
        df,
        path=['country', 'city'],
        values='count'
    )

    fig.update_layout(autosize=False, width=320, height=320)
    fig.write_html(output_file)

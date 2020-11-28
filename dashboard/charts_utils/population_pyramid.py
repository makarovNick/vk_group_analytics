#!/usr/bin/python3

import altair as alt


def build_chart_population_pyramid(df, output_file):
    df['age_group'] = (df['age'] // 2) * 2

    stat = (
        df.groupby(["sex", "age_group"])['age'].count()
        .reset_index()
        .rename(columns={"age": "count"})
    )

    max_female = stat[stat.sex == 0]['count'].max()
    max_male = stat[stat.sex == 1]['count'].max()

    left_width = int(275 * max_female / (max_female + max_male))
    right_width = 275 - left_width

    base = (
        alt.Chart(df)
        .transform_calculate(
            gender=alt.expr.if_(alt.datum.sex == 1, 'Male', 'Female')
        )
        .properties(
            width=280
        )
    )

    color_scale = alt.Scale(
        domain=['Male', 'Female'],
        range=['#1f77b4', '#e377c2']
    )

    left = (
        base
        .transform_filter(
            alt.datum.gender == 'Female'
        )
        .encode(
            y=alt.Y(
                'age_group:O',
                axis=None,
                sort=alt.SortOrder('descending')
            ),
            x=alt.X(
                'count():Q',
                title='population',
                sort=alt.SortOrder('descending')
            ),
            color=alt.Color(
                'gender:N',
                scale=color_scale,
                legend=None
            ),
            tooltip=['count():Q', 'age_group:O']
        )
        .mark_bar()
        .properties(
            title='♀ Female',
            width=left_width,
            height=300
        )
    )

    right = (
        base
        .transform_filter(
            alt.datum.gender == 'Male'
        )
        .encode(
            y=alt.Y(
                'age_group:O',
                axis=None,
                sort=alt.SortOrder('descending')
            ),
            x=alt.X(
                'count():Q',
                title='population'
            ),
            color=alt.Color(
                'gender:N',
                scale=color_scale,
                legend=None
            ),
            tooltip=['count():Q', 'age_group:O']
        )
        .mark_bar()
        .properties(
            title='♂ Male',
            width=right_width,
            height=300
        )
    )

    chart = alt.concat(left, right, spacing=5).resolve_scale(
        y='shared'
    )

    chart.save(output_file)

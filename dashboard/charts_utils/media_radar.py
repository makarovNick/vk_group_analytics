#!/usr/bin/env python3

import plotly.express as px
import pandas as pd


def build_chart_media_radar(data, output_file):
    df = pd.DataFrame(dict(
        count=list(data.values()),
        attachment=list(data.keys())
    ))

    fig = px.line_polar(df, r='count', theta='attachment', line_close=True)
    fig.update_layout(autosize=False, width=320, height=320)
    fig.write_html(output_file)

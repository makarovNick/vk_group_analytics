from tools.utils import get_group_stats, get_group_id, date_n_days_ago
from parser.parser import parse_stats

from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import dash

def make_dash(groups, post_stats = None, member_stats = None, info_stats = None):
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    app.layout = html.Div(children=[
        html.H1(children='Сравнение групп ВК'),
        generate_table(groups, post_stats, member_stats, info_stats),
        html.Div([
            html.Label('Dropdown'),
            dcc.Dropdown(
                id='drop',
                options=[
                    {"label" : "comments", "value" : "comments"},
                    {"label" : "likes", "value" : "likes"},
                    {"label" : "subscribed", "value" : "subscribed"},
                    {"label" : "unsubscribed", "value" : "unsubscribed"},
                    {"label" : "total_views", "value" : "total_views"},
                    {"label" : "mobile_views", "value" : "mobile_views"},
                    {"label" : "total_visitors", "value" : "total_visitors"},
                    {"label" : "mobile_reach", "value" : "mobile_reach"},
                    {"label" : "total_reach", "value" : "total_reach"},
                    {"label" : "reach_subscribers", "value" : "reach_subscribers"},
                    {"label" : "f_visitors", "value" : "f_visitors"},
                    {"label" : "m_visitors", "value" : "m_visitors"},
                    {"label" : "age_visitors", "value" : "age_visitors"},
                    {"label" : "RU_visitors", "value" : "RU_visitors"},
                    {"label" : "NOTRU_visitors", "value" : "NOTRU_visitors"},
                    {"label" : "f_reach", "value" : "f_reach"},
                    {"label" : "m_reach", "value" : "m_reach"},
                    {"label" : "age_reach", "value" : "age_reach"},
                    {"label" : "RU_reach", "value" : "RU_reach"},
                    {"label" : "NOTRU_reach", "value" : "NOTRU_reach"},
                ],
                value='likes'
            ),

            html.Label('Checkboxes'),
            dcc.Checklist(
                id='check',
                options=[
                    {'label': name, 'value': i} for i, name in enumerate(groups)
                ],
                value=[0]
            ),
            dcc.Graph(id='plot'),
        ])
    ])
    stats = [parse_stats(get_group_stats(get_group_id(g), date_n_days_ago(100).timestamp())) for g in groups]
    dfs = [pd.DataFrame(stat) for stat in stats]
    for df in dfs:
        df.index = [date_n_days_ago(df.shape[0] - i).strftime("%d.%m.%Y") for i in df.index]

    @app.callback(Output('plot', 'figure'), [Input('drop', 'value'), Input('check', 'value')])
    def draw_graph(selected_type, selected_grops):
        fig = px.scatter()
        if selected_type in ['age_visitors' , 'age_reach']:
            fig = px.bar(hover_name=dfs[0].columns[12:19])
            if len(selected_grops) != 0:
                for group in selected_grops:
                    fig.add_bar(y=dfs[group].iloc[0, 12:19], name=groups[group])
                    fig.update_traces(marker_color=group)
            
            fig.update_xaxes(title='ages')
            fig.update_yaxes(title='count')
        
        else:
            if len(selected_grops) != 0:
                for group in selected_grops:
                    fig.add_scatter(y=dfs[group][selected_type], x=dfs[group].index, name=groups[group])

                # fig.update
            fig.update_traces(mode='lines+markers')
            fig.update_xaxes(title='date')
            fig.update_yaxes(title=selected_type)
        
        return fig

    app.run_server(debug=True)

def generate_table(groups, *stats):
    table = []
    for d in stats:
        if d is None:
            continue
        keys = sorted(d, key=lambda x:-len(x.keys()))[0].keys()
        for k in keys:
            table.append(
                [k, *[str(st.get(k, None)) for st in d]]
            )

    df = pd.DataFrame(table, columns=['feature'] + groups)
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in df.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(df.iloc[i][col]) for col in df.columns
            ]) for i in range(len(df))
        ])
    ])

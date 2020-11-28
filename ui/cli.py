from rich.console import Console
from rich.table import Table

# import termplotlib as tpl

def draw_table(groups, *stats):
    console = Console()
    table = Table(show_header=True, header_style="bold magenta")

    table.add_column('feature/screen_name')
    for g in groups:
        table.add_column(g)
    for d in stats:
        keys = sorted(d, key=lambda x: -len(x.keys()))[0].keys()
        for k in keys:
            table.add_row(
                k, *[str(st.get(k, "No access")) for st in d]
            )
    console.print(table)

# def draw_plot(x, y, label=None, x_label=None, y_label=None):
#     fig = tpl.figure()
#     fig.plot(x=x, y=y, width=60, height=20, ylim=[0, max(y) + 100],
#              xlabel=x_label, extra_gnuplot_arguments=f'set y2label "{y_label}"')
#     fig.show()

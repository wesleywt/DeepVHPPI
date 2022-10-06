import pandas as pd
import json
import plotly.express as px

def show_graph(df, metric, title):
    fig = px.line(df, x='epoch', y=metric, title=title)
    fig.show()


def log_to_pandas(path_to_log_file):
    with open(path_to_log_file, 'r') as f:
        log = json.load(f)
    log_df = pd.DataFrame([log]).T
    normalized = pd.json_normalize(log_df[0])
    log_df = normalized.reset_index().rename({'index': 'epoch'}, axis='columns')
    return log_df

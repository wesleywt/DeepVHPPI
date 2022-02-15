import typing

import pandas as pd
import plotly.express as px
import json


def create_log_df(log_file: typing.Dict) -> pd.DataFrame:
    log_df = pd.DataFrame([log_file]).T
    normalized_log_df = pd.json_normalize(log_df[0])
    log_df = normalized_log_df.reset_index().rename({'index': 'epoch'}, axis='columns')
    return log_df


def create_plot(df, metric='loss'):  # loss, acc, auc, aupr, all
    if metric == 'loss':
        plot_loss = px.line(df, x=df['epoch'], y=df['loss'])
        plot_loss.show()

    elif metric == 'acc':
        plot_acc = px.line(df, x=df['epoch'], y=df['acc'])
        plot_acc.show()

    elif metric == 'auc':
        plot_auc = px.line(df, x=df['epoch'], y=df['auc'])
        plot_auc.show()

    elif metric == 'aupr':
        plot_aupr = px.line(df, x=df['epoch'], y=df['aupr'])
        plot_aupr.show()

    elif metric == 'all':
        plot_loss = px.line(df, x=df['epoch'], y=df['loss'])
        plot_loss.show()
        plot_acc = px.line(df, x=df['epoch'], y=df['acc'])
        plot_acc.show()
        plot_auc = px.line(df, x=df['epoch'], y=df['auc'])
        plot_auc.show()
        plot_aupr = px.line(df, x=df['epoch'], y=df['aupr'])
        plot_aupr.show()
    else:
        print('Not a valid metric, try loss, acc, auc, aupr or all')


if __name__ == '__main__':
    with open("../results/ppi.bert._bacteria_01-02-2022/train_log.json") as f:
        log = json.load(f)

    training_log_df = create_log_df(log)
    create_plot(training_log_df, metric='acc')

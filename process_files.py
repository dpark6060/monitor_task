import pandas as pd
import seaborn as sb
import numpy as np
import matplotlib.pyplot as pl
import os
import re
from datetime import datetime, timedelta
from pathlib import Path
import pathlib
WORKDIR = pathlib.Path(__file__).parent.resolve()

FILENAME="top_output.txt"
DATE_FORMAT="%Y-%m-%d %H:%M:%S"
filename=FILENAME
TIMESTAMP_COL = "TIMESTAMP"
WORKDIR = WORKDIR / "outputs"

if not WORKDIR.exists():
    WORKDIR.mkdir()

def is_timestamp(test_str):
    try:
        res = bool(datetime.strptime(test_str, DATE_FORMAT))
    except ValueError:
        res = False
    return res

def format_delimiter(filename, delimiter=',', overwrite=False):
    """Format a file to a specific delimiter

    Args:
        filename: the name of the file to format
        delimiter: the delimiter to format the file to

    Returns:
        formatted_filename: the name of the formatted file
    """
    formatted_filename = filename.split('.')[0] + '_formatted.' + filename.split('.')[1]
    if os.path.exists(formatted_filename) and overwrite is False:
        return formatted_filename
    elif overwrite:
        os.remove(formatted_filename)

    with open(filename, 'r') as f:
        with open(formatted_filename, 'w') as f1:
            for line in f:
                f1.write(re.sub("\s+", delimiter, line)+"\n")
    return formatted_filename


def load_report(filename, delimiter=','):
    """Load a report from a file

    Args:
        filename: the name of the file to load

    Returns:
        report: the report as a pandas dataframe
    """
    return pd.read_csv(filename, delimiter=delimiter)


def datetime_range(start, n, delta):
    current = start
    iter = 0
    while iter < n:
        yield current
        current += delta
        iter += 1


def add_timestamp_to_df(df):
    if df.columns[-1].startswith("Unnamed"):
        df = df.drop(df.columns[-1], axis=1)
    if is_timestamp(df.columns[-1]):
        old_name = df.columns[-1]
        df = df.rename(columns={old_name: TIMESTAMP_COL})
        return df

    timestamp_range = [dt.strftime(DATE_FORMAT) for dt in datetime_range(
                        datetime(2024,1,1,1),
                        len(df),
                        timedelta(minutes=1))
                       ]
    df.insert(len(df.columns), TIMESTAMP_COL, timestamp_range)
    return df



def make_plot_report(df, x_col, y_cols, title, xlabel, ylabels, filename):
    """Make a plot from a report

    Args:
        df: the report as a pandas dataframe
        x_col: the column to use for the x axis
        y_cols: the columns to use for the y axis
        title: the title of the plot
        xlabel: the label for the x axis
        ylabel: the label for the y axis
        filename: the name of the file to save the plot to
    """
    n_plots = len(y_cols)
    f, axarr = pl.subplots(n_plots, sharex=True)
    for i, col_name in enumerate(y_cols):
        sb.pointplot(x=x_col, y=col_name, data=df, marker=".", ax=axarr[i])
    ax=axarr[-1]
    xticks = ax.get_xticks()
    new_xticks = [pd.to_datetime(tm, unit='m') for tm in xticks]
    for i in range(0,len(new_xticks),2):
        new_xticks[i] = ""
    # convert all xtick labels to selected format from ms timestamp
    ax.set_xticklabels(new_xticks,
                       rotation=45, ha="right")
    pl.show()

def format_mem(item):
    if item.endswith("K"):
        mult_fact = 1024
    elif item.endswith("M"):
        mult_fact = 1
    item=int(item[:-1])*mult_fact
    return item

def format_columns(df):
    df['MEM'] = df['MEM'].apply(format_mem)
    df[TIMESTAMP_COL] = pd.to_datetime(df[TIMESTAMP_COL], format=DATE_FORMAT)
    df[TIMESTAMP_COL] = df[TIMESTAMP_COL]-df[TIMESTAMP_COL][0]


    return df


def main():
    formatted_file = format_delimiter(FILENAME)
    df = load_report(formatted_file)
    df = add_timestamp_to_df(df)
    df = format_columns(df)

    columns_of_interest = ["%CPU", "MEM"]
    x_axis_col = TIMESTAMP_COL
    title= "CPU and Memory Usage"
    xlabel = "Time"

    name = formatted_file.split('.')[0] + 'report.png'
    filename = WORKDIR / name
    make_plot_report(df=df, x_col=x_axis_col, y_cols=columns_of_interest, title=title, xlabel=xlabel, ylabels=columns_of_interest, filename=filename)


if __name__ == "__main__":
    main()
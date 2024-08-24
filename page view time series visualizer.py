import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv", parse_dates=["date"], index_col="date")

# Clean data
df = df[
    (df["value"] >= df["value"].quantile(0.025)) &
    (df["value"] <= df["value"].quantile(0.975))
]


def draw_line_plot():
    # Create a copy of the cleaned DataFrame
    df_line = df.copy()

    # Draw line plot
    fig, ax = plt.subplots(figsize=(15, 6))
    ax.plot(df_line.index, df_line["value"], color="r", linewidth=1)
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')


def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()

    # Extract year and month from the date column
    df_bar["year"] = df_bar.index.year
    df_bar["month"] = df_bar.index.month_name()

    # Group data by year and month and calculate the average page views
    df_bar = df_bar.groupby(["year", "month"])["value"].mean().unstack()

    # Define the order of months
    month_order = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    # Draw bar plot
    fig, ax = plt.subplots(figsize=(10, 6))
    df_bar.plot(kind="bar", ax=ax)
    ax.set_xlabel("Years")
    ax.set_ylabel("Average Page Views")
    ax.set_xticklabels(df_bar.index, rotation=45)
    ax.legend(title="Months", labels=month_order)

    # Save image and return fig
    fig.savefig('bar_plot.png')


def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    # Year-wise box plot
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")
    axes[0].set_title("Year-wise Box Plot (Trend)")

    # Month-wise box plot
    sns.boxplot(x='month', y='value', data=df_box, ax=axes[1],
                order=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")
    axes[1].set_title("Month-wise Box Plot (Seasonality)")

    # Save image and return fig
    fig.savefig('box_plot.png')

# Call the functions to generate and save plots
draw_line_plot()
draw_bar_plot()
draw_box_plot()

plt.show()

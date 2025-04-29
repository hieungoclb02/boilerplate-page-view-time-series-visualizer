import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv',index_col='date')
# Clean data
df = df[(df.value >= df.value.quantile(0.025))&
(df.value<=df.value.quantile(0.975))]
# print(df.head(5))

df.index=pd.to_datetime(df.index)
month_list=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
full_month_list=['January','February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
colors= [plt.cm.tab10(i % 10) for i in range(20)]

def draw_line_plot():
    # Draw line plot
    fig,ax=plt.subplots(figsize=(15,5))
    ax.plot(df.index,df.value,'red')
    ax.set(title='Daily freeCodeCamp Forum Page Views 5/2016-12/2019',xlabel='Date',ylabel='Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig
# draw_line_plot()
def draw_bar_plot():
    x_indexes= [0,1,2,3]
    df_bar = df.copy()
    df_bar.reset_index(inplace=True)
    df_bar['year']=[d.year for d in df_bar.date]
    df_bar['month']=[d.strftime('%b') for d in df_bar.date]
    
    #cần: {2016:(month1, month2, month3,...)}
    df_2016=df_bar[df_bar['year']==2016].groupby('month')['value'].mean().to_dict()
    df_2016={month:df_2016[month] for month in month_list if month in df_2016}
    df_2017=df_bar[df_bar['year']==2017].groupby('month')['value'].mean().to_dict()
    df_2017={month:df_2017[month] for month in month_list if month in df_2017}
    df_2018=df_bar[df_bar['year']==2018].groupby('month')['value'].mean().to_dict()
    df_2018={month:df_2018[month] for month in month_list if month in df_2018}
    df_2019=df_bar[df_bar['year']==2019].groupby('month')['value'].mean().to_dict()
    df_2019={month:df_2019[month] for month in month_list if month in df_2019}
    # print(df_2016)
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # ax[0].bar(x_indexes,df_2016.values())
    # ax[1].bar(x_indexes,df_2017.values())
    bar_width=0.05
    for i in range(12):
        ax.bar(x_indexes[0] + i * bar_width - 0.3, df_2016.get(month_list[i], np.nan), width=bar_width, color=colors[i],label=full_month_list[i] if x_indexes[0] == 0 else None)
        ax.bar(x_indexes[1] + i * bar_width - 0.3, df_2017.get(month_list[i], np.nan), width=bar_width, color=colors[i])
        ax.bar(x_indexes[2] + i * bar_width - 0.3, df_2018.get(month_list[i], np.nan), width=bar_width, color=colors[i])
        ax.bar(x_indexes[3] + i * bar_width - 0.3, df_2019.get(month_list[i], np.nan), width=bar_width, color=colors[i])
    ax.set(ylabel='Average Page Views',xlabel='Years')
    ax.set_xticks(x_indexes)
    ax.set_xticklabels([2016,2017,2018,2019],rotation=90)
    
    ax.legend(loc="upper left", title="Months")
    fig.savefig('bar_plot.png')
    return fig
# draw_bar_plot()
def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, ax = plt.subplots(1, 2, figsize=(20, 5))

    # Year-wise Box Plot
    sns.boxplot(data=df_box, x='year', y='value', hue='year', ax=ax[0], palette='tab10', hue_order=sorted(df_box['year'].unique()))
    ax[0].set(title='Year-wise Box Plot (Trend)', ylabel='Page Views', xlabel='Year')
    

    # Month-wise Box Plot
    sns.boxplot(data=df_box, x='month', y='value', hue='month', ax=ax[1], order=month_list, palette='tab10')
    ax[1].set(title='Month-wise Box Plot (Seasonality)', ylabel='Page Views', xlabel='Month')
    
    # Save figure
    fig.savefig('box_plot.png')
    plt.close(fig)
    return fig
# draw_box_plot()

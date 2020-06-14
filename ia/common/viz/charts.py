import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mtick
import matplotlib.patches as mpatches
import numpy as np
import datetime

def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{p:1.0f}%\n({v:d})'.format(p=pct,v=val)
    return my_autopct


def pie_chart(labels, values,title=None, explode=None):
    f = plt.figure(1, figsize=(8,4))
    ax1 = f.add_subplot(111)
    patches, texts, autotexts = ax1.pie(values, explode=explode, labels=labels, labeldistance=1.05, autopct=make_autopct(values), textprops={'fontsize': 12})#shadow=True)
    ax1.axis('equal') 
    if title:
        ax1.set_title(f'{title}\n', fontsize="15")
    f.tight_layout()
    return plt


def pie_charts(stats_list, fig_num=None, title=None, sub_titles=None):
    no_charts = len(stats_list)
    f = plt.figure(fig_num, figsize=(15,5*no_charts))
    if title:
        f.suptitle(title, fontsize=16)

    for sq, s in enumerate(stats_list, start=1):
        title = sub_titles[sq-1] if sub_titles else None
        lv = list(s.items())
        lv_sorted_by_value = sorted(lv, key=lambda p: p[1])
        labels = [x for x,_ in lv_sorted_by_value]
        values = [y for _, y in lv_sorted_by_value]

        ax = f.add_subplot(no_charts, 1, sq)
        explode = (0.01,)*len(s)
        patches, texts, autotexts = ax.pie(
            values, 
            explode=explode, 
            labels=labels, 
            labeldistance=1.05, 
            autopct=make_autopct(values), 
            textprops={'fontsize': 12}
        )
        ax.axis('equal')
        if title:
            ax.set_title(f'{title}\n', fontsize="15")
    f.tight_layout()
    return plt


def bar_chart_by_dates(dates, values, color='blue'):
    f = plt.figure(1, figsize=(8,4))
    ax = f.add_subplot(111)

    # formatter = mdates.DateFormatter("%Y-%m-%d")
    # ax.xaxis.set_major_formatter(formatter)

    # locator = mdates.DayLocator()
    # ax.xaxis.set_major_locator(locator)
    dates = [f'{x:%Y-%m-%d}' for x in dates]

    ax.bar(dates, values, color=color)
    f.tight_layout()
    return plt


def bar_chart_percent_stacked(dates, total_counts, part_counts):
    f = plt.figure(1, figsize=(8,4))
    ax = f.add_subplot(111)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())

    green_bar = []
    red_bar = []

    for i, _ in enumerate(dates):
        green_bar_size = round((total_counts[i] - part_counts[i])*100/total_counts[i])
        red_bar_size = round(part_counts[i]*100/total_counts[i])
        green_bar.append(green_bar_size)

        ax.text(i, green_bar_size, f'{green_bar_size}%', fontsize=12, ha='center', color='yellow' if green_bar_size<95 else 'black')
        ax.text(i, green_bar_size/2., f'{(total_counts[i] - part_counts[i])}', fontsize=8, ha='center', color='white')
        if part_counts[i] > 0:
            ax.text(i, green_bar_size + red_bar_size/2., f'{part_counts[i]}', fontsize=8, ha='center', color='white')
        red_bar.append(red_bar_size)
    
    dates = [f'{d:%m-%d}' for d in dates]
    plt.bar(dates, green_bar, color='green', label="independent")
    plt.bar(dates, red_bar, bottom=green_bar, color='red', label="with dependency")
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=False, ncol=2)
    return plt


def barh_progress(labels, done_on_time, done_later=None, title=None, invert_labels=True):
    f = plt.figure(1, figsize=(8,4))
    ax = f.add_subplot(111)

    ax.xaxis.set_major_formatter(mtick.PercentFormatter())

    y_pos = range(len(labels))
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels)

    for i, _ in enumerate(labels):
        grey_size = 100
        done_on_time_size = done_on_time[i]
        grey_size -= done_on_time_size
        ax.barh(y_pos[i], done_on_time_size, color='green', edgecolor='white')

        if done_on_time_size:
            ax.text(done_on_time_size/2., y_pos[i], f'{done_on_time_size}%', fontsize=10, va='center', color='white')

        if done_later is not None:
            done_later_size = done_later[i]
            grey_size -= done_later_size
            ax.barh(y_pos[i], done_later_size, left=done_on_time_size, color='#b5ffb9', edgecolor='white')
            if done_later_size:
                ax.text(done_on_time_size + done_later_size/2., i, f'{done_later_size}%', fontsize=10, va='center', color='black')

            done_on_time_patch = mpatches.Patch(color='green', label='done on time')
            done_later_patch = mpatches.Patch(color='#b5ffb9', label='done later')
            plt.legend(handles=[done_on_time_patch, done_later_patch], loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=False, ncol=2)
        ax.barh(y_pos[i], grey_size, left=100-grey_size, color='lightgrey', edgecolor='white')
    if invert_labels:
        ax.invert_yaxis()
    if title is not None:
        ax.set_title(title)
    f.tight_layout()
    return plt
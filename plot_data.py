from urllib.request import urlopen
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit

plt.rcParams['text.usetex'] = True
plt.rcParams['font.serif'] = ['Computer Modern Roman'] + plt.rcParams['font.serif']

country_names = ['australia', 'uk', 'us', 'italy', 'spain', 'france', 'germany', 'iran']
colours = ['tab:green', 'tab:orange', 'tab:red', 'tab:blue', 'tab:purple', 'tab:pink', 'tab:brown', 'tab:cyan',
           'tab:olive', '#FF1493', 'navy', '#aaffc3', 'lightcoral', '#228B22', '#aa6e28', '#FFA07A']
lookback_time_in_days = -10

base_url = 'https://www.worldometers.info/coronavirus/country/'
font = {'family': 'normal',
        'size': 15}
matplotlib.rc('font', **font)


def get_data(webpage):
    dates = str(webpage).split('categories: ')[1].split('\\n')[0].replace('[', '').replace(']', '').replace('"','').split(',')

    names = []
    data = []
    for line in str(webpage).split('series: ')[1:]:
        keys = line.split(': ')

        done = 0
        for k, key in enumerate(keys):
            if 'name' in key:
                name = keys[k + 1].replace("\\'", "").split(',')[0]
                names.append(name)
                done += 1
            if 'data' in key:
                datum = keys[k + 1].replace('[', '').split(']')[0].split(',')
                data.append(datum)
                done += 1
            if done == 2:
                break

    return dates, names, data


country_data = {}
for i, country in enumerate(country_names):
    url = base_url + country

    f = urlopen(url)
    webpage = f.read()

    dates, names, data = get_data(webpage)

    country_data[country] = {'dates': dates, 'titles': names, 'data': data}

titles = ['Cases', 'Deaths']
for title in titles:
    fig_linear, ax_linear = plt.subplots(1, 1, figsize=(9,6))
    fig_log, ax_log = plt.subplots(1,1, figsize=(9,6))

    for i, c in enumerate(country_names):
        print(c)
        title_index = country_data[c]['titles'].index(title)
        dates = country_data[c]['dates']
        xdata = np.arange(len(dates))
        ydata = country_data[c]['data'][title_index]
        ydata = np.array(ydata).astype('float')

        sidx = lookback_time_in_days
        b, logA = np.polyfit(xdata[sidx:], np.log(ydata[sidx:]), 1)
        log_yfit = b * xdata[sidx:] + logA
        lin_yfit = np.exp(logA) * np.exp(b * xdata[sidx:])

        ax_linear.plot(dates, ydata, label=f'{c.upper():<12s}: ${np.exp(b):.2f}^t$ ({np.log(2)/b:.1f} days to double)', marker='.', color=colours[i])
        ax_linear.plot(xdata[sidx:], lin_yfit , color=colours[i], linestyle=':', alpha=1)
        ax_log.plot(dates, np.log(ydata), label=f'${c.upper()}: {np.exp(b):.2f}^t$', marker='.', color=colours[i])
        ax_log.plot(xdata[sidx:], log_yfit, color=colours[i], linestyle=':', alpha=1)
        # label=f'{c.upper()}: {np.exp(logA):.2f}*{np.exp(b):.2f}^t'

    ax_linear.tick_params(rotation=90)
    ax_linear.set_ylabel(title)
    ax_linear.legend()
    fig_linear.tight_layout()
    fig_linear.savefig(f'{title}_linear.pdf')

    ax_log.tick_params(rotation=90)
    ax_log.set_ylabel('log ' + title)
    ax_log.legend()
    # ax_log.set_yscale('log')
    fig_log.tight_layout()
    fig_log.savefig(f'{title}_log.pdf')
    plt.show()








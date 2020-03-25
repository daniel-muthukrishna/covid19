from urllib.request import urlopen

def get_data(country_name):
    return get_data_from_worldometer(country_name)


def get_data_from_worldometer(country_name):
    base_url = 'https://www.worldometers.info/coronavirus/country/'
    url = base_url + country_name
    f = urlopen(url)
    webpage = f.read()
    dates = str(webpage).split('categories: ')[1].split('\\n')[0].replace('[', '').replace(']', '').replace('"','').replace('},', '').replace('},', '').replace('  ', '').split(',')

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


if __name__ == '__main__':
    country_list = ['australia', 'uk', 'us', 'italy', 'spain', 'germany', 'iran',
                    'france', 'ireland', 'china', 'south-korea', 'switzerland', 'netherlands',
                    'austria', 'belgium', 'norway', 'sweden', 'portugal', 'brazil', 'canada',
                    'denmark', 'malaysia', 'poland', 'greece', 'indonesia', 'philippines',
                    'china-hong-kong-sar', 'iraq', 'algeria']

    country_data = {}
    for i, country in enumerate(country_list):
        dates, names, data = get_data(country)
        country_data[country] = {'dates': dates, 'titles': names, 'data': data}

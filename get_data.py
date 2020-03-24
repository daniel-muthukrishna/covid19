from urllib.request import urlopen

COUNTRY_LIST = ['australia', 'uk', 'us', 'italy', 'spain', 'germany', 'iran',
                'france', 'ireland', 'china', 'south-korea', 'switzerland', 'netherlands',
                'austria', 'belgium', 'norway', 'sweden', 'portugal', 'brazil', 'canada',
                'denmark', 'malaysia', 'poland', 'greece', 'indonesia', 'philippines',
                'china-hong-kong-sar', 'iraq', 'algeria']


def get_data(webpage):
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
    base_url = 'https://www.worldometers.info/coronavirus/country/'

    country_data = {}
    for i, country in enumerate(COUNTRY_LIST):
        url = base_url + country
        f = urlopen(url)
        webpage = f.read()

        dates, names, data = get_data(webpage)
        country_data[country] = {'dates': dates, 'titles': names, 'data': data}

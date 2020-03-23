

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
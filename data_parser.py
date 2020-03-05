import os, json
from functools import reduce


def cut_points(data, top):
    points = []
    for i in range(top):
        for line in data:
            if line[i] != ' ':
                break
        else:
            points.append(i)

    single_points = [-1, points[0]]
    for p in points[1:]:
        if p == single_points[-1] + 1:
            single_points[-1] = p
        else:
            single_points.append(p)
    return single_points


def daily_programs(data, week):
    days = []
    for i in range(7):
        days.append([x[i] for x in data])
    clean_days = []
    for day in days:
        clean_days.append([])
        for line in day:
            if line != '':
                try:
                    start = line[:5].split(':')
                    assert len(start) == 2 and len(start[0]) == 2 and len(start[1]) == 2
                    h, m = int(start[0]), int(start[1])
                    assert h < 25 and m < 60
                    clean_days[-1].append(line)
                except:
                    if len(clean_days[-1]):
                        clean_days[-1][-1] += f" {line}" 
    return {week[i]:clean_days[i] for i in range(7)}


def channels_programs(data, points, dates, tv_channels):
    channels, blocks = [], []
    for line in data:
        element = line.strip()
        if element in tv_channels:
            channels.append(element)
            blocks.append([])
        else:
            daily = []
            for i in range(1, len(points)):
                daily.append(line[points[i - 1] + 1:points[i]].strip())
            if daily[0] in tv_channels:
                channels.append(daily[0])
                blocks.append([])
                daily[0] = ''
            blocks[-1].append(daily)
    return {channels[i]:daily_programs(blocks[i], dates) for i in range(len(blocks))}


def main(args):
    year, d = "2019", {}
    files = [x for x in os.listdir(args.path) if x[-5:] == ".data"]
    dates = ['Domingo', 'Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado']
    channels = ["CUBAVISIÓN", "TELE REBELDE", "CANAL EDUCATIVO", "CANAL EDUCATIVO/2", "MULTIVISIÓN"]

    for file in files:
        with open(f"{args.path}/{file}", 'r') as fd:
            text = fd.read()
        _, month, day, _ = file.split('-')

        raw_data = text.split('\n')[2:-3]
        data = [x for x in raw_data if x.strip() not in channels]
        top = reduce(lambda x, y: max(x, len(y)), data, 0) + 1
        data = [x + ' ' * (top - len(x)) for x in data]

        # dates = [f'{days[i]} {i + int(day)}' for i in range(7)]
        points = cut_points(data, top)
        d[f"{day}/{month}/{year}"] = channels_programs(raw_data, points, dates, channels)

    with open(args.dir, 'w') as fd:
        fd.write(json.dumps(d, indent=4, ensure_ascii=False))      


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='CineTV data parser')
    parser.add_argument('-p', '--path', type=str, default='Files/data/', help='path of the data files')
    parser.add_argument('-d', '--dir', type=str, default='Files/db/CineTV-DB.json', help='file to save the DB')
    
    args = parser.parse_args()
    main(args)
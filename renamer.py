import os
from downloader import tostr, next_date

f = lambda x,y: f"2019-{y}-{x}.pdf"

def generate_all_dates():
    m, d, l = 1, 13, []
    while m < 13:
        l.append(tostr(m, d, f))
        d, m = next_date(m, d)
    return l

def main(args):
    bad_days = [(24, 2), (4, 8), (6, 10)]
    uninformative_days = [(24, 2), (4, 8), (20, 1), (10, 3), (17, 3), (24, 3), (14, 4), (21, 4), (12, 5), (20, 10)]
    bad_names = list(map(lambda x: tostr(x[1], x[0], f), bad_days))
    uninformative = list(map(lambda x: tostr(x[1], x[0], f), uninformative_days))
    path = args.path
    data = [x for x in generate_all_dates() if x not in bad_names]
    files = [x for x in os.listdir(path) if "icultura" in x]

    for file in files:
        name = data[int(file.split('.')[2])]
        if name not in uninformative:
            os.rename(f"{path}/{file}", f"{path}/{name}")
    files = [x for x in os.listdir(path) if "icultura" in x]

    for file in files:
        os.remove(f"{path}/{file}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='CineTV pdf renamer')
    parser.add_argument('-p', '--path', type=str, default='Files/pdf/', help='path of the data files')
    
    args = parser.parse_args()
    main(args)
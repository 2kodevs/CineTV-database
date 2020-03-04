month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

def next_date(m, d):
    newd = d + 7
    newd = newd - month[m] * (newd > month[m])
    if newd < d:
        m += 1
    return newd, m

format = lambda x, y: f"{y}/{x}"
num_str = lambda x: str(x) if x >= 10 else f"0{str(x)}"

def tostr(m, d, f=format):
    month = num_str(m)
    day = num_str(d)

    return f(day, month)

def main():
    url1 = 'http://www.juventudrebelde.cu/printed/2019/'
    url2 = '/icultura.pdf'

    m = 1
    d = 13
    urls = []
    while m < 13:
        urls.append(url1 + tostr(m, d) + url2)
        d, m = next_date(m, d)

    print(' '.join(urls))

if __name__ == "__main__":
    main()
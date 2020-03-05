import os
from pdftotext import PDF

def main(args):
    files = [x for x in os.listdir(args.path) if x[-4:] == ".pdf"]

    for file in files:
        with open(f"{args.path}/{file}", 'rb') as fd:
            pdf = PDF(fd)
        idx, name = 0, file.split('.')[0]
        for page in pdf:
            line = page.split("\n")[0].split()
            if len(line) == 10 and "CARTELERA" in line:
                with open(f"{args.folder}{name}-page{idx}.data", 'w') as fd:
                    fd.write(page)
    
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='CineTV page filter')
    parser.add_argument('-p', '--path', type=str, default='Files/pdf/', help='path of the pdf files')
    parser.add_argument('-f', '--folder', type=str, default='Files/data/', help='destination folder')
    
    args = parser.parse_args()
    main(args)
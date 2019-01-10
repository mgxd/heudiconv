import pandas as pd
import os.path as op
from heudiconv.utils import seqinfo_fields
import argparse

UNUSED_FIELDS = [
    'total_files_till_now',
    'example_dcm_file',
    'unspecified2',
    'unspecified3',
]

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('dicominfo', help='Path to dicominfo.tsv')
    parser.add_argument('--sonic', action='store_true', help='Print all rows instantly')
    return parser

def main():
    args = get_args().parse_args()

    if not op.exists(args.dicominfo):
        print("Dicominfo not found")
        sys.exit(1)

    seqinfo = pd.read_csv(args.dicominfo, sep='\t')

    print("Expanding dicominfo", end='\n\n')
    for seq in range(len(seqinfo)):
        for i in range(len(seqinfo_fields)):
            if seqinfo_fields[i] in UNUSED_FIELDS:
                continue
            print(seqinfo_fields[i], '\t', seqinfo.iloc[seq, i])
        print() 
        if not args.sonic:
            if input('Press return to continue, or q to quit\n').lower() == 'q':
                break

if __name__ == "__main__":
    main()

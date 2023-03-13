import pickle
import json
import numpy as np
from argparse import ArgumentParser
def main():
    parser = ArgumentParser()
    parser.add_argument('file',help='pkl file')
    parser.add_argument('--result',help='result file')

    args=parser.parse_args()
    with open(args.file,'rb') as f:
        data=pickle.load(f)

    if args.result is None:
        pathlist = args.file.split('/')
        args.result=pathlist[-1]+'.txt'

    with open(args.result,'w') as f:
        f.write(str(data))


if __name__=='__main__':
    main()

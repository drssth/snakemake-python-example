import sys, os, os.path
import json
import numpy
import pandas
import logging
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--csvpath', type=str, default='iris.csv', help='data path of csv files')
parser.add_argument('--cols', type=str, default='sepal.length,sepal.width,petal.length,petal.width', help='numerical cols of csv data')
parser.add_argument('--target', type=str, default='variety', help='target col of csv data')
parser.add_argument('--outpath', type=str, default='generator/data.npz', help='output path')
parser.add_argument('--targetjson', type=str, default='generator/targets.json', help='output path')
parser.add_argument('--logpath', type=str, default='log-generate-numbers.log', help='log filename')



def init_logging(logfn):
    if os.path.exists(logfn):
        pass
    else:
        parent = os.path.dirname(logfn)
        if len(parent) > 0:
            os.makedirs(parent, exist_ok=True)
    logging.basicConfig(
        filename=logfn,
        filemode='w+',
        format='%(asctime)s %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.DEBUG,
    )


def log_str(*ls):
    line = [str(i) for i in ls]
    line = ' '.join(line)
    logging.info(line)
    print(line)
    


def main(args):
    init_logging(args.logpath)
    
    log_str('read csv file', args.csvpath)
    df = pandas.read_csv(args.csvpath)
    print(df.head(5))
    
    all_cols = list(df)
    
    cols = args.cols.split(',')
    cols = [i for i in cols if len(i) > 0]
    log_str('numerical cols of csv data', cols)
    for c in cols:
        assert c in all_cols
    assert args.target in all_cols
    
    data = df.loc[:, cols].to_numpy()
    targets = df.loc[:, args.target].tolist()
    log_str('data shape', data.shape)
    log_str('targets', set(targets))
    
    parent_path = os.path.dirname(args.outpath)
    assert len(parent_path) > 0
    os.makedirs(parent_path, exist_ok=True)
    numpy.savez_compressed(args.outpath, data=data)
    
    parent_path = os.path.dirname(args.targetjson)
    assert len(parent_path) > 0
    os.makedirs(parent_path, exist_ok=True)
    with open(args.targetjson, 'w') as f:
        json.dump(targets, f)
    
    
if __name__ == '__main__':
    
    args = parser.parse_args()
    main(args)

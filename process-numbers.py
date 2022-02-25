import sys, os, os.path
import json
import numpy
import pandas
import logging
import argparse

import sklearn.manifold

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--datapath', type=str, default='generator/data.npz', help='data path')
parser.add_argument('--targetpath', type=str, default='generator/targets.json', help='target path')
parser.add_argument('--method', type=str, default='mds', help='mds, tsne, pca')
parser.add_argument('--outpath', type=str, default='data/2d.csv', help='output path')
parser.add_argument('--logpath', type=str, default='log-process-numbers.log', help='log filename')



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
    
    assert os.path.exists(args.datapath)
    assert os.path.exists(args.targetpath)
    
    log_str('read data file', args.datapath)
    data = numpy.load(args.datapath)
    assert 'data' in data
    matrix = data['data']
    log_str('data', matrix.shape)
    
    targets = []
    log_str('read target file', args.targetpath)
    with open(args.targetpath, 'r') as f:
        targets = json.load(f)
    
    assert matrix.shape[0] == len(targets)
    
    embedding = sklearn.manifold.MDS(n_components=2)
    x_2d = embedding.fit_transform(matrix)
    
    log_str('2d data shape', x_2d.shape)
    
    df = pandas.DataFrame(
        data=x_2d,
        index=list(range(x_2d.shape[0])),
        columns=['MDS1', 'MDS2']
    )
    df.loc[:, 'target'] = targets
    
    parent = os.path.dirname(args.outpath)
    if len(parent) > 0:
        os.makedirs(parent, exist_ok=True)
    df.to_csv(args.outpath, index=False)
    
    
    
if __name__ == '__main__':
    
    args = parser.parse_args()
    main(args)

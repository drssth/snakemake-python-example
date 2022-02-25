import sys, os, os.path
import json
import numpy
import pandas
import logging
import argparse

import plotly.express as px

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--datapath', type=str, default='data/2d.csv', help='2d data path')
parser.add_argument('--outpath', type=str, default='plot/dist.png', help='output path')
parser.add_argument('--logpath', type=str, default='log-plot2files.log', help='log filename')



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
    
    log_str('read data file', args.datapath)
    df = pandas.read_csv(args.datapath)
    cols = list(df)
    assert 'MDS1' in cols
    assert 'MDS2' in cols
    assert 'target' in cols

    log_str('generate plot', args.outpath)
    fig = px.scatter(
        df, 
        x="MDS1", y="MDS2", 
        color="target",
        symbol="target"
    )
    
    parent = os.path.dirname(args.outpath)
    if len(parent) > 0:
        os.makedirs(parent, exist_ok=True)
    fig.write_image(args.outpath)
    
    
    
if __name__ == '__main__':
    
    args = parser.parse_args()
    main(args)

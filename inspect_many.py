import configparser
import argparse
from multiprocessing import cpu_count
from pathlib import Path

import pandas as pd
import numpy as np

from utils.inspectors import run_inspectors

config = configparser.ConfigParser()
config.read('config.ini')

# rpc ips file path
rpc_ips_path = config['paths']["rpc_hosts_ip_path"]

# load data file paths
database_path = Path(config['paths']['database_path'])
addresses_data_path = database_path / config['paths']['addresses_data_path']
protocols_data_path = database_path / config['paths']['protocols_data_path']
token_ins_data_path = database_path / config['paths']['token_ins_data_path']
token_outs_data_path = database_path / config['paths']['token_outs_data_path']

# load log paths
logs_path = Path(config["logs"]["logs_path"])
inspectors_log_path = logs_path / config["logs"]["inspectors_log_path"]


def create_dirs(*dirs):
    for directory in dirs:
        directory.mkdir(parents=True, exist_ok=True)


def get_rpcs(file_path):
    return pd.read_csv(file_path, names=["ip"])


if __name__ == "__main__":
    create_dirs(database_path, addresses_data_path, protocols_data_path, token_ins_data_path, token_outs_data_path,
                logs_path, inspectors_log_path)

    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--after', type=int, help='Block number to start from')
    parser.add_argument('-b', '--before', type=int, help='Block number to end with')
    parser.add_argument('-p', '--para', type=int, help='Maximum number of parallel processes/inspectors', default=cpu_count())
    args = parser.parse_args()

    inspector_cnt = args.para
    block_intervals = np.linspace(start=args.after, stop=args.before, num=inspector_cnt + 1)
    rpc_urls = get_rpcs(rpc_ips_path)
    run_inspectors(block_intervals, rpc_urls, inspector_cnt)

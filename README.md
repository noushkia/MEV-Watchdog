# MEV-Watchdog

[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

Fast and light MEV inspector.
MEV-Watchdog is a powerful Ethereum MEV inspector.
It analyzes blocks to detect swaps,
arbitrages, and liquidations.
Using Postgres for data storage, it ensures efficient management.
Future goals include cross-chain transaction inspection, improved detection of complex MEVs, and real-time monitoring.
The aim is to empower users to proactively identify and respond to MEV opportunities before they're confirmed in blocks.

## Table of Contents

- [Install](#install)
- [Usage](#usage)
    - [RPC Finder](#rpc-finder)
    - [Inspector](#inspector)
- [Future Directions](#future-directions)

## Install

### Dependencies

#### PostgreSQL

To install PostgreSQL run the following command:

```bash
sudo apt-get install postgresql postgresql-contrib
```

#### pg_config

To install pg_config and Build psycopg2 from Source, run the following command:

```bash
sudo apt-get install libpq-dev
```

### Requirements

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the requirements.

```bash
pip3 install -r requirements.txt
```

### Configuration

#### PostgreSQL

To configure PostgreSQL run the following command:

```bash
sudo -u postgres psql
```

If it's your first time running the tool on a system, run the following commands in the PostgreSQL shell:

```bash
CREATE DATABASE mev_watchdog;

CREATE USER mev WITH PASSWORD 'watchdog';

GRANT ALL PRIVILEGES ON DATABASE mev_watchdog TO mev;
```

## Usage

### RPC Finder

The rpc_finder package is used to find RPC endpoints for Erigon Ethereum nodes.
It first fetches the list of synced Erigon nodes from Ethernodes.org and then checks if they are responding to JSON-RPC
requests.
The list of all running RPC endpoints is then stored in erigon_sorted_hosts.csv file.

In order to fetch all possible RPC endpoints, run the following command:

```bash
  python rpc_finder/get_rpcs.py
```

After fetching all possible endpoints, in order to fetch only the RPC endpoints that are responding to JSON-RPC
requests and are up-to-date, run the following command:

```bash
  python rpc_finder/rpc_vitals_check.py
```

### Inspector

The mev_inspect package is used to inspect a given range of Ethereum blocks for MEV transactions.
It first fetches the list of all running RPC endpoints from erigon_sorted_hosts.csv file.
Then it starts up a number of processes to inspect blocks in parallel.
Each process then runs several threads to fetch blocks from the RPC endpoints and inspect them for MEV transactions.
The results are then stored in the PostgreSQL database.

In order to inspect a given range of blocks, run the following command:

```bash
  python inspect_many.py -a START_BLOCK_RANGE -b END_BLOCK_RANGE
```

The inspector by default starts up as many processes as the number of available cpu cores.
You can specify the number of processes to start up by using the -p flag:

```bash
  python inspect_many.py -a START_BLOCK_RANGE -b END_BLOCK_RANGE -p NUMBER_OF_PROCESSES
```

The inspector creates a log file named inspector.log in the logs directory.

## Future Directions

- [ ] **Cross-chain transaction inspection**

  In addition to its existing capabilities, Watchdog has several future milestones on its roadmap. One of its key
  objectives is to expand its functionality to include the inspection of cross-chain transactions, enabling users to
  gain
  insights into MEV activities occurring across different blockchain networks.


- [ ] **Complex MEV detection**

  Watchdog aims to enhance its detection capabilities to uncover more complex and sophisticated MEVs. By
  continuously refining its algorithms and analysis techniques, it will be able to identify a wider range of MEV
  strategies and extract even more value from Ethereum transactions.


- [ ] **Real-time monitoring**

  To ensure real-time monitoring and timely intervention, Watchdog is actively working towards improving its speed and
  efficiency. It aims to be fast enough to detect MEV transactions in the mempool, providing users with the ability to
  proactively identify and respond to MEV opportunities before they are included in confirmed blocks.


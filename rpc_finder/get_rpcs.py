import json

import requests

import pandas as pd

# get 100 ips with each request
length = 100

client = "erigon"


def get_total_records():
    response = requests.get(f"https://ethernodes.org/data?draw=9&columns%d5B0%5D%5Bdata%5D=id&columns%5B0%5D%5Bname%5D"
                            f"=&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=true&columns%5B0%5D"
                            f"%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata"
                            f"%5D=host&columns%5B1%5D%5Bname%5D=&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D"
                            f"%5Borderable%5D=true&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D"
                            f"%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=isp&columns%5B2%5D%5Bname%5D=&columns%5B2%5D"
                            f"%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=true&columns%5B2%5D%5Bsearch%5D"
                            f"%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=country"
                            f"&columns%5B3%5D%5Bname%5D=&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable"
                            f"%5D=true&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D"
                            f"=false&columns%5B4%5D%5Bdata%5D=client&columns%5B4%5D%5Bname%5D=&columns%5B4%5D"
                            f"%5Bsearchable%5D=true&columns%5B4%5D%5Borderable%5D=true&columns%5B4%5D%5Bsearch%5D"
                            f"%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B5%5D%5Bdata%5D"
                            f"=clientVersion&columns%5B5%5D%5Bname%5D=&columns%5B5%5D%5Bsearchable%5D=true&columns%5B5"
                            f"%5D%5Borderable%5D=true&columns%5B5%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B5%5D%5Bsearch%5D"
                            f"%5Bregex%5D=false&columns%5B6%5D%5Bdata%5D=os&columns%5B6%5D%5Bname%5D=&columns%5B6%5D"
                            f"%5Bsearchable%5D=true&columns%5B6%5D%5Borderable%5D=true&columns%5B6%5D%5Bsearch%5D"
                            f"%5Bvalue%5D=&columns%5B6%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B7%5D%5Bdata%5D"
                            f"=lastUpdate&columns%5B7%5D%5Bname%5D=&columns%5B7%5D%5Bsearchable%5D=true&columns%5B7%5D"
                            f"%5Borderable%5D=true&columns%5B7%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B7%5D%5Bsearch%5D"
                            f"%5Bregex%5D=false&columns%5B8%5D%5Bdata%5D=inSync&columns%5B8%5D%5Bname%5D=&columns%5B8%5D"
                            f"%5Bsearchable%5D=true&columns%5B8%5D%5Borderable%5D=true&columns%5B8%5D%5Bsearch%5D"
                            f"%5Bvalue%5D=&columns%5B8%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=8&order"
                            f"%5B0%5D%5Bdir%5D=desc&start=0&length={length}&search%5Bvalue%5D={client}"
                            f"&search%5Bregex%5D=false&_=1661254019057")
    return json.loads(response.text)['recordsTotal']


if __name__ == "__main__":
    hosts = pd.DataFrame(
        columns=["id", "host", "port", "client", "clientVersion", "os", "lastUpdate", "country", "inSync", "isp"])
    total_records = get_total_records()
    for idx in range(0, total_records, length):
        print(f"Fetching hosts {idx} to {idx + length}")
        r = requests.get(f"https://ethernodes.org/data?draw=9&columns%d5B0%5D%5Bdata%5D=id&columns%5B0%5D%5Bname%5D"
                         f"=&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=true&columns%5B0%5D"
                         f"%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata"
                         f"%5D=host&columns%5B1%5D%5Bname%5D=&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D"
                         f"%5Borderable%5D=true&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D"
                         f"%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=isp&columns%5B2%5D%5Bname%5D=&columns%5B2%5D"
                         f"%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=true&columns%5B2%5D%5Bsearch%5D"
                         f"%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=country"
                         f"&columns%5B3%5D%5Bname%5D=&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable"
                         f"%5D=true&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D"
                         f"=false&columns%5B4%5D%5Bdata%5D=client&columns%5B4%5D%5Bname%5D=&columns%5B4%5D"
                         f"%5Bsearchable%5D=true&columns%5B4%5D%5Borderable%5D=true&columns%5B4%5D%5Bsearch%5D"
                         f"%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B5%5D%5Bdata%5D"
                         f"=clientVersion&columns%5B5%5D%5Bname%5D=&columns%5B5%5D%5Bsearchable%5D=true&columns%5B5"
                         f"%5D%5Borderable%5D=true&columns%5B5%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B5%5D%5Bsearch%5D"
                         f"%5Bregex%5D=false&columns%5B6%5D%5Bdata%5D=os&columns%5B6%5D%5Bname%5D=&columns%5B6%5D"
                         f"%5Bsearchable%5D=true&columns%5B6%5D%5Borderable%5D=true&columns%5B6%5D%5Bsearch%5D"
                         f"%5Bvalue%5D=&columns%5B6%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B7%5D%5Bdata%5D"
                         f"=lastUpdate&columns%5B7%5D%5Bname%5D=&columns%5B7%5D%5Bsearchable%5D=true&columns%5B7%5D"
                         f"%5Borderable%5D=true&columns%5B7%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B7%5D%5Bsearch%5D"
                         f"%5Bregex%5D=false&columns%5B8%5D%5Bdata%5D=inSync&columns%5B8%5D%5Bname%5D=&columns%5B8%5D"
                         f"%5Bsearchable%5D=true&columns%5B8%5D%5Borderable%5D=true&columns%5B8%5D%5Bsearch%5D"
                         f"%5Bvalue%5D=&columns%5B8%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=8&order"
                         f"%5B0%5D%5Bdir%5D=desc&start={idx}&length={length}&search%5Bvalue%5D={client}"
                         f"&search%5Bregex%5D=false&_=1661254019057")

        rows = pd.DataFrame(json.loads(r.text)['data'])
        hosts = hosts._append(rows, ignore_index=True)

    hosts.drop(hosts[hosts['inSync'] == 0].index, inplace=True)

    with open(f"{client}_hosts.csv", "w", encoding="utf-8") as f:
        hosts["host"].to_csv(f, index=False, header=False)

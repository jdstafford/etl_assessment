#!/usr/bin/python

from dict2xml import dict2xml
import pandas as pd
import sys
import yaml

df = pd.read_csv("data.csv", header=0)
host_data = df.loc[:, df.columns != "Date / Time"]
host_aggregates = host_data.aggregate(["min", "max", "mean"]).assign(
    GLOBAL=[host_data.min().min(), host_data.max().max(), host_data.mean().mean()]
)

for host in host_aggregates:
    # formatted hostname
    colname = host if host == "GLOBAL" else host.split("#")[1]
    host_aggregates.rename(columns={host: colname}, inplace=True)

    # generate STDOUT
    print(f"{colname} MINIMUM: {host_aggregates[colname]['min']}")
    print(f"{colname} MAXIMUM: {host_aggregates[colname]['max']}")
    print(f"{colname} AVERAGE: {host_aggregates[colname]['mean']}")
    print("")

if "json" or "all" in sys.argv:
    host_aggregates.to_json("host_aggregates.json")

if "xml" or "all" in sys.argv:
    with open("host_aggregates.xml", "w") as xml_file:
        xml_file.write(dict2xml(host_aggregates.to_dict()))
        xml_file.close

if "yaml" or "all" in sys.argv:
    with open(r"host_aggregates.yaml", "w") as yaml_file:
        yaml.dump(
            host_aggregates.to_dict(),
            yaml_file,
            sort_keys=False,
            width=72,
            indent=4,
            default_flow_style=None,
        )

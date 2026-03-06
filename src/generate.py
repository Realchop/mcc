from common import *
import argparse
from loguru import logger
from pathlib import Path
import sys
import pandas as pd


logger.remove()

logger.add(sys.stderr, format="[{level}] {message}")

parser = argparse.ArgumentParser(description="Generate a random graph with uniform edge distribution.")

parser.add_argument("N", type=int, help="number of nodes")
parser.add_argument("P", type=float, help="probability of an edge")

parser.add_argument("--path", "-p", action="store", help="directory to store output in (created if it doesn't exist)")
parser.add_argument("--file", "-f", action="store", help="what to name output file (default is \"output\")")
parser.add_argument("--mode", "-m", action="store_true", help="P is the number of branches instead")
parser.add_argument("--verbose", "-v", action="store_true")

args = parser.parse_args()

node_count = args.N
if node_count <= 0:
    logger.error("N must be positive")
    exit(1)

edge_probability = args.P
if not args.mode and (edge_probability < 0 or edge_probability > 1):
    logger.error("P must be in [0, 1]")
    exit(1)

path = Path(".") 
if args.path:
    path = Path(args.path) 
    path.mkdir(parents=True, exist_ok=True)

filename = "output"
if args.file:
    filename = args.file
path = path / f"{filename}.parquet"

if args.verbose:
    logger.info(f"Generating a graph with {node_count} nodes and {'edge probability' if not args.mode else ''} {edge_probability} {'edges' if args.mode else ''}")

G: nx.Graph
if not args.mode:
    G = nx.fast_gnp_random_graph(node_count, edge_probability)
else:
    G = nx.gnm_random_graph(node_count, edge_probability)

if args.verbose:
    logger.info(f"Saving to {path}")

df: pd.DataFrame = nx.to_pandas_edgelist(G)

df.to_parquet(path, engine="pyarrow", compression="snappy")


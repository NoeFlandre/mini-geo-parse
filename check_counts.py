
from src.evaluator import parse_benchmark

toponyms = parse_benchmark("data/benchmark/gwn_full.txt")
unique_mentions = list({t['mention']: t for t in toponyms}.values())

print(f"Total toponyms: {len(toponyms)}")
print(f"Unique mentions: {len(unique_mentions)}")

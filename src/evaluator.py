"""

Evaluator Module
Compute the Accuracy@161km on the GeoWebNews benchmark

"""

import math 
from pathlib import Path

def haversine_distance(lat1 : float, lon1 : float, lat2 : float, lon2 : float) -> float:

    """
    Compute the great-circle distance between two points on Earth in km. It uses the Haversine formula.

    """

    R = 6371 # Earth radius in km

    # Convert to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    c = 2*math.asin(math.sqrt(a))

    return R*c


def parse_benchmark(filepath : str) -> list[dict]:
    """
    Parse the GeoWebNews benchmark file

    Output : Give back a dictionary which for each toponym specifies the mention, latitude and lontitude

    """

    toponyms = []

    with open(filepath, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f):
            line = line.strip()
            if not line :
                continue

            # we split by '||' to get the individual toponyms
            entries = line.split('||')

            for entry in entries :
                if not entry.strip() :
                    continue

                parts = entry.split(',,') # we split by ',,' to get the individual fields

                if len(parts) >= 4:
                    try:
                        toponyms.append({
                            'doc_id' : line_num,
                            'canonical' : parts[0].strip(),
                            'mention' : parts[1].strip(),
                            'lat' : float(parts[2]),
                            'lon' : float(parts[3]),
                        })
                    
                    except (ValueError, IndexError):
                        continue # we are skipping malformed entries

    return toponyms

def evaluate_accuracy_at_161km(
    predictions : list[dict],
    ground_truth : list[dict],
    num_samples : int = None,
) -> dict :

    """

    Compute Accuracy@161km (100 mile) metric.

    A prediction is considered to be correct if the predicted coordinates are within 161km of the ground truth.

    Args :

        predictions : List of {'mention' : str, 'lat' : float, 'lon' : float}
        ground_truth : List from parse_benchmark
        num_samples : The number of samples we asses on

    Output :

        Dict with accuracy score and details

    """

    correct, total = 0, 0
    errors = []

    # Build a lookup from mention to ground truth
    gt_lookup = {item['mention'].lower() : item for item in ground_truth}

    for pred in predictions :
        mention = pred['mention'].lower()

        if mention not in gt_lookup:
            continue # we skip if there is no ground truth

        gt = gt_lookup[mention]
        total+=1

        distance = haversine_distance(pred['lat'], pred['lon'], gt['lat'], gt['lon'])

        if distance <=161:
            correct+=1
        
        else:
            errors.append({
                'mention' : pred['mention'],
                'predicted' : [pred['lat'], pred['lon']],
                'actual' : [gt['lat'], gt['lon']],
                'distance_km' : round(distance, 2),
            })

    total = total if total>0 else 0.0
    denominator = num_samples if num_samples else total
    accuracy = correct / denominator

    return {
        "accuracy_at_161km" : round(accuracy*100, 2),
        "correct" : correct,
        "total" : total,
        "errors" : errors[:5]
    }


if __name__ == "__main__":

    benchmark_path = "data/benchmark/gwn_full.txt"

    toponyms = parse_benchmark(filepath=benchmark_path)

    print(f"Loaded {len(toponyms)} toponyms from {len(set(t['doc_id'] for t in toponyms))} documents") 
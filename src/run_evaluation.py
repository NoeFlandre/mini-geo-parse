"""

Run evaluation on a sample of the GeoWebNews benchmark

"""

from evaluator import parse_benchmark, evaluate_accuracy_at_161km
from pipeline import geoparse


def run_evaluation(sample_size : int = None):
    """
    Run MiniGeoParse on a sample from GeoWebNews and compute accuracy

    """

    ground_truth = parse_benchmark("data/benchmark/gwn_full.txt")

    unique_mentions = list({t['mention']: t for t in ground_truth}.values())
    samples = unique_mentions[:sample_size] if sample_size else unique_mentions

    print(f"Benchmarking on {len(samples)} unique toponyms")

    predictions = []

    for item in samples:

        mention = item['mention']
        test_text = f"The even occured in {mention}"
        print(f"Testing {mention}")

        try :
            results = geoparse(test_text)

            if results:
                pred = results[0]
                predictions.append({
                    'mention': mention,
                    'lat': pred['coordinates'][0],
                    'lon': pred['coordinates'][1],
                })
                print(f"Predicted latitude : {pred['coordinates'][0]} and longitude : {pred['coordinates'][1]}")
            
            else :
                print("No results")

        except Exception as e:
            print(f"Error {e}")

    results = evaluate_accuracy_at_161km(predictions=predictions, ground_truth=ground_truth, num_samples=len(samples))

    return results


if __name__ == "__main__":
    results = run_evaluation()
    print(results)
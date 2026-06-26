import json
import argparse
from dataclasses import dataclass

@dataclass
class InferenceRequest:
    data: str

def run_inference(payload_file):
    try:
        with open(payload_file, 'r') as f:
            payload = json.load(f)
        inference_request = InferenceRequest(data=payload['data'])
        # Simulate inference logic
        result = f"Inferred result: {inference_request.data}"
        return result
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('payload_file', help='Path to JSON payload file')
    args = parser.parse_args()
    result = run_inference(args.payload_file)
    if result:
        print(result)
        return 0
    else:
        return 1

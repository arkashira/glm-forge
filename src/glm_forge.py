import argparse
import json
from dataclasses import dataclass
from typing import List

@dataclass
class Request:
    timestamp: float
    latency: float

class GLMForge:
    def __init__(self, baseline_cpu_usage: float, baseline_gpu_usage: float):
        self.baseline_cpu_usage = baseline_cpu_usage
        self.baseline_gpu_usage = baseline_gpu_usage
        self.inference_workers = 1
        self.requests = []

    def add_request(self, request: Request):
        self.requests.append(request)
        self.auto_scale()

    def auto_scale(self):
        if len(self.requests) > 50:
            self.inference_workers = 2
        else:
            self.inference_workers = 1

    def get_latency(self) -> float:
        if len(self.requests) == 0:
            return 0
        return sum(r.latency for r in self.requests) / len(self.requests)

    def get_cpu_usage(self) -> float:
        return self.baseline_cpu_usage * self.inference_workers

    def get_gpu_usage(self) -> float:
        return self.baseline_gpu_usage * self.inference_workers

    def main(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--baseline-cpu-usage', type=float, default=0.5)
        parser.add_argument('--baseline-gpu-usage', type=float, default=0.5)
        args = parser.parse_args()
        glm_forge = GLMForge(args.baseline_cpu_usage, args.baseline_gpu_usage)
        # Simulate requests
        for i in range(100):
            request = Request(i, 100)
            glm_forge.add_request(request)
        print(f'Latency: {glm_forge.get_latency()} ms')
        print(f'CPU usage: {glm_forge.get_cpu_usage()}')
        print(f'GPU usage: {glm_forge.get_gpu_usage()}')

if __name__ == '__main__':
    glm_forge = GLMForge(0.5, 0.5)
    glm_forge.main()

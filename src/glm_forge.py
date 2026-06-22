import csv
import json
from dataclasses import dataclass
from datetime import datetime
from os import makedirs
from os.path import exists, join
from typing import List

@dataclass
class TrainingLog:
    epoch: int
    loss: float
    gpu_usage: float
    cost: float

class GLMForge:
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.report_dir = join('/tmp', project_id)
        if not exists(self.report_dir):
            makedirs(self.report_dir)

    def generate_report(self, training_logs: List[TrainingLog]) -> str:
        report_path = join(self.report_dir, f'report_{datetime.now().strftime("%Y%m%d%H%M%S")}.csv')
        with open(report_path, 'w', newline='') as csvfile:
            fieldnames = ['epoch', 'loss', 'gpu_usage', 'cost']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for log in training_logs:
                writer.writerow(log.__dict__)
        return report_path

    def get_download_link(self, report_path: str) -> str:
        return f'/download/{self.project_id}/{report_path.split("/")[-1]}'

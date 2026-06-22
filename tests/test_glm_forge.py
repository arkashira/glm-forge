import pytest
from glm_forge import GLMForge, TrainingLog
import os
import tempfile
import csv

@pytest.fixture
def glm_forge():
    with tempfile.TemporaryDirectory() as tmpdir:
        os.environ['TMPDIR'] = tmpdir
        yield GLMForge('test_project')

def test_generate_report(glm_forge):
    training_logs = [TrainingLog(1, 0.1, 0.5, 10.0), TrainingLog(2, 0.2, 0.6, 20.0)]
    report_path = glm_forge.generate_report(training_logs)
    assert os.path.exists(report_path)
    with open(report_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)
    assert len(rows) == 2
    assert rows[0]['epoch'] == '1'
    assert rows[0]['loss'] == '0.1'
    assert rows[0]['gpu_usage'] == '0.5'
    assert rows[0]['cost'] == '10.0'

def test_get_download_link(glm_forge):
    report_path = 'report_20230220123000.csv'
    download_link = glm_forge.get_download_link(report_path)
    assert download_link == '/download/test_project/report_20230220123000.csv'

def test_generate_report_empty(glm_forge):
    training_logs = []
    report_path = glm_forge.generate_report(training_logs)
    assert os.path.exists(report_path)
    with open(report_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)
    assert len(rows) == 0

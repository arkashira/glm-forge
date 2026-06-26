import json
import tempfile
import os
from glm_forge import run_inference
import pytest

def test_run_inference_success():
    with tempfile.NamedTemporaryFile(mode='w') as tmp:
        json.dump({'data': 'test_data'}, tmp)
        tmp.flush()
        result = run_inference(tmp.name)
        assert result == "Inferred result: test_data"

def test_run_inference_failure():
    with tempfile.NamedTemporaryFile(mode='w') as tmp:
        json.dump({'invalid': 'test_data'}, tmp)
        tmp.flush()
        result = run_inference(tmp.name)
        assert result is None

def test_run_inference_invalid_file():
    result = run_inference('non_existent_file.json')
    assert result is None

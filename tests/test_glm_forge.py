import pytest
from glm_forge import GLMForge, Request

def test_auto_scale():
    glm_forge = GLMForge(0.5, 0.5)
    for i in range(51):
        glm_forge.add_request(Request(i, 100))
    assert glm_forge.inference_workers == 2

def test_latency():
    glm_forge = GLMForge(0.5, 0.5)
    for i in range(100):
        glm_forge.add_request(Request(i, 100))
    assert glm_forge.get_latency() == 100

def test_cpu_usage():
    glm_forge = GLMForge(0.5, 0.5)
    for i in range(100):
        glm_forge.add_request(Request(i, 100))
    assert glm_forge.get_cpu_usage() == 1.0

def test_gpu_usage():
    glm_forge = GLMForge(0.5, 0.5)
    for i in range(100):
        glm_forge.add_request(Request(i, 100))
    assert glm_forge.get_gpu_usage() == 1.0

def test_edge_case_zero_requests():
    glm_forge = GLMForge(0.5, 0.5)
    assert glm_forge.get_latency() == 0
    assert glm_forge.get_cpu_usage() == 0.5
    assert glm_forge.get_gpu_usage() == 0.5

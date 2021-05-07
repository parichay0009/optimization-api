import pytest
import json

def test_navie(test_client):
    navie_url = "/optimize/naive?lists={0}&m={1}&f={2}".format("[[5,204],[7,208,209],[5,207,208,209,2010]]","40","f")
    res = test_client.get(
        navie_url
    )
    navie_json = json.loads(res.data.decode('utf-8'))
    assert navie_json["Maximum"] == 37

    navie_url = "/optimize/naive"
    res = test_client.get(
        navie_url
    )
    assert res.status_code == 404

    navie_url = "/optimize/naive?lists={0}&m={1}&f={2}".format("50","40","f")
    res = test_client.get(
        navie_url
    )
    assert res.status_code == 400


def test_efficient(test_client):
    efficient_url = "/optimize/efficient?lists={0}&m={1}&f={2}".format("[[5,204],[7,208,209],[5,207,208,209,2010]]","40","f")
    res = test_client.get(
        efficient_url
    )
    efficient_json = json.loads(res.data.decode('utf-8'))
    assert efficient_json["Maximum"] == 37

    efficient_url = "/optimize/efficient"
    res = test_client.get(
        efficient_url
    )
    assert res.status_code == 404

    efficient_url = "/optimize/efficient?lists={0}&m={1}&f={2}".format("50","40","f")
    res = test_client.get(
        efficient_url
    )
    assert res.status_code == 400


def test_benchmark_naive(test_client):
    naive_url = "/benchmark/naive?num_lists={0}&num_elements={1}&replications={2}".format("5","4","5")
    res = test_client.get(
        naive_url
    )
    assert res.status_code == 200

    naive_url = "/benchmark/naive"
    res = test_client.get(
        naive_url
    )
    assert res.status_code == 404

    naive_url = "/benchmark/naive?num_lists={0}&num_elements={1}&replications={2}".format("50","40","f")
    res = test_client.get(
        naive_url
    )
    assert res.status_code == 400

def test_benchmark_efficient(test_client):
    efficient_url = "/benchmark/efficient?num_lists={0}&num_elements={1}&replications={2}".format("5","4","5")
    res = test_client.get(
        efficient_url
    )
    assert res.status_code == 200

    efficient_url = "/benchmark/efficient"
    res = test_client.get(
        efficient_url
    )
    assert res.status_code == 404

    efficient_url = "/benchmark/efficient?num_lists={0}&num_elements={1}&replications={2}".format("50","40","f")
    res = test_client.get(
        efficient_url
    )
    assert res.status_code == 400

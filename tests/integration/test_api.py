import json
import pytest
from app.main import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config.update(TESTING=True)
    return app.test_client()

@pytest.mark.smoke
@pytest.mark.integration
def test_health(client):
    res = client.get('/health')
    assert res.status_code == 200
    assert res.get_json()['status'] == 'ok'

@pytest.mark.integration
def test_sum_endpoint(client):
    res = client.post('/sum', data=json.dumps({'numbers': [1, 2, 3]}),
                      content_type='application/json')
    assert res.status_code == 200
    assert res.get_json()['result'] == 6.0

@pytest.mark.integration
def test_divide_endpoint_ok(client):
    res = client.get('/divide?a=9&b=3')
    assert res.status_code == 200
    assert res.get_json()['result'] == 3.0

@pytest.mark.integration
def test_divide_endpoint_div_zero(client):
    res = client.get('/divide?a=1&b=0')
    assert res.status_code == 400
    assert 'division by zero' in res.get_json()['error']

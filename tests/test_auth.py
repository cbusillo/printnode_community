import json

import pytest
import requests

from printnode_community.auth import (
    Auth,
    ClientError,
    ConnectionError,
    RequestError,
    ServerError,
    TimeoutError,
    TooManyRequests,
)
from printnode_community.gateway import Gateway, Unauthorized

API_ADDRESS = 'https://api.printnode.com'
API_KEY = 'test-api-key'


class FakeResponse:
    def __init__(self, status_code, payload, content_type='application/json'):
        self.status_code = status_code
        self._payload = payload
        self.content = json.dumps(payload).encode('utf-8')
        self.headers = {'content-type': content_type}

    def json(self):
        return self._payload


def test_gateway(monkeypatch):
    def fake_get(url, auth, headers, **kwargs):
        assert url == API_ADDRESS + '/whoami'
        assert auth == (API_KEY, '')
        assert headers == {}
        assert kwargs == {}
        return FakeResponse(200, {
            'id': 123,
            'firstname': 'Ada',
            'lastname': 'Lovelace',
            'email': 'ada@example.com',
            'canCreateSubAccounts': False,
            'creatorEmail': None,
            'creatorRef': None,
            'childAccounts': [],
            'credits': 0,
            'numComputers': 0,
            'totalPrints': 0,
            'versions': [],
            'connected': False,
            'tags': {},
            'state': 'active',
        })

    monkeypatch.setattr('printnode_community.auth.requests.get', fake_get)

    gateway = Gateway(url=API_ADDRESS, apikey=API_KEY)
    assert gateway.account.firstname == 'Ada'


def test_gateway_handles_unauthentication(monkeypatch):
    def fake_get(url, auth, headers, **kwargs):
        return FakeResponse(401, {
            'code': 'BadRequest',
            'message': 'API Key not found',
        })

    monkeypatch.setattr('printnode_community.auth.requests.get', fake_get)

    gateway = Gateway(
        url=API_ADDRESS,
        email='fake@omlet.co.uk',
        password='helloworld')
    with pytest.raises(Unauthorized):
        gateway.account


@pytest.mark.parametrize('child_id', [123, '123'])
def test_gateway_child_id_prepares_valid_http_header(monkeypatch, child_id):
    def fake_get(url, auth, headers, **kwargs):
        prepared = requests.Request('GET', url, auth=auth, headers=headers).prepare()
        assert prepared.headers['X-Child-Account-By-Id'] == '123'
        response = requests.Response()
        response.status_code = 200
        response.headers['Content-Type'] = 'application/json'
        response._content = b'{"id": 123}'
        return response

    monkeypatch.setattr('printnode_community.auth.requests.get', fake_get)
    assert Gateway(apikey=API_KEY, child_id=child_id).account.id == 123


@pytest.mark.parametrize('status_code', [200, 204])
@pytest.mark.parametrize('content_type', [None, 'application/json'])
def test_gateway_delete_account_accepts_empty_success(
        monkeypatch, status_code, content_type):
    calls = []

    def fake_delete(url, auth, headers, **kwargs):
        prepared = requests.Request('DELETE', url, auth=auth, headers=headers).prepare()
        calls.append(prepared)
        response = requests.Response()
        response.status_code = status_code
        response._content = b''
        if content_type is not None:
            response.headers['Content-Type'] = content_type
        return response

    monkeypatch.setattr('printnode_community.auth.requests.delete', fake_delete)
    assert Gateway(apikey=API_KEY, child_id='123').DeleteAccount() is None
    assert len(calls) == 1
    assert calls[0].url == API_ADDRESS + '/account'


@pytest.mark.parametrize('status_code,body,content_type,error', [
    (200, b'not json', 'application/json', requests.exceptions.JSONDecodeError),
    (204, b'not json', 'application/json', requests.exceptions.JSONDecodeError),
    (200, b'{"deleted": true}', 'text/html', ValueError),
    (401, b'', 'application/json', Exception),
    (401, b'{"code":"Denied","message":"Not authorized"}', 'application/json', Unauthorized),
])
def test_gateway_delete_account_preserves_response_validation(
        monkeypatch, status_code, body, content_type, error):
    response = requests.Response()
    response.status_code = status_code
    response.headers['Content-Type'] = content_type
    response._content = body
    monkeypatch.setattr('printnode_community.auth.requests.delete', lambda **kwargs: response)

    with pytest.raises(error):
        Gateway(apikey=API_KEY, child_id='123').DeleteAccount()


@pytest.mark.parametrize('kwargs,expected_auth,expected_headers', [
    ({'apikey': 'api-key'}, ('api-key', ''), {}),
    (
        {'email': 'ada@example.com', 'password': 'secret'},
        ('ada@example.com', 'secret'),
        {'X-Auth-With-Account-Credentials': 'API'},
    ),
    (
        {'clientkey': 'client-key'},
        ('client-key', ''),
        {'X-Auth-With-Client-Key': 'API'},
    ),
    (
        {'apikey': 'api-key', 'child_email': 'child@example.com'},
        ('api-key', ''),
        {'X-Child-Account-By-Email': 'child@example.com'},
    ),
    (
        {'apikey': 'api-key', 'child_ref': 'child-ref'},
        ('api-key', ''),
        {'X-Child-Account-By-CreatorRef': 'child-ref'},
    ),
    (
        {'apikey': 'api-key', 'child_id': 123},
        ('api-key', ''),
        {'X-Child-Account-By-Id': '123'},
    ),
])
def test_auth_modes_send_expected_auth_and_headers(
        monkeypatch, kwargs, expected_auth, expected_headers):
    calls = []

    def fake_get(url, auth, headers, **other_args):
        calls.append({
            'url': url,
            'auth': auth,
            'headers': headers,
            'other_args': other_args,
        })
        return FakeResponse(200, {'ok': True})

    monkeypatch.setattr('printnode_community.auth.requests.get', fake_get)

    result = Auth(url=API_ADDRESS, **kwargs).get('whoami')

    assert result == {'ok': True}
    assert calls == [{
        'url': API_ADDRESS + '/whoami',
        'auth': expected_auth,
        'headers': expected_headers,
        'other_args': {},
    }]


def test_post_serializes_fields_without_mutating_headers(monkeypatch):
    calls = []

    def fake_post(url, auth, headers, **other_args):
        calls.append({
            'url': url,
            'auth': auth,
            'headers': headers,
            'other_args': other_args,
        })
        return FakeResponse(200, {'created': True})

    monkeypatch.setattr('printnode_community.auth.requests.post', fake_post)
    headers = {'X-Custom': 'value'}
    fields = {'title': 'Example', 'qty': 2}

    result = Auth(url=API_ADDRESS, apikey=API_KEY).post(
        '/printjobs',
        fields=fields,
        request_headers=headers)

    assert result == {'created': True}
    assert headers == {'X-Custom': 'value'}
    assert calls[0]['headers'] == {'X-Custom': 'value'}
    assert json.loads(calls[0]['other_args']['data']) == fields


def test_post_with_no_fields_omits_request_body(monkeypatch):
    calls = []

    def fake_post(url, auth, headers, **other_args):
        calls.append(other_args)
        return FakeResponse(200, {'created': True})

    monkeypatch.setattr('printnode_community.auth.requests.post', fake_post)

    Auth(url=API_ADDRESS, apikey=API_KEY).post('printjobs')

    assert calls == [{}]


def test_patch_adds_json_content_type_without_mutating_headers(monkeypatch):
    calls = []

    def fake_patch(url, auth, headers, **other_args):
        calls.append({'headers': headers, 'other_args': other_args})
        return FakeResponse(200, {'updated': True})

    monkeypatch.setattr('printnode_community.auth.requests.patch', fake_patch)
    headers = {'X-Custom': 'value'}

    result = Auth(url=API_ADDRESS, clientkey='client-key').patch(
        'account',
        fields={'firstname': 'Ada'},
        request_headers=headers)

    assert result == {'updated': True}
    assert headers == {'X-Custom': 'value'}
    assert calls[0]['headers'] == {
        'X-Custom': 'value',
        'X-Auth-With-Client-Key': 'API',
        'Content-Type': 'application/json',
    }


def test_sslcert_is_used_as_verify_path(monkeypatch, tmp_path):
    cert_path = tmp_path / 'cert.pem'
    cert_path.write_text('certificate')
    calls = []

    def fake_delete(url, auth, headers, **other_args):
        calls.append(other_args)
        return FakeResponse(200, {'deleted': True})

    monkeypatch.setattr('printnode_community.auth.requests.delete', fake_delete)

    Auth(url=API_ADDRESS, apikey=API_KEY, sslcert=str(cert_path)).delete(
        'printjobs/123')

    assert calls == [{'verify': str(cert_path)}]


def test_missing_sslcert_raises_file_not_found():
    with pytest.raises(FileNotFoundError):
        Auth(url=API_ADDRESS, apikey=API_KEY, sslcert='/no/such/cert.pem')


@pytest.mark.parametrize('status_code,error_type', [
    (401, Unauthorized),
    (429, TooManyRequests),
    (404, ClientError),
    (500, ServerError),
])
def test_request_maps_api_error_status_codes(
        monkeypatch, status_code, error_type):
    def fake_get(url, auth, headers, **other_args):
        return FakeResponse(status_code, {
            'code': 'ExampleError',
            'message': 'Something went wrong',
            'uid': 'error-uid',
        })

    monkeypatch.setattr('printnode_community.auth.requests.get', fake_get)

    with pytest.raises(error_type) as error:
        Auth(url=API_ADDRESS, apikey=API_KEY).get('whoami')

    assert error.value.status_code == status_code
    assert error.value.code == 'ExampleError'
    assert error.value.message == 'Something went wrong'
    assert error.value.uid == 'error-uid'


def test_request_rejects_non_json_response(monkeypatch):
    def fake_get(url, auth, headers, **other_args):
        return FakeResponse(200, 'not json', content_type='text/html')

    monkeypatch.setattr('printnode_community.auth.requests.get', fake_get)

    with pytest.raises(ValueError, match='Incorrect Content-Type'):
        Auth(url=API_ADDRESS, apikey=API_KEY).get('whoami')


def test_request_accepts_json_content_type_with_charset(monkeypatch):
    def fake_get(url, auth, headers, **other_args):
        return FakeResponse(
            200,
            {'ok': True},
            content_type='application/json; charset=utf-8')

    monkeypatch.setattr('printnode_community.auth.requests.get', fake_get)

    assert Auth(url=API_ADDRESS, apikey=API_KEY).get('whoami') == {'ok': True}


def test_request_raises_for_unexpected_status_code(monkeypatch):
    def fake_get(url, auth, headers, **other_args):
        return FakeResponse(302, {'redirect': True})

    monkeypatch.setattr('printnode_community.auth.requests.get', fake_get)

    with pytest.raises(Exception, match='status code: 302'):
        Auth(url=API_ADDRESS, apikey=API_KEY).get('whoami')


@pytest.mark.parametrize('request_error,expected_error', [
    (requests.Timeout('slow'), TimeoutError),
    (requests.ReadTimeout('read timeout'), TimeoutError),
    (requests.ConnectionError('offline'), ConnectionError),
    (requests.RequestException('broken'), RequestError),
])
def test_request_rewrites_requests_exceptions(
        monkeypatch, request_error, expected_error):
    def fake_get(url, auth, headers, **other_args):
        raise request_error

    monkeypatch.setattr('printnode_community.auth.requests.get', fake_get)

    with pytest.raises(expected_error) as error:
        Auth(url=API_ADDRESS, apikey=API_KEY).get('whoami')

    assert str(error.value) == str(request_error)

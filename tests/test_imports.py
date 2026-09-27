import printnode_community
from printnode_community import auth, gateway


def test_gateway_imports_from_single_namespace():
    assert printnode_community.Gateway is gateway.Gateway


def test_top_level_errors_are_the_ones_auth_raises():
    # Callers write `except printnode_community.Unauthorized`; that only works
    # if the package exports the same classes the request layer raises.
    for name in (
            'ApiError', 'ClientError', 'Unauthorized', 'TooManyRequests',
            'ServerError', 'NetworkError', 'TimeoutError',
            'TooManyRedirectsError', 'ConnectionError', 'HttpError',
            'RequestError'):
        assert getattr(printnode_community, name) is getattr(auth, name)

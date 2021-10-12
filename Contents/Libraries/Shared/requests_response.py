from requests.models import Response
from requests.cookies import cookiejar_from_dict


def FakeResponse(req, url, status_code, content, headers={}, cookies={}):
    response = req
    if response is None:
        response = Response()

    response.url = url
    response.status_code = status_code
    response._content = content.encode('UTF-8') if content else ''
    response.headers = headers
    response.cookies = cookiejar_from_dict(cookies)

    return response

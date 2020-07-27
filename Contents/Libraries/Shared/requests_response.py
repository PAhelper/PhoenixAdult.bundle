from requests.models import Response

def FakeResponse(req, url, status_code, content):
    response = req
    response.url = url
    response.status_code = status_code
    response._content = content.encode('UTF-8')

    return response

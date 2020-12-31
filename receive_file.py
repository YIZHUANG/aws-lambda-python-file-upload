

import base64
from requests_toolbelt.multipart import decoder


def _extract_file(headers, body):
    multipart_string = base64.b64decode(body)
    content_type = headers['content-type']

    multipart_data = decoder.MultipartDecoder(
        multipart_string, content_type)

    filename = None
    part = multipart_data.parts[0]
    content = part.content
    disposition = part.headers[b'Content-Disposition']
    for content_info in str(disposition).split(';'):
        info = content_info.split('=', 2)
        if info[0].strip() == 'filename':
            filename = info[1].strip('\"\'\t \r\n')
    assert filename is not None
    file = {'file': (filename, content)}
    return file


def receive_file(event, context):
    headers = {k.lower(): v for k, v in event['headers'].items()}
    body = event['body']
    file = _extract_file(headers, body)
    print(file)
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
        }
    }

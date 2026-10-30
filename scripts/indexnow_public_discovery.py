#!/usr/bin/env python3
"""Notify IndexNow of ALAYA-999 public pages only.

Exits without any submission unless the key and target pages are live.
HTTP 200/202 means receipt, not search indexing.
"""
import json
import sys
import time
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = 'https://cesaragliardi-creator.github.io/alaya-999-public/'
KEY = '28d64bafdd7bc8ceff483428ccc5227d'
KEY_URL = ROOT + KEY + '.txt'
PUBLIC_PAGES = (ROOT, ROOT + 'pt/pesquisa.html', ROOT + 'en/research.html', ROOT + 'en/replicate.html')


def request(url):
    req = Request(url, headers={'User-Agent': 'ALAYA-999-Public-Discovery/1.0'})
    with urlopen(req, timeout=20) as response:
        return response.status, response.read(200000)


def main():
    report = {'timestamp_utc': datetime.now(timezone.utc).isoformat(),
              'key_location': KEY_URL, 'pages': list(PUBLIC_PAGES),
              'submissions': [], 'status': 'not_submitted'}
    # GitHub Pages builds can lag behind the push that triggered this workflow.
    # Recheck only public pages; do not submit an unverified URL.
    last_error = None
    for attempt in range(1, 13):
        try:
            status, content = request(KEY_URL)
            if status != 200 or content.decode('utf-8').strip() != KEY:
                raise ValueError('Project-scoped IndexNow key is unavailable or incorrect')
            for page in PUBLIC_PAGES:
                code, body = request(page)
                if code != 200 or b'ALAYA-999' not in body:
                    raise ValueError('Published research page is unavailable: ' + page)
            report['verification'] = 'IndexNow key and all %d public pages returned HTTP 200' % len(PUBLIC_PAGES)
            report['verification_attempts'] = attempt
            break
        except (ValueError, UnicodeError, HTTPError, URLError, TimeoutError, OSError) as exc:
            last_error = str(exc)
            if attempt < 12:
                time.sleep(15)
    else:
        report['error'] = 'Public site not ready after 12 checks: ' + (last_error or 'unknown')
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 2
    for page in PUBLIC_PAGES:
        params = urlencode({'url': page, 'key': KEY, 'keyLocation': KEY_URL})
        try:
            code, _ = request('https://api.indexnow.org/indexnow?' + params)
            report['submissions'].append({'url': page, 'http_status': code,
                                          'received': code in (200, 202)})
        except HTTPError as exc:
            report['submissions'].append({'url': page, 'http_status': exc.code,
                                          'received': False})
        except (URLError, TimeoutError, OSError) as exc:
            report['submissions'].append({'url': page, 'received': False,
                                          'error': str(exc)})
    report['status'] = ('received_not_indexed'
                        if report['submissions'] and
                        all(x['received'] for x in report['submissions'])
                        else 'partial_or_failed')
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report['status'] == 'received_not_indexed' else 1


if __name__ == '__main__':
    sys.exit(main())

"""Transfer one pre-verified binary release; this repository has no app source."""
import hashlib
import http.client
import json
import os
import shutil
import sys
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path, PurePosixPath

REPO = 'TongZi2003/Notara-Desktop-Releases'
RELEASE = 401046349
VERSION = '0.1.0-preview.5'
ARCHIVE_SHA = 'be18a7afa54f00b24363b038c7d8a645f6f5575a5074a9db1085de93478eaaa4'
INSTALLER_SHA = '1e1d9ca1659a86472a1e8d50084580227a88b9db37021814a22ef4e1fd7ae6a0'
token = os.environ['GH_TOKEN']
stage = 'read dispatch input'

def digest(path):
    with path.open('rb') as handle:
        return hashlib.file_digest(handle, 'sha256').hexdigest()

def api(path, method='GET', payload=None):
    request = urllib.request.Request('https://api.github.com/repos/' + REPO + path,
        data=json.dumps(payload).encode() if payload is not None else None, method=method,
        headers={'Authorization': 'Bearer ' + token, 'Accept': 'application/vnd.github+json', 'Content-Type': 'application/json'})
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.load(response)

try:
    # Read the temporary URL from the event file, never from interpolated shell
    # text or a logged environment variable. Only public-release bytes are moved.
    event = json.loads(Path(os.environ['GITHUB_EVENT_PATH']).read_text())
    url = event['inputs']['artifact_url']
    parsed = urllib.parse.urlsplit(url)
    assert parsed.scheme == 'https' and parsed.hostname.endswith(('.oaiusercontent.com', '.trycloudflare.com'))
    assert not parsed.username and not parsed.password
    print('Source link expiry:', urllib.parse.parse_qs(parsed.query).get('se', ['missing'])[0])
    stage = 'check release target'
    release = api(f'/releases/{RELEASE}')
    assert release['draft'] and release['tag_name'] == 'v' + VERSION and release['prerelease']
    stage = 'download pinned archive'
    archive = Path(os.environ['RUNNER_TEMP']) / 'verified-installers.zip'
    with urllib.request.urlopen(url, timeout=90) as incoming, archive.open('wb') as outgoing:
        total = 0
        while block := incoming.read(1024 * 1024):
            total += len(block)
            assert total <= 250_000_000
            outgoing.write(block)
    assert digest(archive) == ARCHIVE_SHA
    stage = 'verify archive members'
    output = Path(os.environ['RUNNER_TEMP']) / 'public-release'
    output.mkdir()
    with zipfile.ZipFile(archive) as source:
        names = [entry.filename for entry in source.infolist() if not entry.is_dir()]
        assert len(names) == len(set(names))
        assert sum(entry.file_size for entry in source.infolist()) < 2_000_000_000
        for name in names:
            path = PurePosixPath(name)
            assert not path.is_absolute() and '..' not in path.parts and '\\' not in name
        recorded = set()
        for row in source.read('SHA256SUMS.txt').decode('utf-8-sig').splitlines():
            expected, name = row.split(None, 1)
            name = name.lstrip('*')
            with source.open(name) as handle:
                assert hashlib.file_digest(handle, 'sha256').hexdigest() == expected
            recorded.add(name)
        assert recorded == set(names) - {'SHA256SUMS.txt'}
        original = f'Notara Setup {VERSION}.exe'
        installer = f'Notara-{VERSION}-windows-x64-Setup.exe'
        assert [name for name in names if name.endswith('.exe')] == [original]
        for name in [original, 'RELEASE-NOTES.md', 'UNSIGNED-PREVIEW.txt']:
            with source.open(name) as incoming, (output / (installer if name == original else name)).open('wb') as outgoing:
                shutil.copyfileobj(incoming, outgoing)
        assert digest(output / installer) == INSTALLER_SHA
        assert VERSION in (output / 'RELEASE-NOTES.md').read_text(encoding='utf-8-sig')
        licenses = sorted(name for name in names if name.startswith('licenses/'))
        assert 'licenses/THIRD-PARTY-NOTICES.md' in licenses
        with zipfile.ZipFile(output / 'THIRD-PARTY-LICENSES.zip', 'w', zipfile.ZIP_DEFLATED) as notices:
            for name in licenses:
                entry = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
                entry.compress_type = zipfile.ZIP_DEFLATED
                notices.writestr(entry, source.read(name))
    (output / 'SHA256SUMS.txt').write_text(''.join(f'{digest(path)}  {path.name}\n' for path in sorted(output.iterdir())), encoding='utf-8')
    expected = {path.name: digest(path) for path in output.iterdir()}
    for path in sorted(output.iterdir()):
        stage = 'upload ' + path.name
        existing = {asset['name']: asset for asset in api(f'/releases/{RELEASE}/assets')}
        if path.name in existing:
            assert existing[path.name]['digest'] == 'sha256:' + expected[path.name]
            continue
        connection = http.client.HTTPSConnection('uploads.github.com', timeout=180)
        with path.open('rb') as handle:
            connection.request('POST', f'/repos/{REPO}/releases/{RELEASE}/assets?name=' + urllib.parse.quote(path.name), body=handle,
                headers={'Authorization': 'Bearer ' + token, 'Content-Type': 'application/octet-stream', 'Content-Length': str(path.stat().st_size)})
            response = connection.getresponse()
            assert response.status == 201, 'asset upload HTTP ' + str(response.status)
            uploaded = json.loads(response.read())
            assert uploaded['digest'] == 'sha256:' + expected[path.name]
        connection.close()
        print('Verified upload:', path.name)
    stage = 'verify all server assets'
    actual = {asset['name']: asset for asset in api(f'/releases/{RELEASE}/assets')}
    assert set(actual) == set(expected)
    for name, value in expected.items():
        assert actual[name]['state'] == 'uploaded' and actual[name]['digest'] == 'sha256:' + value
    stage = 'publish prerelease'
    result = api(f'/releases/{RELEASE}', 'PATCH', {'draft': False, 'prerelease': True, 'make_latest': 'false'})
    assert not result['draft'] and result['prerelease']
    print('Published:', result['html_url'])
except Exception as error:
    # Never echo a credential-bearing download URL or an HTTP request object.
    print('Transfer failed at', stage, type(error).__name__, getattr(error, 'code', ''), file=sys.stderr)
    if stage == 'download pinned archive' and hasattr(error, 'read'):
        import re
        code = re.search(r'<Code>([A-Za-z0-9_]+)</Code>', error.read(8192).decode('utf-8', errors='replace'))
        if code:
            print('Storage error code:', code.group(1), file=sys.stderr)
    sys.exit(1)

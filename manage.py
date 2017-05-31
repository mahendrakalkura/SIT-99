from os import makedirs
from re import findall
from shutil import rmtree

from requests import request
from tidylib import tidy_document

DIRECTORY = 'files'


def main():
    rmtree(DIRECTORY)

    directory = '{directory:s}/css'.format(directory=DIRECTORY)
    makedirs(directory)

    directory = '{directory:s}/js'.format(directory=DIRECTORY)
    makedirs(directory)

    directory = '{directory:s}/images'.format(directory=DIRECTORY)
    makedirs(directory)

    response = request(
        method='GET',
        url='http://menshealthlife.net/testosterone-aw/?c=us',
    )

    options = {
        'alt-text': '',
        'doctype': 'strict',
        'force-output': 1,
        'indent': 1,
        'indent-spaces': 4,
        'output-xhtml': 0,
        'tidy-mark': 0,
        'wrap': 0,
    }
    contents, errors = tidy_document(response.text, options=options)

    for pattern in findall(r'href="(.*?)"', contents):
        if pattern == '/product-link.php?l=1':
            contents = contents.replace(
                '/product-link.php?l=1',
                'https://proshredelite.com/blue/?'
                'cp=106&AFID=MBZH&SID=&C1=menshealthlife-testosteroneus',
            )
            continue
        if pattern == '/product-link.php?l=2':
            contents = contents.replace(
                '/product-link.php?l=2',
                'https://proshredelite.com/blue/?'
                'cp=106&AFID=MBZH&SID=&C1=menshealthlife-testosteroneus',
            )
            continue
        if pattern in [
            'http://browsehappy.com/',
            'http://www.google.com/chromeframe/?redirect=true',
            'https://www.facebook.com/tr'
            '?id=123&amp;ev=Lead&amp;noscript=1',
        ]:
            continue
        source, target = download(pattern)
        if source and target:
            pattern = '{directory}/'.format(directory=DIRECTORY)
            target = target.replace(pattern, '')
            contents = contents.replace(source, target)

    for pattern in findall(r'src="(.*?)"', contents):
        source, target = download(pattern)
        if source and target:
            pattern = '{directory}/'.format(directory=DIRECTORY)
            target = target.replace(pattern, '')
            contents = contents.replace(source, target)

    path = '{directory:s}/index.html'.format(directory=DIRECTORY)
    with open(path, 'w') as resource:
        resource.write(contents)


def download(pattern):
    source = pattern

    file = pattern
    file = file.replace('/', '_')
    file = file.replace(':', '_')

    response = request(method='GET', url=source)

    content_type = response.headers['Content-Type']

    if 'css' in content_type:
        target = '{directory:s}/css/{file:s}'.format(
            directory=DIRECTORY,
            file=file,
        )
        with open(target, 'w') as resource:
            resource.write(response.text)
        return source, target

    if 'image' in content_type:
        target = '{directory:s}/images/{file:s}'.format(
            directory=DIRECTORY,
            file=file,
        )
        with open(target, 'wb') as resource:
            for chunk in response.iter_content(1024):
                resource.write(chunk)
        return source, target

    if 'javascript' in content_type:
        target = '{directory:s}/js/{file:s}'.format(
            directory=DIRECTORY,
            file=file,
        )
        with open(target, 'w') as resource:
            resource.write(response.text)
        return source, target

    return None, None


if __name__ == '__main__':
    main()

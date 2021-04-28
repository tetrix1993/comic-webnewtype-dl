import os
import requests


HTTP_HEADER_USER_AGENT = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) ' +
                                        'AppleWebKit/537.36 (KHTML, like Gecko) ' +
                                        'Chrome/50.0.2661.102 Safari/537.36'}
PREFIX = 'https://comic.webnewtype.com'
JSON_TEMPLATE = 'https://comic.webnewtype.com/contents/%s/%s/json/'
BASE_FOLDER = 'download'


def run():
    while True:
        print('URL Format: https://comic.webnewtype.com/contents/{series}/{chapter}/')
        series = input('Enter series: ')
        if len(series) == 0:
            break
        chapter = input('Enter chapter: ')
        if len(chapter) == 0:
            continue
        process_manga(series, chapter)


def process_manga(series, chapter):
    json_url = JSON_TEMPLATE % (series, chapter)
    try:
        json_obj = get_json(json_url)
        if isinstance(json_obj, list) and len(json_obj) > 0:
            save_folder = '%s/%s/%s' % (BASE_FOLDER, series, chapter)
            if not os.path.exists(save_folder):
                os.makedirs(save_folder)
            for i in range(len(json_obj)):
                image_url = PREFIX + json_obj[i]
                image_name = save_folder + '/' + str(i + 1).zfill(3) + '.jpg'
                download_image(image_url, image_name)
    except Exception as e:
        print('Error in processing %s' % json_url)
        print(e)


def get_json(url):
    response = ""
    headers = HTTP_HEADER_USER_AGENT
    try:
        response = requests.get(url, headers=headers).json()
    except Exception as e:
        print(e)
    return response


def download_image(url, filepath):
    headers = HTTP_HEADER_USER_AGENT
    if os.path.exists(filepath):
        print('File %s exists' % filepath)
        return 1
    try:
        with requests.get(url, stream=True, headers=headers) as r:
            if r.status_code >= 400:
                return -1
            with open(filepath, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            print('Downloaded %s' % url)
    except Exception as e:
        print('Failed to download %s' % url)
        print(e)
        return -1
    return 0


if __name__ == '__main__':
    run()

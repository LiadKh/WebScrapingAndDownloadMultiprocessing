#!/usr/bin/python

import getopt
import sys
from bs4 import BeautifulSoup
import requests


def get_links(url, div_type, prop, start_as):
    page = requests.get(url)
    data = page.text
    soup = BeautifulSoup(data)

    rv = []

    for link in soup.find_all(div_type):
        href = link.get(prop)
        if href.startswith(start_as):
            rv.append(href)

    return rv

# def download_video(url):


def find_all_url(url, resource_template, video_url):
    all_videos_link = []
    size = 5
    for resource in get_links(url, 'a', 'href', resource_template):
        if size > 0:
            size -= 1
            video_link = get_links(resource, 'source', 'src', video_url)[0]
            all_videos_link.append(video_link)
            print(video_link)


def main(argv):
    input_url = ''
    template_url = ''
    video_url = ''
    try:
        opts, args = getopt.getopt(argv, "hi:r:v:", ["help", "input=", "resource=", "video="])
    except getopt.GetoptError:
        print('Run the script with --help or -h option for more information')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('<script>.py -i <input website> -r <template resource> -v <video url>')
            sys.exit()
        elif opt in ("-i", "--input"):
            input_url = arg
        elif opt in ("-r", "--resource"):
            template_url = arg
        elif opt in ("-v", "--video"):
            video_url = arg
    if input_url == '' or template_url == '' and video_url == '':
        print('Run the script with --help or -h option for more information')
        sys.exit(2)
    print('Download from website ', input_url)
    print('Url same as ', template_url)
    print('Video template ', video_url)
    find_all_url(input_url, template_url, video_url)


if __name__ == "__main__":
    main(sys.argv[1:])

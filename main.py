#!/usr/bin/python

import getopt
import sys

import requests
from bs4 import BeautifulSoup

from downloadPool import download_pool


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


def find_all_url(url, resource_template, video_url, start, size):
    all_videos_link = []
    for resource in get_links(url, 'a', 'href', resource_template)[start:start + size]:
        video_link = get_links(resource, 'source', 'src', video_url)[0]
        all_videos_link.append(video_link)
    return all_videos_link


def main(argv):
    input_url = ''
    template_url = ''
    video_url = ''
    output_folder = ''
    start = 0
    size = 10
    try:
        opts, args = getopt.getopt(argv, "hi:r:v:o:s:n:",
                                   ["help", "input=", "resource=", "video=", "output=", "start=", "size="])
    except getopt.GetoptError:
        print('Run the script with --help or -h option for more information')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(
                '<script>.py -i <input website> -r <template resource> -v <video url> -o <output folder> \
                -s <start index> -n <size>')
            sys.exit()
        elif opt in ("-i", "--input"):
            input_url = arg
        elif opt in ("-r", "--resource"):
            template_url = arg
        elif opt in ("-v", "--video"):
            video_url = arg
        elif opt in ("-o", "--output"):
            output_folder = arg
        elif opt in ("-s", "--start"):
            start = int(arg)
        elif opt in ("-n", "--size"):
            size = int(arg)
    if input_url == '' or template_url == '' and video_url == '' and output_folder == '':
        print('Run the script with --help or -h option for more information')
        sys.exit(2)
    print('Download from website ', input_url)
    print('Url same as ', template_url)
    print('Video template ', video_url)
    print('From index ', start)
    print('Size ', size)
    all_videos_link = find_all_url(input_url, template_url, video_url, start, size)
    download_pool(all_videos_link, output_folder, start)


if __name__ == "__main__":
    main(sys.argv[1:])
    print("finish")

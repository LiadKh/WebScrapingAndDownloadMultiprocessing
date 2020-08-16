import os
import urllib.request
from multiprocessing import Pool, cpu_count

from progressbar import Bar, Percentage, ProgressBar


class DownloadProgressBar:
    def __init__(self, name):
        self.pbar = None
        self.name = name

    def __call__(self, block_num, block_size, total_size):
        if not self.pbar:
            self.pbar = ProgressBar(widgets=[Bar('=', '[', ']'), ' ', Percentage(), '\t', self.name], maxval=total_size)
            self.pbar.start()

        downloaded = block_num * block_size
        if downloaded < total_size:
            self.pbar.update(downloaded)
        else:
            self.pbar.finish()


def download_pool(all_video_links, output_folder, start):
    n = cpu_count() - 1
    p = Pool(n)
    lst = [(i + start, l, output_folder) for i, l in enumerate(all_video_links)]
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    p.map(download_video, lst)
    p.close()
    p.join()


def download_video(index_url_folder):
    index, url, output_folder = index_url_folder
    name = "{0}.{1}".format(index + 1, url.rsplit('.', 1)[1])
    full_file_name = os.path.join(output_folder, name)
    print("start downloading", index, url, name)
    urllib.request.urlretrieve(url, full_file_name, DownloadProgressBar(full_file_name))
    print("finish downloading", index, url, name)

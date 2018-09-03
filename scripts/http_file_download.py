# coding=utf-8
from bs4 import BeautifulSoup
import os, sys, urllib2, time, random

path = os.getcwd()
root_path = os.path.join(path, u'TempDownload')
if not os.path.isdir(root_path):
    os.mkdir(root_path)


def download_loop(url, dl_path):
    print url
    content = urllib2.urlopen(url)
    soup = BeautifulSoup(content,"html.parser")
    link = soup.find_all('a')
    for download in link:
        flink = download.get('href')
        if flink.find(".pdf", len(flink) - 4) <> -1 \
                or flink.find(".xls", len(flink) - 4) <> -1 \
                or flink.find(".txt",len(flink) - 4) <> -1 \
                or flink.find(".xlsx", len(flink) - 5) <> -1 \
                or flink.find(".rtf", len(flink) - 4) <> -1\
                or 1 == 1:
            print '+' + flink
            content2 = urllib2.urlopen(url + flink).read()
            with open(dl_path + '/' + flink, 'wb') as code:
                code.write(content2)
        temp = download.get_text()
        if flink.find("/", len(flink) - 1) <> -1 and temp <> u'Parent Directory':
            directory = str(flink[:-1])
            file_path = os.path.join(dl_path, directory.replace("%20", " "))
            if not os.path.isdir(file_path):
                os.mkdir(file_path)
            print '-' + flink + ' || path is:' + str(dl_path)
            new_url = url + flink
            download_loop(new_url, file_path)


##    print u'download completed'

if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] == "-h":
        usage = "Http file downloader Usage: " + sys.argv[0]  + " url"
        print usage
        sys.exit()

    url = sys.argv[1] + '/'

    download_loop(url, root_path)
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~END~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    raw_input("Press <Enter> To Quit!")
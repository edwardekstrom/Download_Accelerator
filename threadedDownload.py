import argparse
import os
import requests
import threading
from fileinput import filename

''' Downloader for a set of files '''
class Downloader:
    def __init__(self):
        ''' initialize the file where the list of URLs is listed, and the
        directory where the downloads will be stored'''
        self.args = None
        self.url = 'http://174.52.164.54/files/design-philosophy-sigcomm-88.pdf'
        self.threads = 10
        self.parse_arguments()

    def parse_arguments(self):
        ''' parse arguments, which include file '-d' for download directory'''
        parser = argparse.ArgumentParser(prog='Mass downloader', description='A simple script that downloads multiple files from a list of URLs specified in a file', add_help=True)
        parser.add_argument('--url', type=str, action='store', help='The URL to download',default='http://174.52.164.54/files/design-philosophy-sigcomm-88.pdf')
        parser.add_argument('-n', '--threads', type=int, action='store', help='Specify the number of threads used to download the file.',default=10)
        args = parser.parse_args()
        self.url = args.url
        self.threads = args.threads
        '''if not os.path.exists(self.dir):
            os.makedirs(self.dir)'''

    def download(self):
        ''' download the files listed in the input file '''
        # setup URLs
        '''urls = []
        f = open(self.in_file,'r')
        for line in f.readlines():
            urls.append(line.strip())
        f.close()'''
        # setup download locations
        file = self.url.split('/')[-1].strip()
        # get header content-length
        r = requests.head(self.url, stream=True)
        headers = r.headers
        print headers['content-length']
        contentLength = headers['content-length']
        sharedDictionary = {}
        # create a thread for each url
        threads = []
        d= DownThread(self.url,0,contentLength,sharedDictionary,0)
        threads.append(d)
        '''for f,url in zip(files,urls):
            filename = self.dir + '/' + f
            d = DownThread(url,filename)
            threads.append(d)'''
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        with open(file, 'wb') as f:
            f.write(sharedDictionary[0])

''' Use a thread to download part of a given file'''
class DownThread(threading.Thread):
    def __init__(self,url,startByte,endByte,sharedDict,index):
        self.url = url
        self.startByte = str(startByte)
        self.endByte = str(endByte)
        self.sharedDictionary = sharedDict
        self.index = index
        #print str(startByte) + ' - ' + str(endByte)
        threading.Thread.__init__(self)
        self._content_consumed = False

    def run(self):
        print 'Downloading %s' % self.url
        r = requests.get(self.url, stream=True, headers={'Range': 'bytes={0}-{1}'.format(self.startByte,self.endByte),'accept-encoding': ''})
        #print r.content
        print r
        self.sharedDictionary[self.index] = r.content
        #with open(self.filename, 'wb') as f:
         #   f.write(r.content)
 
if __name__ == '__main__':
    d = Downloader()
    d.download()
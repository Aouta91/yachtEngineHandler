import os
import errno


class transitPipe:
    def __init__(self, pathPipe):
        self.pathPipe = pathPipe
        try:
            os.mkfifo(self.pathPipe)
        except OSError as oe:
            if oe.errno != errno.EEXIST:
                raise
    def runReadPipe(self):

        while True:
            with open(self.pathPipe) as fifo:
                print("FIFO opened")
                while True:
                    data = fifo.read()
                    if len(data) == 0:
                        print("Writer closed")
                        break
                    print('Read: "{0}"'.format(data))

if __name__ == '__main__':
    wathcReadPipe = transitPipe('devYacht/IOstreams/out')
    wathcReadPipe.runReadPipe()

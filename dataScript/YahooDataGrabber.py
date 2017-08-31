#!/usr/bin/env python

import sys
import csv
import Queue
import threading
import ystockquote as ys


def gen_info_list(tickers, start, end):
    '''
    Given a list of ticker symbols, a start date, and an end date, return a
    list of dictionaries containing the information.
    '''
    return [{'symbol': ticker,    \
             'start': start, \
             'end': end}     \
             for ticker in tickers]

class FetcherThread(threading.Thread):

    def __init__(self, in_queue, out_queue):
        threading.Thread.__init__(self)
        self.in_queue = in_queue
        self.out_queue = out_queue

    def run(self):
        while True:
            spec = self.in_queue.get()
            data = ys.get_historical_prices(spec['symbol'], spec['start'], spec['end'])
            spec.update({'data': data})

            # Emit a new dictionary equivalent to spec but with a new key 'data'
            # containing the price data.
            self.out_queue.put(spec)
            self.in_queue.task_done()


class WriterThread(threading.Thread):
    '''
    A class to perform concurrent writes to the file system.
    '''

    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def __decorate(self, symbol, start, end):
        return '_'.join([symbol, start, end]) + '.csv'

    def run(self):
        while True:
            spec = self.queue.get()
            filename = spec['symbol']
            with open(filename, 'wb') as csvfile:
                writer = csv.writer(csvfile, delimiter=',', quotechar='"',
                                    quoting=csv.QUOTE_MINIMAL)
                writer.writerows(spec['data'])
            self.queue.task_done()

def main():
    with open('tickers.txt') as tickersFile:
        tickers = tickersFile.readlines()
    start_date = '20000101'
    end_date = '20170206'
    in_queue = Queue.Queue()
    out_queue = Queue.Queue()

    # Populate the in_queue with data
    for symbol in tickers:
        symbol = symbol.strip("\n")
        packet = {'symbol': symbol, 'start': start_date, 'end': end_date}
        in_queue.put(packet)

    # Spawn a pool of fetcher threads
    for i in range(4):
        t = FetcherThread(in_queue, out_queue)
        t.setDaemon(True)
        t.start()

    for i in range(4):
        w = WriterThread(out_queue)
        w.setDaemon(True)
        w.start()

    # Wait on the queues until everything has been processed
    in_queue.join()
    out_queue.join()


if __name__ == '__main__':
    main()
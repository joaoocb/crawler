import os   
import signal                                                                    
from multiprocessing import Pool 

processes = ('twitter_crawler.py', 'telegram_crawler.py')


def run_crawler(process):
    os.system('python {}'.format(process))


def main():
    #original_sigint_handler = signal.signal(signal.SIGINT, signal.SIG_IGN)
    pool = Pool(processes=2)
    pool.daemon=True
    #signal.signal(signal.SIGINT, original_sigint_handler)
    try:
        print('Press Ctrl+C to stop')
        pool.map(run_crawler, processes)
    except KeyboardInterrupt:
        print("Keyboard interrupt received! Stoping...")
        pool.terminate()
        pool.join()
        pass

if __name__ == '__main__':
    main()
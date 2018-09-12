from urllib.request import urlopen
import time
import threading
import logging
import os
import configparser

logger = logging.getLogger('page')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('page_check.log')
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)
config = configparser.ConfigParser()
config.read('config.ini',"utf-8-sig")
url = config['page']['url']
restart = config['page']['restart']
timer = int(config['page']['timer'])

def check_baseline():
    try:
        resp = urlopen(url)
        code = resp.getcode()  
        if code == 200:
            logger.info(f'url:{url};-the result is :{code},连接正常')
        else:
            logger.info(f'-未连上页面，执行{restart}')
            os.system(restart)
    except Exception as e:
        print(e)
        logger.info(f'-未连上页面，执行{restart}')
        os.system(restart)
    finally:
        if 1:
            threading.Timer(timer, check_baseline).start()

if __name__ == "__main__":
    logger.info('baseline check start')
    threading.Timer(timer, check_baseline).start()
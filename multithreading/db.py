import logging
import threading
import time
from concurrent.futures import ThreadPoolExecutor

class Database:
    def __init__(self):
        self.value = 0
        self._lock = threading.Lock()

    def update(self, name):
        logging.info("Thread %s: starting update", name)
        logging.debug("Thread %s about to lock", name)
        
        with self._lock:
            logging.debug("Thread %s has lock", name)
            local_copy = self.value
            local_copy += 1
            time.sleep(0.1)
            self.value = local_copy
            logging.debug("Thread %s about to release lock", name)
        
        logging.debug("Thread %s after release", name)
        logging.info("Thread %s: finishing update", name)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    database = Database()
    logging.info("Testing update. Starting value is %d.", database.value)
    
    with ThreadPoolExecutor(max_workers=2) as executor:
        for index in range(2):
            executor.submit(database.update, index)
    
    logging.info("Testing update. Ending value is %d.", database.value)


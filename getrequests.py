import datetime, sys, queue
import urllib, urllib.request
from socket import timeout
from urllib.error import HTTPError, URLError
from threading import Thread
from config import url, get_logger

logger = get_logger("requests")

def time_monitor(timestamps):
    """
    This function sends a GET request to the url at every given timestamp until all timestamps have been reached.
    
    Parameters:
    timestamps [ ]: List of timestamps at which requests must be sent.
    
    Returns:
    response_codes [ ]: List of HTTP response codes that contains one HTTP response code for every sent request.
    """
    timestamps = check_validity(timestamps)
    if timestamps==[]: return []
    response_codes = []

    ts_dict = build_timestamp_dict(timestamps)

    while(True):
        curr_time = datetime.datetime.now().strftime("%H:%M:%S")
        if curr_time in timestamps:
            if ts_dict[curr_time] > 1:
                requests = []
                for i in range(ts_dict[curr_time]):
                    requests.append(curr_time)
                    timestamps.remove(curr_time)
                response_codes.extend(send_multiple_get_requests(requests, 16))
            else: 
                timestamps.remove(curr_time)
                response_codes.append(send_single_get_request(curr_time))
        if timestamps == []:
            return response_codes

def build_timestamp_dict(timestamps):
    """
    This function builds a dictionary to account for equal timestamps.

    Returns:
    ts_dict {timestamp: int}: Dict of timestamps and integers that count the occurences of each timestamp.
    """
    ts_dict = { }
    for t in timestamps:
        ts_dict[t]=0
    for t in timestamps:
        ts_dict[t]+=1
    return ts_dict 

def check_validity(timestamps):
    """
    This function checks the timestamp input list for emptiness and removes timestamps that are before runtime.
    
    Parameters:
    timestamps [ ]: List of timestamps at which requests must be sent.

    Returns:
    timestamps [ ]: List of timestamps after filtering out any invalid timestamps
    """
    if len(timestamps)==0:
        return []
    ts_to_remove = []
    for i in range(0, len(timestamps)):
        now = datetime.datetime.strptime(datetime.datetime.now().strftime("%H:%M:%S"), "%H:%M:%S")
        try: 
            curr_timestamp = datetime.datetime.strptime(timestamps[i], "%H:%M:%S")
        except:
            return []
        #set_trace()
        if now > curr_timestamp:
            if len(timestamps) == 1:
                return []
            else:
                ts_to_remove.append(timestamps[i])
    for ts in ts_to_remove: timestamps.remove(ts)
    return timestamps

def send_single_get_request(timestamp):
    """
    This function sends one GET request to the global url and handles the HTTP response.

    Parameters:
    timestamp (str): The specific timestamp at which the GET request will be sent.

    Returns:
    resp_code [ (int) ]: HTTP response code (eg. 200) resulting from GET request.
    """
    agent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36'}
    page = urllib.request.Request(url, headers=agent)
    resp_code = []
    logger.info("Sending One GET Request for Timestamp: " + timestamp)
    try:

        response = urllib.request.urlopen(page, timeout=0.5)
        resp_code = response.getcode()
    except HTTPError as error:
        logger.error(error)
    except URLError as error:
        if error == timeout:
            logger.error("Request Timed Out")
        else:
            logger.error(error)
    logger.info("Received Response from GET Request for Timestamp: " + timestamp)

    return resp_code

def send_multiple_get_requests(timestamps, no_workers):
    """
    This function sends multiple GET requests at the same timestamps using thread parallelization.

    Parameters:
    timestamps [ (str) ]: List of identical timestamps at which the GET requests will be sent.
    no_workers (int): The number of workers used to parallelize the GET requests.

    Returns:
    resp_codes [ (int) ]: List of HTTP response codes that result from the simultaneous GET requests.

    Classes:
    Worker (Thread): This class extends the Thread class to run simultaneous GET requests.
        Methods:
        __init__(self, request_queue): The constructor for the Worker class.
            Parameters:
            request_queue (queue): The queue of timestamps at which requests will be sent.
        run(self): Executes the GET requests for the timestamps in the request_queue
    """
    class Worker(Thread):
        def __init__(self, request_queue):
            Thread.__init__(self)
            self.queue = request_queue
            self.results = []
        def run(self):
            while(True):
                content = self.queue.get()
                if content == "":
                    break
                resp_code = send_single_get_request(content)
                self.results.append(resp_code)
                self.queue.task_done()
    
    q = queue.Queue()
    for ts in timestamps:
        q.put(ts)
    for _ in range(no_workers):
        q.put("")

    workers = []
    for _ in range(no_workers):
        worker = Worker(q)
        worker.start()
        workers.append(worker)

    for worker in workers:
        worker.join()

    resp_codes = []
    for worker in workers:
        resp_codes.extend(worker.results)
    return resp_codes

def print_result_at_exit(resp_codes):
    if resp_codes==[]:
        print("No GET Requests were Sent")
    else:
        errors = 0
        for code in resp_codes:
            if code != 200:
                errors += 1
        if errors > 0:
            print(str(errors) + " Requests Were Not Sent and Received Successfuly")
        else:
            print("All Requests were Sent and Received Successfully")

if __name__ == "__main__":
    timestamps = []

    if len(sys.argv) > 1:
        timestamps = sys.argv[1:]

    resp_codes = time_monitor(timestamps)
    print_result_at_exit(resp_codes)    
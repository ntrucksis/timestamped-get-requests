import getrequests
import datetime
import unittest
from config import url, get_logger
import urllib

logger = get_logger("tests")

class test_simple(unittest.TestCase):

    def test_no_timestamps(self):
        """
        This function tests that inputting no timestamps will run no GET requests.
        """
        logger.info("Testing with No Timestamp")
        res = getrequests.time_monitor([])
        self.assertEqual(res, [], "Test with no timestamp failed")

    def test_invalid_timestamp(self):
        """
        This function tests that inputting a timestamp that has already passed will run no GET requests.
        """
        logger.info("Testing with One Invalid Timestamp")
        now = datetime.datetime.now()
        timestamps = [(now - datetime.timedelta(seconds=5)).strftime("%H:%M:%S")]
        res = getrequests.time_monitor(timestamps)
        self.assertEqual(res, [], "Test with invalid timestamp failed")
    
    def test_valid_and_invalid_timestamps(self):
        """
        This function tests that inputting one invalid timestamp and one valid timestamp will 
        run one GET request (for the valid timestamp).
        """
        logger.info("Testing with One Valid Timestamp and One Invalid Timestamp")
        now = datetime.datetime.now()
        invalid_timestamp = (now - datetime.timedelta(seconds=5)).strftime("%H:%M:%S")
        valid_timestamp = (now + datetime.timedelta(seconds=5)).strftime("%H:%M:%S")
        timestamps = [invalid_timestamp, valid_timestamp]
        res = getrequests.time_monitor(timestamps)
        self.assertEqual(res, [200], "Test with invalid and valid timestamps failed")
    
    def test_one_timestamp(self):
        """
        This function tests that inputting one timestamp will run one GET request.
        """
        logger.info("Testing with One Timestamp")        
        now = datetime.datetime.now()
        timestamps = [(now + datetime.timedelta(seconds=5)).strftime("%H:%M:%S")]
        res = getrequests.time_monitor(timestamps)
        self.assertEqual(res, [200], "Test with one timestamp failed")

    def test_two_timestamps(self):
        """
        This function tests that inputting two timestamps will run two GET requests.
        """
        logger.info("Testing with Two Timestamps")
        now = datetime.datetime.now()
        timestamp = (now + datetime.timedelta(seconds=5)).strftime("%H:%M:%S")
        timestamp_2 = (now + datetime.timedelta(seconds=10)).strftime("%H:%M:%S")
        timestamps = [timestamp, timestamp_2]
        res = getrequests.time_monitor(timestamps)
        self.assertEqual(res, [200, 200], "Test with two timestamps failed")

class test_difficult(unittest.TestCase):
    def test_five_timestamps_one_second_apart(self):
        """
        This function tests that inputting five consecutive timestamps, each two seconds after
        the previous, will run 5 GET requests.
        """
        logger.info("Testing with Five Consecutive Timestamps")
        now = datetime.datetime.now()
        timestamps = []
        j = 0
        for i in range(5):
            j+=1
            timestamps.append((now + datetime.timedelta(seconds=5+i+j)).strftime("%H:%M:%S"))
        res = getrequests.time_monitor(timestamps)
        self.assertEqual(res, [200, 200, 200, 200, 200], "Test with 5 consecutive timestamps failed")

    def test_two_identical_timestamps(self):
        """
        This function tests that inputting two equal timestamps will run two simultaneous GET requests.
        """
        logger.info("Testing with Two Identical Timestamps")
        now = datetime.datetime.now()
        timestamps = []
        for i in range(2):
            timestamps.append((now + datetime.timedelta(seconds=5)).strftime("%H:%M:%S"))
        res = getrequests.time_monitor(timestamps)
        self.assertEqual(res, [200, 200], "Test with 2 identical timestamps failed")

    def test_five_identical_timestamps(self):
        """
        This function tests that inputting five equal timestamps will run five simultaneous GET requests.
        """        
        logger.info("Testing with Five Identical Timestamps")
        now = datetime.datetime.now()
        timestamps = []
        for i in range(5):
            timestamps.append((now + datetime.timedelta(seconds=5)).strftime("%H:%M:%S"))
        res = getrequests.time_monitor(timestamps)
        self.assertEqual(res, [200, 200, 200, 200, 200], "Test with 5 identical timestamps failed")

    def test_consecutive_and_simultaneous_timestamps(self):
        """
        This function tests that inputting two consecutive timestamps, followed by two equal timestamps,
        followed by a consecutive timestamp will run five GET requests.
        """
        logger.info("Testing with Consecutive and Simulataneous Timestamps")
        now = datetime.datetime.now()
        timestamps = []
        j = 0
        for i in range(2):
            j += 1
            timestamps.append((now + datetime.timedelta(seconds=5+i+j)).strftime("%H:%M:%S"))
        for i in range(2):
            timestamps.append((now + datetime.timedelta(seconds=10)).strftime("%H:%M:%S"))
        timestamps.append((now + datetime.timedelta(seconds=15)).strftime("%H:%M:%S"))
        res = getrequests.time_monitor(timestamps)
        self.assertEqual(res, [200, 200, 200, 200, 200], "Test with identical and consecutive timestamps failed")

    def test_manual_vs_output(self):
        """
        This function tests that making a GET request manually and making a GET request via
        the getrequests program will both return the same HTTP code.
        """
        logger.info("Testing a Request from GetRequests Versus a Manual Request")
        request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(request, timeout=0.5)
        resp_code = response.getcode()

        now = datetime.datetime.now()
        timestamps = [(now + datetime.timedelta(seconds=15)).strftime("%H:%M:%S")]
        res = getrequests.time_monitor(timestamps)

        self.assertEqual(resp_code, res[0])
    

if __name__ == "__main__":
    unittest.main()


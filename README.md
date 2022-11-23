# Timestamped GET Requests - Nick Trucksis
## Description
The goal of this project is to recieve a list of timestamps and make GET requests exactly at each of these timestamps to the URL ```http://ifconfig.co/``` .  This goal includes accounting for equal timestamps, where multiple GET requests must be sent at the same time.

The implementation used in this project runs indefinitely until a GET request has been sent at every provided timestamp.  Once the current time has reached a known timestamp, one or more GET requests will be sent depending on whether the current timestamp has multiple occurences.  To view the timing of these requests, the dev.log file contains the times of each GET request and HTTP response, which will show whether requests were sent sequentially or simultaneously.  In testing, consecutive timestamps within two seconds of each other are supplied, as well as identical timestamps.

## Files

- getrequests.py
-- Handles the Sending of GET Requests that Execute at Provided Timestamps
- test.py
-- Supplies Various Groups of Timestamps to Test the Behavior of getrequests.py
- config.py
-- Contains the Global URL that Requests are Made To
-- Contains the Logger Setup 
- dev.log
-- Contains the Times at which Each Request and Response were Sent or Received, Respectively

## How to Run
To run getrequests.py :
Provide timestamp values in the form of HH::MM:SS as CLI arguments
```sh
python getrequest.py arg1 arg2 arg3...
```
Example Run and Output:
```sh
python getrequest.py 09:15:25 11:58:23 13:45:09 13:45:09 13:45:09 17:22:00 17:22:00
All Requests were Sent and Received Successfully
```
To run tests.py:
```sh
python tests.py
```
# Notes
- The dev.log file updates with every run
- The tests.py file takes ~80 seconds to run every test

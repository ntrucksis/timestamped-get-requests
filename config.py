import urllib.parse
import logging

base_url = "http://ifconfig.co/"
params = {
    "param1": "GET"
}
query_string = urllib.parse.urlencode( params )
url = base_url + "?" + query_string

def get_logger(name):
    """
    This function configures a logger than can be imported and used in other modules
    """
    log_format = '%(asctime)s  %(name)8s  %(levelname)5s  %(message)s'
    logging.basicConfig(level=logging.DEBUG,
                        format=log_format,
                        filename='dev.log',
                        filemode='w',
                        datefmt='%Y-%m-%d %H:%M:%S')
    #console = logging.StreamHandler()
    #console.setLevel(logging.DEBUG)
    #console.setFormatter(logging.Formatter(log_format))
    #logging.getLogger(name).addHandler(console)
    return logging.getLogger(name)
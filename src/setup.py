import argparse
import logging
import os
import subprocess

def setup(debug_mode):
    logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s] :: %(message)s", "%Y-%m-%d %H:%M:%S")
    rootLogger = logging.getLogger()
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)
    
    if debug_mode:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.info("Application in DEBUG Mode")
    else:
        logging.getLogger().setLevel(logging.INFO)
        fileHandler = logging.FileHandler("{0}/{1}.log".format(args.log_dir, "log"), mode='w')
        fileHandler.setFormatter(logFormatter)
        rootLogger.addHandler(fileHandler)
        logging.info("Application in INFO Mode")

        return

parser = argparse.ArgumentParser(description='Motion analysis and beat-timing video mapping features.')

parser.add_argument('--debug', default=False, type=bool,
                    help="Debug session set to True does not create log file for experiment and all info is displayed on console")

parser.add_argument('--input', default="input.mid", type=str)
parser.add_argument('--input_dir', default="../input", type=str)
parser.add_argument('--log_dir', default="../log", type=str)
args = parser.parse_args()

#check if video and path exists TODO
#check if input args are all valid and if they need debugging TODO
setup(args.debug)

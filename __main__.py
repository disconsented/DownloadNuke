import configparser
import logging
import datetime
import os
import shutil
import sys

fileConfig = 'config.ini'
fileLog = '{0:%Y-%m-%d}'.format(datetime.datetime.now())+".log"
dateNow = datetime.datetime.now();

#Logging and config setup
logging.basicConfig(filename=fileLog, level=logging.INFO)

config = configparser.ConfigParser()

#Config file didnt exist and then exit afterwards
if not os.path.isfile(fileConfig):
    config['SETTINGS'] = {'location': 'D:\\Downloads\\',
                          'days': 180}
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    sys.exit(0)

config.read(fileConfig)
config.sections()

#Echoing config settings
folderLocation = config['SETTINGS'].get('location', 'D:\\Downloads\\')

fileThreshold = dateNow + datetime.timedelta(days=-int(config['SETTINGS'].get('days', '180')))
logging.info("Location:" + folderLocation)
logging.info("Days:" + config['SETTINGS'].get('days', '180'))
logging.info("Threshold date:" + fileThreshold.isoformat())

for file in os.listdir(folderLocation):
    creationDate = datetime.datetime.utcfromtimestamp(os.stat(folderLocation + file).st_ctime)
    location = folderLocation + file
    fileName = location.encode("utf-8")
    logging.info('Found {} created at {}'.format(fileName, creationDate))
    if creationDate < fileThreshold:
        logging.info("{} is older than the threshold by {} days, deleting.".format(fileName, (fileThreshold - creationDate).days))
        try:
            if os.path.isdir(location):
                shutil.rmtree(location)
            elif os.path.isfile(location):
                os.remove(location)
            else:
                logging.error(fileName + ' is unknown')
        except Exception as e:
            logging.error(e)

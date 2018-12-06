import configparser
import os


def getConfug(section, key):
    config = configparser.ConfigParser()
    path = os.path.split(os.path.realpath(__file__))[0]+'/section.conf'
    config.read(path)
    return config.get(section, key)

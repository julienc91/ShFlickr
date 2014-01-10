#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Julien Chaumont"
__copyright__ = "Copyright 2014, Julien Chaumont"
__licence__ = "MIT"
__version__ = "1.0.1"
__contact__ = "julienc91 [at] outlook.fr"



# Ask Flickr for a non-commercial API key
# http://www.flickr.com/services/apps/create/apply/
API_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
API_SECRET = 'XXXXXXXXXXXXXXXX'


# Your user id is the last part of the url when you go to your profile:
# http://www.flickr.com/photos/XXXXXXXXXXXXX/
USER_ID = 'XXXXXXXXXXXXXX'


# The folder which contains all the pictures to synchronize
PICTURE_FOLDER_PATH = '~/Pictures/'
# The file extensions to synchronize
PICTURE_EXTENSIONS = ('.JPG', '.jpg')
# A regular expression to select all your different subdolders
# insed the main folder.
# You can just set it to r'' if you want to select all your subfolders.
SUBFOLDERS_REGEXP = r'^[01]\d-((0[1-9])|(1[0-2]))$'


# Set to 1 if the uploaded pictures can be seen by everyone, 0 otherwise
VISIBLE_PUBLIC = 0
# Set to 1 if the uploaded pictures can be seen by your family,
# 0 otherwise
VISIBLE_FAMILY = 0
# Set to 1 if the uploaded pictures can be seen by your friends,
# 0 otherwise
VISIBLE_FRIEND = 0


# Max number of failed uploads for a single photo before
# uploading the next one.
MAX_RETRIES = 3
# Max number of consecutive failed uploads before exit.
MAX_CONSECUTIVE_ERRORS = 5

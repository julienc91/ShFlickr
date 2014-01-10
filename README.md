ShFlickr
========

Python script to easily synchronize a picture folder with a Flickr account


Licence: MIT
Author:  Julien CHAUMONT
Contact: julienc91 [at] outlook.fr
Version: 1.0.1 - 10/01/2014


Introduction
------------

Flickr is a popular image hosting website. It offers a free storage of 1TB to all users.
Therefore, it is a good choice to back-up all your pictures.

ShFlickr allows you to synchronize your local picture folder with your Flickr account easily from your shell.


Be aware that ShFlickr was initially a script for my own use. I decided to put it on Github to share it with people who want to synchronize easily their pictures with their Flickr account.
This is the main reason why ShFlickr does not have a lot of features: I just did not need them.
However, if other people are interested by this project, I may try to improve it with new versions from time to time.


Requirements
------------

* python 2.7
* The Python Flickr API module by Sybren Stüvel (http://stuvel.eu/flickrapi)
* A Flickr account (http://www.flickr.com)
* A Flickr API key (http://www.flickr.com/services/apps/create/apply

Unfortunately, you cannot use ShFlickr without an API Key, as Yahoo limits requests to its Flickr API up to 3600 per hour. Consequently, every user must have its own API key. But don't worry, it is totally free and easy to have! You just have to fill a form to request a non-commercial API key (2 minutes of your time max).

*Note: * to install the Python Flickr API, you can use `apt-get install python-flickr-api` on Debian, or `yum install python-flickrapi` on Fedora. For other OS, refer to the official documentation of the API.


Installation
------------

* Using git:
`git clone https://github.com/julienc91/ShFlickr.git`
`cd ShFlickr`
* Using a zip archive:
`wget https://github.com/julienc91/ShFlickr/archive/master.zip`
`unzip master.zip`
`cd ShFlickr`

Then you will have to edit the `config.py` file with your Flickr account informations:
* `API_KEY`: the public key provided by Flickr (you need to request it first)
* `API_SECRET`: the secret key of the API
* `USER_ID`: your Flickr unique id
You will also have to indicate informations about your picture folders:
* `PICTURE_FOLDER_PATH`: absolute path to your picture folder root
* `PICTURE_EXTENSIONS`: only files whose name ends with one of the element in the list will be synchronized (it is case sensitive)
* `SUBFOLDERS_REGEXP`: a regular expression to select the subfolders you want to synchronize. If you don't know what a regular expression is, just let it as "r''".


Folder organization
-------------------

The Flickr API has some limitations. For instance, it is not possible to list all the pictures of a user.
ShFlickr needs to get the whole list of uploaded pictures to see which ones are not syncrhonized yet. To do so, ShFlickr needs to create *photosets* to organize your pictures on Flickr.
Thus, instead of getting the entire list of uploaded pictures, ShFlickr retrieves the list of uploaded pictures per photoset. But to do this correctly, you must have created subfolders in your main picture folder, each folder corresponding to a photoset to create. For instance:
`~/Pictures` is my main picture folder
`~/Pictures/13-11, ~/Pictures/13-12, ~/Pictures/14-01, ~/Pictures/Trip_to_London` are my subfolders and contain my pictures.
Do not forget to set the `SUBFOLDERS_REGEXP` variable in the configuration file to match your subfolders!
Currently, only pictures which are directly located in those subfolders will be synchronized (it may change in a future version, along with other improvements).


Usage
-----

You just have to run the following command line to let ShFlickr do its job:
`python main.py`
To interrupt ShFlickr, use '^C' (the `ctrl` key of your keyboard along with the `C` key) or just close your shell. The synchronization will continue from where it stopped at its next launch (however, it will restart the uploading of the last picture from the beginning). 

#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Julien Chaumont"
__copyright__ = "Copyright 2014, Julien Chaumont"
__licence__ = "MIT"
__version__ = "1.0.2"
__contact__ = "julienc91 [at] outlook.fr"



import flickrapi
import os, sys
import re
from config import *


class ShFlickr:

    ##
    # Connexion to Flickr.
    #
    def __init__(self):
        self.flickr = flickrapi.FlickrAPI(API_KEY, API_SECRET)
        (token, frob) = self.flickr.get_token_part_one(perms='write')
        if not token:
            raw_input("Press ENTER after you authorized this program")
        self.flickr.get_token_part_two((token, frob))


    ##
    # Get the list of files to synchronize with Flickr.
    # @param folder     Path to the main folder
    # @return A tuple (photos_to_sync, photosets_to_create) where photos_to_sync
    #  is the list of files to synchronize for each subfolder, and
    #  photoset_ids is the list of albums with their respective id on Flickr,
    #  or None if the album does not exist yet.
    #
    def synclist(self, folder=PICTURE_FOLDER_PATH):

        print "Getting the list of pictures to synchronize..."
        subfolders = [lfile for lfile in os.listdir(unicode(folder))
                      if os.path.isdir(os.path.join(folder, lfile))
                      and re.match(SUBFOLDERS_REGEXP, lfile)]
        photosets = self.flickr.photosets_getList(user_id=USER_ID)
        photos_to_sync = {}
        photoset_ids = {}
        for subfolder in subfolders:
            subfolder = subfolder.encode("UTF-8")
            # Check if the album already exists on Flickr
            photoset_id = None
            for photoset in photosets.find('photosets').findall('photoset'):
                photoset_title = photoset.find('title').text
                if type(photoset_title) == unicode:
                    photoset_title = photoset_title.encode("UTF-8")
                if photoset_title == subfolder:
                    photoset_id = str(photoset.attrib['id'])
                    break
            photoset_ids[subfolder] = photoset_id

            # Get the list of pictures to synchronize within this album
            photos_to_sync[subfolder] = self.synclist_subfolder(os.path.join(folder, subfolder), photoset_id)
        return photos_to_sync, photoset_ids
        

    ##
    # Get the list of pictures to synchronize within an album.
    # @param subfolder     Complete path to the subfolder to synchronize
    # @param photoset_id   Id of the album on Flickr, or None of the album does not exist yet
    # @return The list of the pictures to synchronize.
    #    
    def synclist_subfolder(self, subfolder, photoset_id=None):
        files = [lfile for lfile in os.listdir(unicode(subfolder))
                 if lfile.endswith(PICTURE_EXTENSIONS)]
        files_to_sync = []
        if photoset_id is not None:
            # Find which file were not uploaded
            photoset = list(self.flickr.walk_set(photoset_id))
            for lfile in files:
                lfile = lfile.encode("UTF-8")
                found = False
                for photo in photoset:
                    photo = photo.get('title')
                    if type(photo) == unicode:
                        photo = photo.encode("UTF-8")
                    if photo == lfile:
                        found = True
                        break
                if not found:
                    files_to_sync.append(lfile)
        else:
            for lfile in files:
                files_to_sync.append(lfile)
        return files_to_sync


    ##
    # Performs the upload.
    # @param photos_to_sync       A dictionary containing the list of
    #                             pictures to upload for each subfolder.
    # @param photoset_ids         Dict of albums and their Flickr ids.
    # @param folder               Path to the main folder.
    #
    def upload(self, photos_to_sync, photosets={}, folder=PICTURE_FOLDER_PATH):
        
        for subfolder in sorted(photos_to_sync):
            count = 1
            total = len(photos_to_sync[subfolder])
            len_count = len(str(total))
            consecutive_errors = 0            
            print "Album %s: %s photos to synchronize" % (subfolder, total)
            
            for photo in sorted(photos_to_sync[subfolder]):
                print "%-*s/%s\t %s" % (len_count, count, total, photo)
                
                nb_errors = 0
                done = False
                while nb_errors < MAX_RETRIES and not done:
                    try:
                        response = self.flickr.upload(filename=os.path.join(folder, subfolder, photo),
                                                      title=photo,
                                                      is_public=VISIBLE_PUBLIC,
                                                      is_family=VISIBLE_FAMILY,
                                                      is_friend=VISIBLE_FRIEND)
                    except KeyboardInterrupt:
                        print "Exit by user request"
                        return
                    except:
                        nb_errors += 1
                        consecutive_errors += 1
                        if consecutive_errors >= MAX_CONSECUTIVE_ERRORS:
                            print "5 failed uploads in a row, aborting."
                            return
                        else:
                            print "Error, retrying upload (%s/%s)" % (nb_errors, MAX_RETRIES)
                    else:
                        photo_id = response.find('photoid').text
                        done = True
                        count += 1
                        consecutive_errors = 0
                        if photoset_ids[subfolder] is None:
                            print "Creating the remote album %s" % subfolder
                            response = self.flickr.photosets_create(title=subfolder,
                                                         primary_photo_id=photo_id)
                            photoset_ids[subfolder] = response.find('photoset').attrib['id']
                        else:
                            self.flickr.photosets_addPhoto(photoset_id=photoset_ids[subfolder],
                                                          photo_id=photo_id)
                if nb_errors == 3:
                    print "%s failed to upload" % photo



if __name__ == "__main__":
    shflickr = ShFlickr()
    photos_to_sync, photoset_ids = shflickr.synclist()
    shflickr.upload(photos_to_sync, photoset_ids)

    


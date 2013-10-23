-12 # Copyright (C) 2010, One Laptop Per Child
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

#use this program to load information into the db - assume item and thumbnail are already in /library/media

from django.core.management.base import BaseCommand, CommandError
from django.core.files.storage import default_storage
from django.core.files import File

import os, subprocess
import json

from library.models import Book
import schoolsite.settings
from path import path
import datetime
src = path('/library/schoolsite/static/media')

"""
This command shows a collection specified by the filepath. A collection is 
a folder (e.g. p01) containing:
  a file: books.json with a list of json (dictionaries) entries, one for each item in the collection
  a file for each item to be added to the library (e.g. title.pdf)
  a thumbnails folder containing the cover image for the each item: title.png (where title is the item's file name)

The collection is in /media/usb0/xc-library. The library is in /library/media.
Each folder in xc-library and in media corresponds to a language and has the two letter code for the language.
The collection itself has (by convention) a three-letter name such as P01 or A01.
For example, the absolute path of the source collection could be /media/usb0/xc-library/en/P01 or
/media/usb0/xc-library/xo/A01 (where xo is the language code for the Sugar activities.
The library stores the metadata in a database and has a folder corresponding to the collection as, for example,
/media/en/P01 or /media/xo/A01. These folders contain the files themselves and the thumbnails.

This program:
     reads each dictionary item in books.json or meta in otr, 
     updates the database with the metadata,
     copies the file to the folder for the collection in /media
     copies the thumnail to the thumbnail folder for the collection in /library/schoolsite/static/media

The command for this program is: python manage.py showCollection xo/A01 
(where xo is the language and A01 is the collection) 
"""

class Command(BaseCommand):
    help = "Shows a collection"
    args = 'xo/A01 where xo is the language and A01 is the collection'

    def handle(self, filepath='', *args, **options):
        temp = filepath.split('/')
        lng = temp[0]
        collection = temp[1]
        bookset = Book.objects.filter(a_collection=collection)
        print 'collection', len(bookset), collection
        if bookset:
            for i in range(len(bookset)-1):
                book = bookset[i]
                print book.a_title,
                print book.a_author,
                print book.a_summary,
                print book.dc_language,
                print book.a_collection,
                print book.cover_img,
                print book.mime_type,
                print book.book_file
            else:
                print 'bookset not found', collection
    


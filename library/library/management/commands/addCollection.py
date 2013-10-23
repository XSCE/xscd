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

from django.core.management.base import BaseCommand, CommandError
from django.core.files.storage import default_storage
from django.core.files import File

import os, subprocess
import json

from books.models import Book
import settings
from path import path
import datetime
src = path('/media/usb0/xc-library')
tgt = path('/library/media/')

"""
This command adds or updates a collection specified by the filepath. A collection is 
a folder (e.g. P01) containing:
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
     reads each dictionary item in books.json, 
     updates the database with the metadata,
     copies the file to the folder for the collection in /media
     copies the thumnail to the thumbnail follder for the collection in /media

The command for this program is: python manage.py addCollection xo/A01 
(where xo is the language and A01 is the collection) 
"""

class Command(BaseCommand):
    help = "Adds a collection"
    args = 'Absolute path to collection'

    def handle(self, filepath='', *args, **options):
        print filepath
        temp = filepath.split('/')
        lng = temp[0]
        collection = temp[1]
        collectionPath = tgt / lng / collection
        thumbnailPath = collectionPath / 'thumbnails'
        subprocess.call('mkdir -p ' + thumbnailPath,shell=True)
        pth = src / lng / collection
        """
        Store books from a file in JSON format.
        
        """
        jsonpath = pth / 'books.json'
        jsonfile = open(jsonpath)
        txt=jsonfile.read()
        jsonfile.close()
        data_list = eval(txt)
        log = open('log','w')
        print 'items',len(data_list)
        for d in data_list:
            # Get a Django File from the given path:
            book = pth / d['book_file']
            print book, os.path.exists(book)
            if os.path.exists(book):
                subprocess.call('cp '+ book + ' ' + collectionPath,shell=True)
                #copy thumbnail
                try:
                    tpth = src / filepath / 'thumbnails' / d['cover_img']
                except:
                    tpth = ''
                if tpth and tpth.isfile() and tpth.exists():
                        cmd = 'cp ' + tpth + ' ' + thumbnailPath
                        subprocess.call(cmd,shell=True)
                else:    
                    tpth = src / filepath / 'thumbnails' / book.namebase +'.png'
                    if tpth.exists():
                       cmd = 'cp ' + tpth + ' ' + thumbnailPath
                       subprocess.call(cmd,shell=True)
                       d['cover_img'] = book.namebase + '.png'
                    else:
                       #activity icon
                       tname = str(book.name)
                       pos1 = tname.find('-')
                       if pos1 > -1:
                            tname = tname[:pos1]
                       tpth = pth / 'thumbnails' / tname + '.svg'
                       if tpth.exists():
                           cmd = 'cp ' + tpth + ' ' + thumbnailPath
                           subprocess.call(cmd,shell=True)
                           d['cover_img'] = tname + '.svg'
                       else:
                           print 'thumbnail not found', tpth
            
            bookset = Book.objects.filter(book_file=d['book_file'])
            #there should be at most one - delete all but one
            if bookset:
                for i in range(len(bookset)-1):
                    bookset[i].delete()
                book = bookset[len(bookset)-1]
                #now update
                bookkeys = d.keys()
                for bookkey in bookkeys:
                    book.bookkey = d[bookkey]
                    if bookkey == 'cover_img':
                        book.cover_img = d['cover_img']
            else:
                book = Book(**d)
            book.save()
        log.close()
    


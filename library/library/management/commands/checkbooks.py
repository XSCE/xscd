# Copyright (C) 2010, One Laptop Per Child
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
import csv
import json
from path import path
from optparse import make_option

from books.models import Book
import settings

BASE = '/media/usb0/xc-library/en'

class Command(BaseCommand):
    help = "Adds a book collection (via a CSV file)"
    args = 'Absolute path to CSV file'

    option_list = BaseCommand.option_list + (
        make_option('--json',
            action='store_true',
            dest='is_json_format',
            default=False,
            help='The file is in JSON format'),
        )

    def _handle_json(self, collection):
        """
        show books in specified collection
        
        """
        jsonpath = os.path.join(collection,'books.json')
        jsonfile = open(jsonpath)
        #data_list = json.loads(jsonfile.read())
        txt=jsonfile.read()
        jsonfile.close()
        data_list = eval(txt)
        log = open('log','w')
        temp = path(collection).namebase
        pcollection = temp.replace('collection','')
        if len(pcollection)==1:
            pcollection = pcollection + '0'
        pcollection = 'P' + pcollection
        print >> log, 'items',len(data_list), collection, pcollection
        count = 0
        for d in data_list:
            #find record in db
            count += 1
            searchkey = str(d['book_file'])
            print >> log, count, searchkey
            try:
                book = Book.objects.get(book_file=searchkey)
                #set a_collection in record
                book.a_collection=pcollection
                book.save()
            except:
                print count, searchkey, 'not found'
        log.close()
    
    def handle(self, filepath='', *args, **options):
        collection = filepath
        books = Book.objects.filter(a_collection=collection)
        print 'found', collection, len(books)



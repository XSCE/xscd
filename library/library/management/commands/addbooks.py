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
from optparse import make_option

from books.models import Book
import settings

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

    def _handle_csv(self, csvpath):
        """
        Store books from a file in CSV format.
        
        """
        
        csvfile = open(csvpath)
        dialect = csv.Sniffer().sniff(csvfile.read(1024))
        csvfile.seek(0)
        reader = csv.reader(csvfile, dialect)

        #TODO: Figure out if this is a valid CSV file

        for row in reader:
            path = row[0]
            title = row[1]
            author = row[2]
            summary =  row[3]

            f = open(path)
            book = Book(book_file = File(f), a_title = title, a_author = author, a_summary = summary)
            book.save()

    def _handle_json(self, collection):
        """
        Store books from a file in JSON format.
        
        """
        jsonpath = os.path.join(collection,'books.json')
        jsonfile = open(jsonpath)
        #data_list = json.loads(jsonfile.read())
        txt=jsonfile.read()
        jsonfile.close()
        data_list = eval(txt)
        log = open('log','w')
        print 'items',len(data_list)
        for d in data_list:
            # Get a Django File from the given path:
            pth = os.path.join(collection,d['book_file'])
            if os.path.exists(pth):
                if len(d['book_file'])>0:
                    lng = d['dc_language']
                    subprocess.call('cp '+ pth + ' ' + '/library/media/'+lng,shell=True)
                    book = Book(**d)
                else:
                    print >> log, 'book_file not found',str(d)
                    continue
            else:
                print >> log, 'path not found', pth
                continue
            book.save()
        log.close()
    
    def handle(self, filepath='', *args, **options):
        if not os.path.exists(filepath):
            raise CommandError("%r is not a valid path" % filepath)

        if options['is_json_format']:
            self._handle_json(filepath)
        else:
            self._handle_csv(filepath)



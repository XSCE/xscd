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

import sys, os, subprocess
from path import path

from books.models import Book
import settings

BASE = path('/media/usb0/xc-library')
SOURCE = path('/library/media')

#python manage.py saveCollection P01 en saves the en langauge collection P01 in
#/media/usb0/xc-library/en/P01 after erasing the existing folder, if any
#the target folder will contain the items (e.g. pdf files) and a file: books.json
#books.json contains a list of json dictionaries, one per item in the collection
#the command python manage.py loadCollection P01 en restores the collection

class Command(BaseCommand):

    def handle(self, filepath='', *args, **options):
        language = sys.argv[2]
        collection = sys.argv[3]
        log = open('log','w')
        print >> log, language, collection
        basepath = BASE /language
        filepath = basepath / collection
        #check that usb drive is mounted
        if not basepath.exists():
            raise CommandError("%r is not a valid path" % basepath)
        #clear previous collection
        subprocess.call('rm -rf ' + filepath, shell=True)
        subprocess.call('mkdir ' + filepath, shell=True)
        #add items in library to collection on usb drive
        items = Book.objects.filter(a_collection=collection).values()
        print >> log, 'items', len(items)
        jsons = []
        for item in items:
            jsons.append(item)
            src = SOURCE / language / item['book_file']
            cmd = 'cp ' + src + ' ' + filepath
            print >> log, cmd
            subprocess.call(cmd,shell=True)
        print filepath, len(items), 'items',len(jsons),'jsons'
        fout = open(filepath / 'books.json','w')
        fout.write(str(jsons))
        fout.close()
        log.close()

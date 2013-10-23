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

from kls.models import PNR
import schoolsite.settings

from path import path

class Command(BaseCommand):
    help = "Adds a person to roster (via a CSV file)"
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
        Store pnr from a file in CSV format.        
        """
        records = PNR.objects.values()
        print 'PNR has',len(records),'records'
                
        csvfile = open(csvpath,'r')
        txt = csvfile.read()
        csvfile.close()
        #fields are last, first, xo-id
        lines = txt.split('\n')
        role = path(csv).namebase[:2]
        if role == 'st':
            role = 'staff'
        records = PNR.objects.filter(role=role)
        for record in records:
            record.delete()
        for line in lines:
            row = line.split(',')
            if len(row)<3:
                print 'bad line', len(row), line
                continue
            last = row[0].strip()
            first = row[1].strip()
            xo = row[2]
            pnr = PNR(\
                      last = last, \
                      first = first,\
                      role = role,\
                      xo = xo)                      
            pnr.save()

	records = PNR.objects.values()
        print 'PNR now has',len(records),'records'


    def handle(self, filepath='', *args, **options):
        if not os.path.exists(filepath):
            raise CommandError("%r is not a valid path" % filepath)

        self._handle_csv(filepath)



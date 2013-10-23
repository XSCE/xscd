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

import os, sys, subprocess
import csv
import json
from optparse import make_option

from kls.models import XO
import schoolsite.settings

class Command(BaseCommand):
    help = "Loads xo id and serial-numbers"
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
        Store xo_id from a file in CSV format.
        
        """

        records = XO.objects.all().order_by('xo_id')
        print 'XO has',len(records),'records'
        for record in records:
            record.delete()
	records = XO.objects.all().order_by('xo_id')
        print 'XO has',len(records),'records'                
        csvfile = open(csvpath,'r')
        txt = csvfile.read()
        csvfile.close()
        #each line has a two fields: the id number (e.g. 1) and the serial-number
        #serial-number may be last three digits where form is SHC13100000
        #e.g. 1 = SHC13100001 
        #if serial-number is 11 characters, it is complete number
        #convert xo_id to 'ESJ/03/02/000' where final 000 is the number converted to three-character string
        lines = txt.split('\n')
        for line in lines:
            if not line:
                continue
            row = line.split(',')
            xo_id = row[0]
            serial = row[1]
            xo = XO()
            xo.xo_id = xo_id
            xo.serial_number = serial
            try:
                xo.save()
            except:
                print 'error saving record', xo_id, serial,sys.exc_info()[:2]

        records = XO.objects.all().order_by('xo_id')
        print 'XO now has',len(records),'records'


    def handle(self, filepath='', *args, **options):
        if not os.path.exists(filepath):
            raise CommandError("%r is not a valid path" % filepath)

        self._handle_csv(filepath)



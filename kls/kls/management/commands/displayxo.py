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
    help = "displays xo id and serial-numbers"
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

        count = 0
        for record in records:
            count += 1
            xo_id = record.xo_id
            serial_number = record.serial_number
            print count,xo_id,serial_number
                
    def handle(self, filepath='', *args, **options):

        self._handle_csv(filepath)



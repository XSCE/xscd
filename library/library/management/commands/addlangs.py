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

from books.models import Language
import settings

class Command(BaseCommand):
    help = "Adds languages from json file"
    args = 'Absolute path to json file'

    def handle(self, filepath='', *args, **options):
        langs=[{'code':'en','label':'English'},{'code':'es','label':'Spanish'},{'code':'fr','label':'French'}]
        for d in langs:
            language = Language(**d)
            language.save()


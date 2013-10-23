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
from optparse import OptionParser

from kls.models import PNR, XO
import schoolsite.settings

from path import path

base = path('/library/users/')

class Command(BaseCommand):
    help = "Sets .profile folder in /library/users"
    args = 'Role to display: staff, p4, p5, or p6'


    def handle(self, filepath, *args, **options):

        parser = OptionParser(usage="Usage: %prog [options] role")
        (options, args) = parser.parse_args()

        #query for records matching args
        records = PNR.objects.all().order_by('student_id')

        #get registered users
        fin = open('/etc/passwd','r')
        passwds = fin.read()
        fin.close()

        for record in records:
            xo = record.xo
            if not xo:
                continue
            role = record.role
            #find serial-number of xo
            try:
                xo_record = XO.objects.get(xo_id=xo)
            except:
                print 'serial_number not found', xo, role
                continue
            #check if registered
            serial_number = xo_record.serial_number
            if not serial_number in passwds:
                continue
            pth = base / serial_number 
            cmd = 'mkdir -p ' +  pth / '.profile'
            subprocess.call(cmd,shell=True)
            cmd = 'mkdir -p ' + pth / 'journal'
            subprocess.call(cmd,shell=True)
            cmd = 'mkdir -p ' + pth / 'log'
            subprocess.call(cmd,shell=True)
            cmd = 'mkdir -p ' + pth / 'session'
            subprocess.call(cmd,shell=True)
            fout = open(pth / '.profile/profile','w')
            fout.write("{'role':'"+role+"'}")
            fout.close()
            cmd = 'chown '+serial_number+':'+serial_number + ' ' +pth / 'log'
            subprocess.call(cmd,shell=True)
            cmd = 'chown '+serial_number+':'+serial_number + ' ' +pth / 'journal'
            subprocess.call(cmd,shell=True)
            cmd = 'chown -R '+serial_number+':'+serial_number + ' ' + pth / '.profile'
            subprocess.call(cmd,shell=True)
         
            
            


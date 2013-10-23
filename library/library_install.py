#!/usr/bin/python

from path import path

#install app in settings.py
BASE = path('/library/schoolsite/schoolsite')
SETTINGS = BASE / 'settings.py'
URLS = BASE / 'urls.py'
fin = open(SETTINGS,'r')
txt = fin.read()
fin.close()
lines = txt.split('\n')
txtout = ''
if not 'library' in txt:
    for line in lines:
        txtout += line + '\n'
        if 'django.contrib.admin' in line:
            txtout += "    'library',\n"
    fout = open(SETTINGS,'w')
    fout.write(txtout)
    fout.close()
#install urls in urls.py
fin = open(URLS,'r')
txt = fin.read()
fin.close()
lines = txt.split('\n')
txtout = ''
for line in lines:
    if '#admin'	in line:
        txtout+="\n    # Book list:\n"
        txtout+="    (r'^library/$', 'library.books.views.library_main'),\n"
        txtout+="    (r'^library/topic/(\w+)/$', 'library.books.views.library_topic'),\n"
        txtout+="    (r'^library/list/(\w+)/(\d+)/$', 'library.books.views.library_book_list'),\n"
        txtout+="    (r'^library/detail/(\d+)/$', 'library.books.views.library_book_detail'),\n"
    txtout += line + '\n'
    if 'library' in line:
        continue
fout = open(URLS,'w')
fout.write(txtout)
fout.close()


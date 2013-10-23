#!/usr/bin/python

#install app in settings.py
fin = open('/library/schoolsite/schoolsite/settings.py','r')
txt = fin.read()
fin.close()
lines = txt.split('\n')
txtout = ''
if not 'kls' in txt:
    for line in lines:
        txtout += line + '\n'
        if 'django.contrib.admin' in line:
       	    txtout += "    'kls',\n"
    fout = open('/library/schoolsite/schoolsite/settings.py','w')
    fout.write(txtout)
    fout.close()
#install urls in urls.py
fin = open('/library/schoolsite/schoolsite/urls.py','r')
txt = fin.read()
fin.close()
lines = txt.split('\n')
txtout = ''
for line in lines:
    if '#admin'	in line:
        txtout+="\n    # Kls application:\n"
        txtout+="    (r'^kls/school/grade/(\w+)/$','kls.school.views.classlist'),\n"
        txtout+="    (r'^kls/school/log/(\w+)/$','kls.school.views.logview'),\n"
        txtout+="    (r'^kls/school/me/(\w+)/$','kls.school.views.studentview'),\n"
        txtout+="    (r'^kls/school/time/$','kls.school.views.time'),\n"
    if 'kls' in line:
        continue
    txtout += line + '\n'
fout = open('/library/schoolsite/schoolsite/urls.py','w')
fout.write(txtout)
fout.close()


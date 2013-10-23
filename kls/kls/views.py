from django.http import HttpResponse
import subprocess
from subprocess import PIPE
from path import path

def time(request):
    cmd = 'date --rfc-3339="seconds"'
    pid = subprocess.Popen(cmd,stdout=PIPE,stderr=PIPE,shell=True)
    (result,err) = pid.communicate()
    if result:
        return HttpResponse(result)
    elif err:
        return HttpResponse(err)
    else:
        return HttpResponse('oops!')

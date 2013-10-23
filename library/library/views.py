# Copyright (C) 2010, One Laptop Per Child
# Copyright (C) 2010, Kushal Das
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

import os
from path import path

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.views.generic.simple import redirect_to
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, update_object, \
  delete_object
from django.template import RequestContext

from django.conf import settings

from search import simple_search, advanced_search
from forms import BookForm, AddLanguageForm
from langlist import langs as LANG_CHOICES
from models import *
from popuphandler import handlePopAdd

collection_titles = {
      'p01':'English Literature',
      'p02':"English Children's Literature",
      'p03':'Inspirational Art',
      'p04':'Do It Yourself Art',
      'p05':'Traditional Art',
      'p06':'English Course Materials',
      'p07':'Economics Course Materials',
      'p08':'Mathematics CM',
      'p09':'Science CM',
      'p10':'Environmental Studies CM',
      'p11':'Sociology CM',
      'p12':'Political Science and Philosophy CM',
      'p13':'Governmant Reference Materials',
      'p14':'Other Agriculture and Biodiversity',
      'p15':'Other Law and Government',
      'p16':'Other History and Culture',
      'p17':'Other Science and Technology',
      'p18':'Other Environment-related',
      'p19':'Other Health and Security-related',
      'p20':'Other Civics-related',
      'p21':'Other Education-related',
      'p22':'Other Videos',
      'p23':'Other Photo Essay',
      'p24':'Educatonal Theory and Practice for Teachers',
      'p25':'Reading Material for Teachers',
      'p26':'Support for Teachers',
      'p27':'Training for Teachers',
      'p28':'Professional Development for Teachers',
      'a01':'Sugar Activities',
      'm01':'Maps',
      'b01':'Fun with English',
      'b02':'Language Games',
      'b03':'Play with Friends',
      'b04':'Short Stories',
      'b05':'Songs',
      'amhist':'The amhist',
      'cbs':'The cbs',
      'history':'The history',
      'royrogers':'The royrogers',
      'annie':'The annie',
      'cbsradioworkshop':'The cbsradioworkshop',
      'JB':'The JB',
      'shakespeare':'The shakespeare',
      'believeitornot':'The believeitornot',
      'CoA':'The CoA',
      'jubilee':'The jubilee',
      'sherlockholmes':'The sherlockholmes',
      'belltelephone':'The belltelephone',
      'columbia_works':'The columbia_works',
      'keen':'The keen',
      'sixshooter':'The sixshooter',
      'bennygoodman':'The bennygoodman',
      'crosbyclooney':'The crosbyclooney',
      'lespaul':'The lespaul',
      'Sousa':'The Sousa',
      'bergenmccarthy':'The bergenmccarthy',
      'dragnet':'The dragnet',
      'lone_ranger':'The lone_ranger',
      'spike_jones':'The spike_jones',
      'bigband':'The bigband',
      'elvispresley':'The elvispresley',
      'melodyranch':'The melodyranch',
      'suspense':'The suspense',
      'bigjon':'The bigjon',
      'enchantedhour':'The enchantedhour',
      'MercurySummerTheatre':'The MercurySummerTheatre',
      'tomcorbett':'The tomcorbett',
      'bigshow':'The bigshow',
      'flashgordon':'The flashgordon',
      'mickeymouse':'The mickeymouse',
      'victorborge':'The victorborge',
      'billymills':'The billymills',
      'gangbusters':'The gangbusters',
      'misc':'The misc',
      'YouAreThere':'The YouAreThere',
      'bobcrosby':'The bobcrosby',
      'gerswhin':'The gerswhin',
      'nbc':'The nbc',
      'YourHitParade':'The YourHitParade',
      'bobhope':'The bobhope',
      'glennmiller':'The glennmiller',
      'ourmissbrooks':'The ourmissbrooks',
      'yukon':'The yukon',
      'britten':'The britten',
      'gunsmoke':'The gunsmoke',
      'pollparrot':'The pollparrot',
      'burnsallen':'The burnsallen',
      'hearitnow':'The hearitnow',
      'pretend':'The pretend',
}

collections = {
      'Topic1':[{'id':'p01','title':'English Literature'}],
      'Topic2':[{'id':'p02','title':"English Children's Literature"}],
      'Topic4':[{'id':'p03','title':'Inspirational Art'},
                {'id':'p04','title':'Do It Yourself Art'},
                {'id':'p05','title':'Traditional Art'}],
      'Topic3':[{'id':'p06','title':'English Course Materials'},
                {'id':'p07','title':'Economics Course Materials'},
                {'id':'p08','title':'Mathematics CM'},
                {'id':'p09','title':'Science CM'},
                {'id':'p10','title':'Environmental Studies CM'},
                {'id':'p11','title':'Sociology CM'},
                {'id':'p12','title':'Political Science and Philosophy CM'},
                {'id':'p13','title':'Governmant Reference Materials'},
                {'id':'p14','title':'Other Agriculture and Biodiversity'},
                {'id':'p15','title':'Other Law and Government'},
                {'id':'p16','title':'Other History and Culture'},
                {'id':'p17','title':'Other Science and Technology'},
                {'id':'p18','title':'Other Environment-related'},
                {'id':'p19','title':'Other Health and Security-related'},
                {'id':'p20','title':'Other Civics-related'},
                {'id':'p21','title':'Other Education-related'},
                {'id':'p22','title':'Other Videos'},
                {'id':'p23','title':'Other Photo Essay'},
                {'id':'p24','title':'Educatonal Theory and Practice for Teachers'},
                {'id':'p25','title':'Reading Material for Teachers'},
                {'id':'p26','title':'Support for Teachers'},
                {'id':'p27','title':'Training for Teachers'},
                {'id':'p28','title':'Professional Development for Teachers'}
               ],
      'Topic5':[{'id':'a01','title':'Sugar Activities'}],
      'Topic6':[{'id':'m01','title':'Maps'}],
      'Topic7':[
                {'id':'b01','title':'Fun with English'},
                {'id':'b02','title':'Language Games'},
                {'id':'b03','title':'Play with Friends'},
                {'id':'b04','title':'Short Stories'},
                {'id':'b05','title':'Songs'},
               ],
       'Topic8':[
                {'id':'amhist','title':'American History'},
                {'id':'cbs','title':'The CBS Show'},
                {'id':'history','title':'History'},
                {'id':'royrogers','title':'The Roy Rogers Show'},
                {'id':'annie','title':'Little Orphan Annie'},
                {'id':'cbsradioworkshop','title':'The CBS Radio Workshop'},
                {'id':'JB','title':'The Jack Benny Show'},
                {'id':'shakespeare','title':'Shakespeare'},
                {'id':'believeitornot','title':"Riply's Believe It or Not"},
                {'id':'CoA','title':'The Cavalcade of America'},
                {'id':'jubilee','title':'Jubilee'},
                {'id':'sherlockholmes','title':'Sherlock Holmes'},
                {'id':'belltelephone','title':'The Bell Telephone Hour'},
                {'id':'columbia_works','title':'The Columbia_Workshop'},
                {'id':'keen','title':'Mr. Keen, Tracer of Lost Persons'},
                {'id':'sixshooter','title':'The Sixshooter'},
                {'id':'bergenmccarthy','title':'The Edgar Bergen and Charlie McCarthy'},
                {'id':'dragnet','title':'Dragnet'},
                {'id':'lone_ranger','title':'The Lone Ranger'},
                {'id':'suspense','title':'Suspense'},
                {'id':'bigjon','title':'Big Jon'},
                {'id':'MercurySummerTheatre','title':'The Mercury Summer Theatre'},
                {'id':'tomcorbett','title':'Tom Corbett Space Cadet'},
                {'id':'bigshow','title':'The Big Show'},
                {'id':'flashgordon','title':'Flash Gordon'},
                {'id':'mickeymouse','title':'Mickey Mouse'},
                {'id':'gangbusters','title':'Gangbusters'},
                {'id':'YouAreThere','title':'You Are There'},
                {'id':'nbc','title':'The NBC Show'},
                {'id':'bobhope','title':'Bob Hope'},
                {'id':'ourmissbrooks','title':'Our Miss Brooks'},
                {'id':'yukon','title':'Yukon'},
                {'id':'gunsmoke','title':'Gunsmoke'},
                {'id':'pollparrot','title':'Poll Parrot'},
                {'id':'burnsallen','title':'George Burns and Gracie Allen'},
                {'id':'hearitnow','title':'Hear It Now with Edward R. Murrow'},
                {'id':'pretend','title':"Let's Pretend"},
               ],
       'Topic9':[
                {'id':'enchantedhour','title':'The Enchanted Hour'},
                {'id':'bennygoodman','title':'The Benny Goodman Show'},
                {'id':'crosbyclooney','title':'Bob Crosby and Mary Clooney'},
                {'id':'lespaul','title':'Les Paul'},
                {'id':'Sousa','title':'John Phillip Sousa'},
                {'id':'spike_jones','title':'The Spike Jones Show'},
                {'id':'bigband','title':'The Big Band Show'},
                {'id':'elvispresley','title':'Elvis Presley'},
                {'id':'melodyranch','title':'Melody Ranch'},
                {'id':'victorborge','title':'Victor Borge'},
                {'id':'billymills','title':'The Billy Mills Show'},
                {'id':'bobcrosby','title':'Bob Crosby'},
                {'id':'gerswhin','title':'Gerswhin'},
                {'id':'YourHitParade','title':'Your Hit Parade'},
                {'id':'glennmiller','title':'Glenn Miller'},
                {'id':'britten','title':"Benjamin Britten, Young People's Guide to the Orchestra"},
                {'id':'misc','title':'Misc'},
               ],
}

def library_main(request,qtype=None):
    extra_context={}
    extra_context['title']='Library'
    extra_context['topic_list']=[
        {'topic':'Topic2','class':'c11','title':'Juvenile Fiction','image':'Litchar.png','collection':'p02'},
       	{'topic':'Topic4','class':'c21','title':'Juvenile Non-fiction','image':'Childbook.png','collection':'list'},
       	{'topic':'Topic1','class':'c13','title':'Adult Fiction','image':'fiction.jpg','collection':'p01'},
       	{'topic':'Topic7','class':'c12','title':'Learn English','image':'bc.png','collection':'list'},
       	{'topic':'Topic3','class':'c23','title':'Adult Non-fiction','image':'reading_books.png','collection':'list'},
       	{'topic':'Topic5','class':'c22','title':'Sugar Activities','image':'logo-add-ons-half.png','collection':'a01'},
       	{'topic':'Topic6','class':'c33','title':'Maps','image':'map_icon.png','collection':'m01'},
        {'topic':'Topic8','class':'c31','title':'Old Time Radio','image':'otr.png','collection':'list'},
        {'topic':'Topic9','class':'c32','title':'Classical Music','image':'bach.png','collection':'list'},
    ]
    return render_to_response('bookMain.html',extra_context,RequestContext(request))

def library_topic(request,topic_id):
    extra_context = {}
    extra_context['topic'] = collections[str(topic_id)]
    if len(collections[str(topic_id)])>1:
        extra_context['type'] = 'topic'
    else: 
        extra_context['type'] = 'list' 
    return render_to_response('bookTopic.html',extra_context,RequestContext(request))

def library_book_list(request, collection_id, page):
    queryset = Book.objects.filter(a_collection=collection_id).order_by('a_title').values()
    pageset = []
    pageno = int(page)
    min = pageno * 9
    max = min + 8
    lastpage = (len(queryset) / 9)+1;
    title = collection_titles[collection_id]
    for i in range(len(queryset)):
        if i >= min and i <= max:
            item = queryset[i]
            img = queryset[i]['cover_img']
            item['img']=str(img).replace('.svg','.png')
            pageset.append(item)
    extra_context = {
        'book_list': pageset,
        'collection_id':collection_id.lower(),
        'collection_title':title,
        'min':min,
        'max':max,
        'lastpage':lastpage,
        'pageno':pageno,
        'total_books': len(queryset),
    }
    return render_to_response(
        'bookList.html',
        extra_context,
        context_instance = RequestContext(request),
    )

def library_book_detail(request, book_id):
    book = Book.objects.get(id=book_id)
    language = path(book.dc_language)
    collection = path(book.a_collection)
    cover_img = path(book.cover_img)
    extra_context={
      'book':book,
      'thumbnail':cover_img,
      'thumbnailPath':'http://schoolserver/static/media/' + tpth
    }
    return render_to_response(
        'bookDetail.html',
        extra_context,
        context_instance = RequestContext(request),
    )


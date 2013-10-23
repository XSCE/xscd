
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

from django.db import models

from uuidfield import UUIDField
from langlist import langs

class Language(models.Model):
    label = models.CharField('language name', max_length=50, blank=False, unique=True)
    code = models.CharField(max_length=4, blank=True)

    def __unicode__(self):
        return self.label

    def save(self, *args, **kwargs):
        '''
        This method automatically tries to assign the right language code
        to the specified language. If a code cannot be found, it assigns
        'xx'
        '''
        code = 'xx'
        for lang in langs:
            if self.label.lower() == lang[1].lower():
                code = lang[0]
                break
        self.code = code
        super(Language, self).save(*args, **kwargs)


class Book(models.Model):
    """
    This model stores the book file, and all the metadata that is
    needed to publish it in a OPDS atom feed.
    
    It also stores other information, like tags and downloads, so the
    book can be listed in OPDS catalogs.
    
    """
    book_file = models.FileField(upload_to='books')
    time_added = models.DateTimeField(auto_now_add=True)
    tags = models.CharField(max_length=200)
    downloads = models.IntegerField(default=0)
    a_id = UUIDField('atom:id')
    a_title = models.CharField('atom:title', max_length=200)
    a_author = models.CharField('atom:author', max_length=200)
    a_updated = models.DateTimeField('atom:updated', auto_now=True)
    a_summary = models.TextField('atom:summary', blank=True)
    COLLECTION_CHOICES = (
      (u'P01',u'English Literature'),
      (u'P02',u"English Children's Literature"),
      (u'P03',u'Inspirational Art'),
      (u'P04',u'Do It Yourself Art'),
      (u'P05',u'Traditional Art'),
      (u'P06',u'English Course Materials'),
      (u'P07',u'Economics Course Materials'),
      (u'P08',u'Mathematics Course Materials'),
      (u'P09',u'Science Course Materials'),
      (u'P10',u'Environmental Studies Course Materials'),
      (u'P11',u'Sociology Course Materials'),
      (u'P12',u'Political Science and Philosophy Course Materials'),
      (u'P13',u'Government Reference Materials'),
      (u'P14',u'Other Agriculture and Biodiversity'),
      (u'P15',u'Other Law and Government'),
      (u'P16',u'Other History and Culture'),
      (u'P17',u'Other Science and Technology'),
      (u'P18',u'Other Environment-related'),
      (u'P19',u'Other Health and Security-related'),
      (u'P20',u'Other Civics-related'),
      (u'P21',u'Other Education-related'),
      (u'P22',u'Other Videos'),
      (u'P23',u'Other Photo Essay'),
      (u'P24',u'Educational Theory and Practice for Teachers'),
      (u'p25',u'Reading Material for Teachers'),
      (u'P26',u'Support for Teachers'),
      (u'P27',u'Training for Teachers'),
      (u'P28',u'Professional Development for Teachers'),
      (u'A01',u'Sugar Activities'),      
    )
    a_collection = models.CharField(max_length=3, choices= COLLECTION_CHOICES)
    a_category = models.CharField('atom:category', max_length=200, blank=True)
    a_rights = models.CharField('atom:rights', max_length=200, blank=True)
    LANGUAGE_CHOICES = (
        (u'en', u'English'),
        (u'es', u'Spanish'),
        (u'fr', u'French'),
        (u'xo', u'Sugar Activity'),
    )
    dc_language = models.CharField(max_length=4, choices = LANGUAGE_CHOICES)
    dc_publisher = models.CharField('dc:publisher', max_length=200, blank=True)
    dc_issued = models.CharField('dc:issued', max_length=100, blank=True)
    dc_identifier = models.CharField('dc:identifier', max_length=50, \
        help_text='Use ISBN for this', blank=True)
    cover_img = models.FileField(blank=True, upload_to='covers')
    mime_type = models.CharField(max_length = 200, blank=True)
    
    class Meta:
        ordering = ('-time_added',)
        get_latest_by = "time_added"
    
    def __unicode__(self):
        return self.a_title
    
    @models.permalink
    def get_absolute_url(self):
        return ('pathagar.books.views.book_detail', [self.pk])

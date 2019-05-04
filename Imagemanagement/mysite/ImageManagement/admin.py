# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from . import models



admin.site.register(models.User)
admin.site.register(models.Acquisition)
admin.site.register(models.Image)
admin.site.register(models.ImageOptional)
admin.site.register(models.AcqOptional)


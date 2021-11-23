from django.contrib import admin

from .models import News, Feed, SourceForParse


admin.site.register(News)
admin.site.register(Feed)
admin.site.register(SourceForParse)

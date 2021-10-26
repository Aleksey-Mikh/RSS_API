from django.db import models


class News(models.Model):
    channel_title = models.ForeignKey(
        "Feed", verbose_name="Channel title", on_delete=models.PROTECT, related_name="news"
    )
    title = models.CharField(max_length=200, verbose_name="Title")
    date = models.TimeField(verbose_name="Publication date")
    link = models.URLField(max_length=200, verbose_name="Link")
    author = models.CharField(max_length=200, verbose_name="Author")
    category = models.CharField(max_length=255, verbose_name="Category")
    description = models.CharField(max_length=255, verbose_name="Description")
    more_description = models.TextField(verbose_name="More description", blank=True)
    comments = models.CharField(max_length=255, verbose_name="Comments", blank=True)
    media_objects = models.TextField(verbose_name="Media Object", blank=True)
    extra_links = models.TextField(verbose_name="Extra_links", blank=True)
    source_feed = models.TextField(verbose_name="Source", blank=True)


class Feed(models.Model):
    channel_title = models.CharField(max_length=255, verbose_name="Channel title")
    source = models.URLField(max_length=200, verbose_name="Feed source")


class SourceForParse(models.Model):
    source_for_parse = models.URLField(max_length=200, verbose_name="Source for parse")


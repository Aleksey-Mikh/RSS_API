from django.db import models


class News(models.Model):
    channel_title = models.ForeignKey(
        "Feed", verbose_name="Channel title", on_delete=models.PROTECT, related_name="news"
    )
    title = models.CharField(max_length=200, verbose_name="Title")
    pub_date = models.DateField(verbose_name="Publication date")
    link = models.URLField(max_length=200, verbose_name="Link")
    author = models.CharField(max_length=200, verbose_name="Author", blank=True, null=True)
    category = models.CharField(max_length=255, verbose_name="Category", blank=True, null=True)
    description = models.CharField(max_length=255, verbose_name="Description", blank=True, null=True)
    more_description = models.TextField(verbose_name="More description", blank=True, null=True)
    comments = models.CharField(max_length=255, verbose_name="Comments", blank=True, null=True)
    media_objects = models.TextField(verbose_name="Media Object", blank=True, null=True)
    extra_links = models.TextField(verbose_name="Extra_links", blank=True, null=True)
    source_feed = models.TextField(verbose_name="Source", blank=True, null=True)

    def __str__(self):
        return f"{self.title}, {self.pub_date}"

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"


class Feed(models.Model):
    channel_title = models.CharField(max_length=255, verbose_name="Channel title")
    source = models.URLField(max_length=200, verbose_name="Feed source")

    def __str__(self):
        return f"{self.channel_title}, {self.source}"

    class Meta:
        verbose_name = "Feed"
        verbose_name_plural = "Feeds"


class SourceForParse(models.Model):
    source_for_parse = models.URLField(max_length=200, verbose_name="Source for parse")

    def __str__(self):
        return self.source_for_parse

    class Meta:
        verbose_name = "Source for parse"
        verbose_name_plural = "Sources for parse"


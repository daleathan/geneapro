from django.db import models
from django.conf import settings
from .base import GeneaProveModel
from .source import Source


class Representation(GeneaProveModel):
    """
    Contains the representation of a source in a variete of formats.
    A given source can have multiple representations
    """

    mime_type = models.CharField(max_length=40)
    source = models.ForeignKey(Source, related_name="representations")
    file = models.TextField()
    comments = models.TextField(null=True)

    class Meta:
        """Meta data for the model"""
        db_table = "representation"

    def url(self):
        """
        :return: a string
           The URL that should be used to access the media on the disk,
           from a web browser.
        """
        return '/repr/%s' % (self.id, )
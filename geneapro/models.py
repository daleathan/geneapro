from django.db import models

class Place_Part_Type (models.Model):
    name        = models.CharField (
        'Type name', max_length=100, blank=False,null=False)

    def __unicode__ (self):
        return self.name

class Place (models.Model):
    date = models.CharField (
        'date of existence', max_length=200, null=True, blank=True)
    date_sort = models.DateTimeField (
        'date used when sorting', null=True, blank=True)
    parentPlace = models.ForeignKey ('self', blank=True, null=True,
        help_text = "The parent place, that contains this one")

    def __unicode__ (self):
        parts = self.place_part_set.all ()
        name = ",".join ([p.name for p in parts]) + " " + str (self.date)
        if self.parentPlace:
            return str (self.parentPlace) + name
        else:
            return name

class Place_Part (models.Model):
    # ??? How do we know where the place_part was found (ie for instance an
    # alternate name for the place found in a different document ?)
    # ??? Should the existence date be a place_part as well, or a field in
    # a place part, so that the same place with different names results in
    # a single id
    place       = models.ForeignKey (Place)
    type        = models.ForeignKey (Place_Part_Type)
    name        = models.CharField (max_length=200)
    sequence_number = models.PositiveSmallIntegerField (
       "Sequence number", default=1)

    class Meta:
        order_with_respect_to = 'place'
        ordering = ('sequence_number', 'name')

    def __unicode__ (self):
        return str (self.type) + "=" + self.name
 
# from mysites.geneapro.models import *
# p = Place ()
# p.place_part_set.create (type="0", name="France")
# p.place_part_set.create (type=Place_Part_Type.objects.get(pk=1), name="France")

# from django.db import connection
# connection.queries

"""
Event-related views
"""

from django.http import HttpResponse
from geneaprove import models
from ..sql import AssertList
from geneaprove.views.to_json import JSONView


def extended_events(ids):
    """Return a dict of Event instances, augmented with the following fields:
        - "p2e": a list of instances of P2E for this event
    """

    return events


class EventDetailsView(JSONView):
    def get_json(self, params, id):
        """JSON data for a specific event"""

        asserts = AssertList(models.P2E.objects.filter(event_id=id))
        return {
            "id": id,
            **asserts.to_json()
        }

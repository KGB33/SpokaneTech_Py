from datetime import timedelta

import freezegun

from django.test import TestCase
from django.utils import timezone

from web import models, services


class SimpleSender(services.Sender):

    def __init__(self, expected: str) -> None:
        self.expected = expected

    def send(self, message: str, **kwargs) -> None:
        assert message == self.expected


class TestSendEventsToDiscord(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()

    @freezegun.freeze_time("2024-03-18")
    def test_send_events(self):
        today = timezone.localtime()

        group = models.TechGroup.objects.create(name="Spokane Python User Group")
        models.Event.objects.create(
            name="Intro to Python",
            date_time = today + timedelta(days=1),
            url="https://spokanepython.com/meetups/intro-to-python/",
            group=group,
        )
        event2 = models.Event.objects.create(
            name="Advanced Python",
            date_time = today + timedelta(days=2, hours=18),
            group=group,
        )
        models.Event.objects.create(
            name="Way in the future event",
            date_time = today + timedelta(days=7),
            group=group,
        )

        expected = f"""_Here are the upcoming Spokane Tech events for this week:_

**Tuesday, Mar 19 @ 12:00 AM**
Spokane Python User Group — [Intro to Python](<https://spokanepython.com/meetups/intro-to-python/>)

**Wednesday, Mar 20 @ 6:00 PM**
Spokane Python User Group — [Advanced Python](<https://spokanetech.org/events/{event2.pk}>)

"""
        sender = SimpleSender(expected)
        service = services.DiscordService(sender)
        service.send_events()

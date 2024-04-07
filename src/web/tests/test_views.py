from datetime import datetime

import freezegun
import pytest
from bs4 import BeautifulSoup
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from django.utils import timezone
from model_bakery import baker
from web.models import TechGroup


@pytest.mark.django_db
def test_list_tech_groups(client: Client):
    # Arrange
    tech_group = TechGroup(
        name="List Tech Groups Test",
        description="List Tech Groups Test",
        enabled=True,
        homepage="https://spokanetech.org/",
    )
    tech_group.save()

    # Act
    url = reverse("web:list_tech_groups")
    response = client.get(url)

    # Assert
    assert response.status_code == 200
    assert response.context["queryset"].get().pk == tech_group.pk


@pytest.mark.django_db
def test_get_tech_group(client: Client):
    # Arrange
    tech_group = TechGroup(
        name="Get Tech Groups Test",
        description="Get Tech Groups Test",
        enabled=True,
        homepage="https://spokanetech.org/",
    )
    tech_group.save()

    # Act
    url = reverse("web:get_tech_group", args=[tech_group.pk])
    response = client.get(url)

    # Assert
    assert response.status_code == 200
    assert response.context["object"].pk == tech_group.pk


@freezegun.freeze_time("2024-03-17")
@pytest.mark.django_db
def test_set_timezone_and_timezone_middleware(client: Client):
    # Arrange
    date_time = datetime.fromisoformat("2024-03-19T01:00:00Z")
    baker.make("web.Event", date_time=date_time)

    # Act
    client.post(reverse("web:set_timezone"), {"timezone": "America/Los_Angeles"})
    response = client.get(reverse("web:events"))

    # Assert
    soup = BeautifulSoup(response.content, "lxml")
    date_time_tag = soup.find(attrs={"data-testid": "date_time"})
    assert date_time_tag is not None
    actual = date_time_tag.text.strip()
    assert actual == "Monday, March 18, 2024 at 6:00 PM"


class TestEventDetailModal(TestCase):
    """test GetEventDetailsModal view"""

    def setUp(self):
        super(TestEventDetailModal, self).setUp()
        self.object = baker.make("web.Event")
        self.headers = dict(HTTP_HX_REQUEST="true")
        self.referrer = reverse("web:index")
        self.url = reverse("web:get_event_details", kwargs={"pk": self.object.pk})

    @pytest.mark.django_db
    def test_get(self):
        """verify modal content can be rendered"""
        response = self.client.get(self.url, HTTP_REFERER=self.referrer, **self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "web/partials/modal/detail_event.htm")

    @pytest.mark.django_db
    def test_non_htmx_call(self):
        """verify 400 response if non-htmx request is used"""
        response = self.client.get(self.url, HTTP_REFERER=self.referrer)
        self.assertEqual(response.status_code, 400)


class TestEventCalendarView(TestCase):
    """test EventCalendarView view"""

    def setUp(self):
        super(TestEventCalendarView, self).setUp()
        self.object = baker.make("web.Event")
        self.headers = dict(HTTP_HX_REQUEST="true")
        self.referrer = reverse("web:index")
        self.now = timezone.now()
        self.url = reverse("web:event_calendar", kwargs={"year": self.now.year, "month": self.now.month})

    @pytest.mark.django_db
    def test_get(self):
        """verify page content can be rendered"""
        response = self.client.get(self.url, HTTP_REFERER=self.referrer, **self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "handyhelpers/partials/calendar.htm")
        self.assertIn(self.object.name, response.content.decode("utf-8"))
        self.assertIn(f"/events/{self.object.pk}/details", response.content.decode("utf-8"))

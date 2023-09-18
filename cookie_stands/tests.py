from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import CookieStand


class ThingFrontTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="tester", email="tester@email.com", password="pass"
        )

        self.cookie_stand = CookieStand.objects.create(
            name="pickle", rating=1, reviewer=self.user, description="pickle description"
        )

    def test_string_representation(self):
        self.assertEqual(str(self.cookie_stand), "pickle")

    def test_thing_content(self):
        self.assertEqual(f"{self.cookie_stand.name}", "pickle")
        self.assertEqual(f"{self.cookie_stand.reviewer}", "tester")
        self.assertEqual(self.cookie_stand.rating, 1)

    def test_list_page_status_code(self):
        self.client.login(username="tester", password="pass")  # need to log in
        url = reverse('thing_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_list_page_template(self):
        self.client.login(username="tester", password="pass")  # need to log in
        url = reverse('thing_list')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'cookie_stands/thing_list.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_list_page_context(self):
        self.client.login(username="tester", password="pass")  # need to log in
        url = reverse('thing_list')
        response = self.client.get(url)
        cookie_stands = response.context['object_list']
        self.assertEqual(len(cookie_stands), 1)
        self.assertEqual(cookie_stands[0].name, "pickle")
        self.assertEqual(cookie_stands[0].rating, 1)
        self.assertEqual(cookie_stands[0].reviewer.username, "tester")

    def test_detail_page_status_code(self):
        self.client.login(username="tester", password="pass")  # need to log in
        url = reverse('thing_detail', args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail_page_template(self):
        self.client.login(username="tester", password="pass")  # need to log in
        url = reverse('thing_detail', args=(1,))
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'cookie_stands/thing_detail.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_detail_page_context(self):
        self.client.login(username="tester", password="pass")  # need to log in
        url = reverse('thing_detail', args=(1,))
        response = self.client.get(url)
        cookie_stand = response.context['cookie_stand']
        self.assertEqual(cookie_stand.name, "pickle")
        self.assertEqual(cookie_stand.rating, 1)
        self.assertEqual(cookie_stand.reviewer.username, "tester")


class ThingApiTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        testuser1 = get_user_model().objects.create_user(
            username="testuser1", password="pass"
        )
        testuser1.save()

        test_thing = CookieStand.objects.create(
            name="rake",
            reviewer=testuser1,
            description="Better for collecting leaves than a shovel.",
        )
        test_thing.save()

    def test_things_model(self):
        cookie_stand = CookieStand.objects.get(id=1)
        actual_reviewer = str(cookie_stand.reviewer)
        actual_name = str(cookie_stand.name)
        actual_description = str(cookie_stand.description)
        self.assertEqual(actual_reviewer, "testuser1")
        self.assertEqual(actual_name, "rake")
        self.assertEqual(
            actual_description, "Better for collecting leaves than a shovel."
        )

    def test_get_thing_list(self):
        self.client.login(username="testuser1", password="pass")  # need to log in
        url = reverse("thing_list")
        response = self.client.get(url)
        # print("response context is:", response.context)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cookie_stands = response.context["cookie_stands"]
        self.assertEqual(len(cookie_stands), 1)
        # self.assertEqual(cookie_stands[0]["name"], "rake")

    # def test_get_thing_by_id(self):
    #     url = reverse("thing_detail", args=(1,))
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     cookie_stand = response.data
    #     self.assertEqual(cookie_stand["name"], "rake")
    #
    # def test_create_thing(self):
    #     url = reverse("thing_list")
    #     data = {"reviewer": 1, "name": "spoon",
    #             "description": "good for cereal and soup"}
    #     response = self.client.post(url, data)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     cookie_stands = CookieStand.objects.all()
    #     self.assertEqual(len(cookie_stands), 2)
    #     self.assertEqual(CookieStand.objects.get(id=2).name, "spoon")
    #
    # def test_update_thing(self):
    #     url = reverse("thing_detail", args=(1,))
    #     data = {
    #         "reviewer": 1,
    #         "name": "rake",
    #         "description": "pole with a crossbar toothed like a comb.",
    #     }
    #     response = self.client.put(url, data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     cookie_stand = CookieStand.objects.get(id=1)
    #     self.assertEqual(cookie_stand.name, data["name"])
    #     self.assertEqual(cookie_stand.reviewer.id, data["reviewer"])
    #     self.assertEqual(cookie_stand.description, data["description"])
    #
    # def test_delete_thing(self):
    #     url = reverse("thing_detail", args=(1,))
    #     response = self.client.delete(url)
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #     cookie_stands = CookieStand.objects.all()
    #     self.assertEqual(len(cookie_stands), 0)

import pytest
from django.urls import reverse

@pytest.mark.django_db # доступ до БД дає
def test_home_page_returns_200(client):
    response = client.get(reverse("core:home"))

    assert response.status_code == 200

@pytest.mark.django_db
def test_home_page_uses_expected_template(client):
    response = client.get(reverse("core:home"))

    template_names = [template.name for template in response.templates]

    assert "core/home.html" in template_names
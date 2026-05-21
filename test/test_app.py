import pytest
from vietnam import app


def test_home_page_loads_successfully():
    client = app.test_client()
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200


def test_home_page_shows_destinations():
    client = app.test_client()
    response = client.get("/")
    page_content = response.data.decode()

    assert "Ha Long Bay" in page_content
    assert "Hoi An" in page_content
    assert "Hanoi" in page_content
    assert "Ho Chi Minh City" in page_content


def test_search_by_destination_name_hanoi():
    client = app.test_client()
    response = client.get("/?search=hanoi")
    page_content = response.data.decode()

    assert response.status_code == 200
    assert "Hanoi" in page_content
    assert "Ha Long Bay" not in page_content


def test_search_by_description():
    client = app.test_client()
    response = client.get("/?search=limestone")
    page_content = response.data.decode()

    assert response.status_code == 200
    assert "Ha Long Bay" in page_content
    assert "Hanoi" not in page_content


def test_filter_by_duration():
    client = app.test_client()
    response = client.get("/?duration=2-3 Days")
    page_content = response.data.decode()

    assert response.status_code == 200
    assert "Ha Long Bay" in page_content
    assert "Hoi An" not in page_content
    assert "Hanoi" not in page_content


def test_search_and_duration_filter_together():
    client = app.test_client()
    response = client.get("/?search=city&duration=2-4 Days")
    page_content = response.data.decode()

    assert response.status_code == 200
    assert "Ho Chi Minh City" in page_content
    assert "Ha Long Bay" not in page_content


def test_destination_detail_page_loads_successfully():
    client = app.test_client()
    response = client.get("/destination/ha-long-bay")
    page_content = response.data.decode()

    assert response.status_code == 200
    assert "Ha Long Bay" in page_content
    assert "2-3 Days" in page_content


def test_hoi_an_destination_detail_page():
    client = app.test_client()
    response = client.get("/destination/hoi-an")
    page_content = response.data.decode()

    assert response.status_code == 200
    assert "Hoi An" in page_content
    assert "2-4 Days" in page_content


def test_search_is_case_insensitive():
    client = app.test_client()
    response = client.get("/", query_string={"search": "HANOI"})
    page_content = response.data.decode()

    assert response.status_code == 200
    assert "Hanoi" in page_content


def test_search_no_result():
    client = app.test_client()
    response = client.get("/", query_string={"search": "sydney"})
    page_content = response.data.decode()

    assert response.status_code == 200
    assert "Ha Long Bay" not in page_content
    assert "Hoi An" not in page_content
    assert "Hanoi" not in page_content
    assert "Ho Chi Minh City" not in page_content


def test_filter_duration_with_multiple_results():
    client = app.test_client()
    response = client.get("/", query_string={"duration": "2-4 Days"})
    page_content = response.data.decode()

    assert response.status_code == 200
    assert "Hoi An" in page_content
    assert "Ho Chi Minh City" in page_content
    assert "Ha Long Bay" not in page_content
    assert "Hanoi" not in page_content


def test_filter_duration_no_result():
    client = app.test_client()
    response = client.get("/", query_string={"duration": "10 Days"})
    page_content = response.data.decode()

    assert response.status_code == 200
    assert "Ha Long Bay" not in page_content
    assert "Hoi An" not in page_content
    assert "Hanoi" not in page_content
    assert "Ho Chi Minh City" not in page_content


def test_search_and_duration_filter_no_match():
    client = app.test_client()
    response = client.get("/", query_string={
        "search": "hanoi",
        "duration": "2-4 Days"
    })
    page_content = response.data.decode()

    assert response.status_code == 200
    assert "Hanoi" not in page_content
    assert "Hoi An" not in page_content
    assert "Ho Chi Minh City" not in page_content


@pytest.mark.parametrize("destination_id, destination_name", [
    ("ha-long-bay", "Ha Long Bay"),
    ("hoi-an", "Hoi An"),
    ("hanoi", "Hanoi"),
    ("ho-chi-minh-city", "Ho Chi Minh City"),
])
def test_all_destination_detail_pages(destination_id, destination_name):
    client = app.test_client()
    response = client.get(f"/destination/{destination_id}")
    page_content = response.data.decode()

    assert response.status_code == 200
    assert destination_name in page_content


def test_invalid_destination_page_does_not_crash():
    client = app.test_client()
    response = client.get("/destination/unknown-place")

    assert response.status_code == 200

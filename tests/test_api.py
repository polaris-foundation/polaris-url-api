from flask.testing import FlaskClient


class TestApi:
    def test_create_short_url(self, client: FlaskClient) -> None:
        url_to_shorten = "https://test123.com"
        post_response = client.post("/dhos/v1/short_url", json={"url": url_to_shorten})
        assert post_response.json is not None
        get_response = client.get(
            f"/dhos/v1/original_url/{post_response.json['short_form']}"
        )
        assert get_response.json is not None
        assert "short_form" in post_response.json
        assert len(post_response.json) == 1
        assert "original_url" in get_response.json
        assert get_response.json["original_url"] == url_to_shorten

    def test_create_empty_url(self, client: FlaskClient) -> None:
        post_response = client.post("/dhos/v1/short_url", json={"url": ""})
        assert post_response.status_code == 400

    def test_create_invalid_url(self, client: FlaskClient) -> None:
        post_response = client.post("/dhos/v1/short_url", json={"url": "not_a_url"})
        assert post_response.status_code == 400

    def test_create_with_limit(self, client: FlaskClient) -> None:
        get_response = client.post(
            "/dhos/v1/short_url", json={"url": "https://test123.com", "maximum_uses": 2}
        )
        assert get_response.json is not None
        short_form: str = get_response.json["short_form"]
        post_response_1 = client.get(f"/dhos/v1/original_url/{short_form}")
        post_response_2 = client.get(f"/dhos/v1/original_url/{short_form}")
        post_response_3 = client.get(f"/dhos/v1/original_url/{short_form}")
        assert post_response_1.status_code == 200
        assert post_response_2.status_code == 200
        assert post_response_3.status_code == 404

    def test_create_twice(self, client: FlaskClient) -> None:
        url_to_shorten = "https://test123.com"
        post_response_1 = client.post(
            "/dhos/v1/short_url", json={"url": url_to_shorten}
        )
        post_response_2 = client.post(
            "/dhos/v1/short_url", json={"url": url_to_shorten}
        )
        assert post_response_1.json is not None
        assert post_response_2.json is not None
        assert post_response_1.json["short_form"] == post_response_2.json["short_form"]

    def test_create_no_parameters(self, client: FlaskClient) -> None:
        response = client.post("/dhos/v1/short_url")
        assert response.status_code == 400

    def test_retrieve_no_short_form(self, client: FlaskClient) -> None:
        response = client.get("/dhos/v1/original_url")
        assert response.status_code == 404

    def test_retrieve_invalid_short_form(self, client: FlaskClient) -> None:
        response = client.get("/dhos/v1/original_url/12345")
        assert response.status_code == 404

    def test_debug(self, client: FlaskClient) -> None:
        response = client.get("/debug", headers={"X-Something": "some-value"})
        assert response.status_code == 200
        assert response.json is not None
        assert response.json["X-Something"] == "some-value"

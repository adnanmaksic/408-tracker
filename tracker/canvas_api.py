import requests


class CanvasAPIError(Exception):
    pass


class CanvasClient:
    def __init__(self, base_url, token):
        if not token:
            raise CanvasAPIError("CANVAS_API_TOKEN is missing.")

        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {token}"
        })

    def get_all(self, endpoint, params=None):
        url = f"{self.base_url}{endpoint}"
        results = []

        while url:
            try:
                response = self.session.get(
                    url,
                    params=params,
                    timeout=15,
                )
                response.raise_for_status()
                data = response.json()
            except requests.RequestException as error:
                raise CanvasAPIError(
                    f"Canvas request failed: {error}"
                ) from error
            except ValueError as error:
                raise CanvasAPIError(
                    "Canvas returned invalid JSON."
                ) from error

            results.extend(data)
            url = self.get_next_url(response.headers.get("Link"))
            params = None

        return results

    @staticmethod
    def get_next_url(link_header):
        if not link_header:
            return None

        for link in link_header.split(","):
            if 'rel="next"' in link:
                return link.split(";")[0].strip().strip("<>")

        return None

    def get_courses(self):
        return self.get_all(
            "/api/v1/courses",
            {
                "enrollment_state": "active",
                "per_page": 100,
            },
        )

    def get_assignments(self, course_id):
        return self.get_all(
            f"/api/v1/courses/{course_id}/assignments",
            {
                "order_by": "due_at",
                "per_page": 100,
            },
        )
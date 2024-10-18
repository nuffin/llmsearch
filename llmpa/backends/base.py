import requests
from requests.exceptions import HTTPError, Timeout, RequestException
from typing import Optional, List


class ClientBase:
    def __init__(
        self,
        base_url: str,
        api_key: Optional[str] = None,
        verify_ssl: Optional[bool] = True,
        timeout: Optional[int] = 10,
    ):
        self.base_url = base_url
        if self.base_url.endswith("/"):
            self.base_url = self.base_url[:-1]
        self.api_key = api_key
        self.verify_ssl = verify_ssl
        self.timeout = timeout
        self.headers = {
            "Authorization": f"Bearer {self.api_key}" if self.api_key else None,
            "Content-Type": "application/json",
        }

    def _make_request(
        self,
        method,
        endpoint,
        data=None,
        json=None,
        params=None,
        extra_headers=None,
        timeout: Optional[int] = None,
    ):
        """
        Make an HTTP request to the LocalAI server.

        :param method: HTTP method (GET, POST, PUT, DELETE).
        :param endpoint: The API endpoint to hit.
        :param data: The request body for POST/PUT requests.
        :param params: Query parameters for GET/DELETE requests.
        :param extra_headers: Additional headers for the request.
        :return: Parsed JSON response or None if an error occurred.
        """
        url = f"{self.base_url}{endpoint}"
        headers = {**self.headers, **(extra_headers or {})}

        print(
            f"data={data}, json={json}, params={params}, extra_headers={extra_headers}"
        )
        try:
            response = requests.request(
                method=method.upper(),
                url=url,
                data=data,
                json=json,
                params=params,
                headers=headers,
                verify=self.verify_ssl,
                timeout=timeout or self.timeout,
            )
            response.raise_for_status()  # Raise HTTPError for bad responses
            return response
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Timeout as timeout_err:
            print(f"Timeout error: {timeout_err}")
        except RequestException as req_err:
            print(f"Request error: {req_err}")
        except Exception as err:
            print(f"An error occurred: {err}")
        return None

    def get(
        self, endpoint, params=None, extra_headers=None, timeout: Optional[int] = None
    ):
        return self._make_request(
            "GET", endpoint, params=params, extra_headers=extra_headers, timeout=timeout
        )

    def post(
        self,
        endpoint,
        data=None,
        json=None,
        extra_headers=None,
        timeout: Optional[int] = None,
    ):
        return self._make_request(
            "POST",
            endpoint,
            data=data,
            json=json,
            extra_headers=extra_headers,
            timeout=timeout,
        )

    def put(
        self,
        endpoint,
        data=None,
        json=None,
        extra_headers=None,
        timeout: Optional[int] = None,
    ):
        return self._make_request(
            "PUT",
            endpoint,
            data=data,
            json=json,
            extra_headers=extra_headers,
            timeout=timeout,
        )

    def delete(
        self, endpoint, params=None, extra_headers=None, timeout: Optional[int] = None
    ):
        return self._make_request(
            "DELETE",
            endpoint,
            params=params,
            extra_headers=extra_headers,
            timeout=timeout,
        )

    def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
        max_tokens: Optional[int] = 150,
        temperature: Optional[float] = 1.0,
    ) -> Optional[str]:
        raise NotImplementedError

    def embedding_text(self, text: str, model: str) -> Optional[List[float]]:
        raise NotImplementedError

    def embedding_file(self, filepath: str, model: str) -> Optional[List[float]]:
        raise NotImplementedError

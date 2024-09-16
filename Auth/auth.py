import json


class FlowException(Exception):
    pass


def auth(self):
    body_ = {"login": self.login, "password": self.password, "is_remember": True}
    with self.client.request(method='POST',
                             url="/api/v1/login",
                             data=json.dumps(body_),
                             catch_response=True,
                             headers={"Content-Type": "application/json"},
                             verify=self.environment.parsed_options.ssl_check,
                             name="auth/login") as response:
        self.logging_response(response)
        return response


def get_http_headers(token):
    headers = {
        "Cookie": "access_token=" + token, "Content-Type": "application/json",
        "Accept-Language": "ru,ru-RU;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    return headers

class FlowException(Exception):
    pass


def baseGet(self, name_scenario, resource, param=None):
    with self.client.request(method='GET',
                             url=resource,
                             headers=self.header,
                             params=param,
                             catch_response=True,
                             verify=self.environment.parsed_options.ssl_check,
                             name=name_scenario + "/" + resource) as response:
        self.logging_response(response)
    return response


def basePost(self, name_scenario, resource, body=None):
    with self.client.request(method='POST',
                             url=resource,
                             headers=self.header,
                             json=body,
                             catch_response=True,
                             verify=self.environment.parsed_options.ssl_check,
                             name=name_scenario + "/" + resource) as response:
        self.logging_response(response)
    return response


def basePUT(self, name_scenario, resource, body=None):
    with self.client.request(method='PUT',
                             url=resource,
                             headers=self.header,
                             json=body,
                             catch_response=True,
                             verify=self.environment.parsed_options.ssl_check,
                             name=name_scenario + "/" + resource) as response:
        self.logging_response(response)
    return response

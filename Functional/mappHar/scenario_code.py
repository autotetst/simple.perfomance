def base_code():
    file_Base_code = '''
import time
import logging

from locust import HttpUser, task, between, events,tag

from Auth import auth
from Functional import base

@events.init_command_line_parser.add_listener
def _(parser):
    parser.add_argument("--SuperLogin", type=str, env_var="SuperLogin", default='')
    parser.add_argument("--SuperPass", type=str, env_var="SuperPass", default='')
    parser.add_argument("--ssl_check", type=bool, env_var="ssl_check", default=True)

class FlowException(Exception):
   pass

class LoadTest(HttpUser):
    wait_time = between(1, 3)
    token = ""
    header = None
    login = None
    password = None

    def __init__(self, *args, **kwargs):
        pass
        # Блок кода ниже включает авторизцию пользователя. Необходимо раскоментировать его
        # При необходимости поправить функцию Auth/auth.auth()
        # super().__init__(*args, **kwargs)
        # self.login = self.environment.parsed_options.SuperLogin
        # self.password = self.environment.parsed_options.SuperPass
        # 
        # response = None
        # for i in range(0, 60):#Нужно получить начальный токен любыми путями)
        #     response = auth.auth(self)
        #     if response.status_code > 299:
        #         time.sleep(2)
        #     else:
        #         break      
        # 
        # self.token = response.json()["access_token"]
        # 
        # self.header = auth.get_http_headers(self.token)
        # logging.info(f'===== Auth user: {self.login} =====')
        # logging.info(f'Token received: {self.token}')

    @staticmethod
    def logging_response(response):
        """
        Метод логирования полученного ответа метода
        Работает правильно при условии, что в запросе был передан аргумент catch_response=True
        :param response: ответ метода
        :return: None
        :Логирует только ошибки. Позитивные запросы не логируются
        """
        try:
            if int(response.status_code) > 299:
                logging.error(response.status_code)
                logging.error(response.request.path_url)
                logging.error(response.request.headers)
                logging.error(response.request.body)
                logging.error(response.text)
        except (KeyError, AttributeError) as error:
            logging.error(error)
            response.failure(error)

    @staticmethod
    def eventScenario(result):
        if int(result["time_delta"]) == 0:
            return
        events.request.fire(
            request_type="SCENARIO",
            name=result["nameSc"],
            response_time=int(result["time_delta"]),
            response_length=0,
            context=None,
            exception=None,
        )

    '''
    return file_Base_code


def scenario_code(scenarioDetail):
    name_sc = scenarioDetail[0]["name_scenario"].split('!')[1]
    name_sc = name_sc.split('.')[0]
    code = f'''
        
    @tag('{name_sc}')
    @task ({scenarioDetail[0]["priority"]})
    def {name_sc}(self):
        time_start = int(time.time() * 1000)'''
    for i in scenarioDetail:
        if i["type_request"] == "GET":
            code = code + f'''
        base.baseGet(self,'{name_sc}','{i["resource"]}')'''
        if i["type_request"] == "POST":
            code = code + f'''
        base.basePost(self,'{name_sc}','{i["resource"]}',{i["body"]})'''
        if i["type_request"] == "PUT":
            code = code + f'''
        base.basePUT(self,'{name_sc}','{i["resource"]}',{i["body"]})'''
    code = code + '''
        result = {}
        result["nameSc"] = "''' + name_sc + '''"
        time_end = int(time.time() * 1000)
        time_delta = (time_end - time_start)
        result["time_delta"] = time_delta
        self.eventScenario(result)'''
    return code

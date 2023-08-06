import dynaconf
from dynaconf.vendor.toml.decoder import TomlDecodeError
from .common import constant, common
from .common import logger
from .configuration.wb import webSocket
from .configuration.sql import MySql
from .configuration.request import requestBase
from rediscluster import RedisCluster
from redis import StrictRedis
from autoTestScheme.configuration import robot
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os, copy


class Report(dict):

    _object = {'env': [], 'button_element':[], 'other_element': []}

    def __getattr__(self, item):
        if item in self._object:
            return self._object.get(item)
        return super().__getattribute__(item)


class BaseDynaconf(dynaconf.Dynaconf):
    _hook_list = {}
    _hook_client_list = {}
    _hook_close_list = {}
    _client_list = {}
    _fixture_list = []
    _report = Report()
    default_settings = {'current_tag': 'debug', 'test_tags': ['info'], 'test_case': 'all', 'is_debug': False,
                        'tag_name_list': {'all': '其他'}, 'tag_env_list': {'all': 'all'}, 'tag_env_name_list': {'all': 'all'}, 'is_locust': False}

    def __init__(self, *args, **kwargs):
        super(BaseDynaconf, self).__init__(*args, **kwargs)
        self._first_session = False
        self._end_session = False
        self.init_run_config()

    def init_run_config(self):
        if self.exists('run'):
            self.set('run', {})
        for key, value in self.default_settings.items():
            if key not in self.run:
                setattr(self.run, key, value)
        self._report.env.append(['环境:', self.get_env_name()])

        tag_name = []
        for i in self.run.test_tags:
            if i not in self.run.tag_env_name_list:
                tag_name.append(f'标签{i}未定义名称')
            else:
                tag_name.append(self.run.tag_env_name_list[i])
        self._report.env.append(['标签:', ';'.join(tag_name)])
        self._report.env.append(['执行用例:', self.run.test_case])

        self.register_hook('redis', self.get_redis)
        self.register_hook('request', self.get_session)
        self.register_hook('sql', self.get_sql)
        self.register_hook('feishu', self.get_feishu)
        self.register_hook('ws', self.get_websocket)
        self.register_hook('browser', self.get_browsert)
        self.register_hook_close('browser', self.close_browsert)

    def close_browsert(self, browsert):
        logger.info('关闭浏览器驱动')
        browsert.close()
        browsert.quit()

    def get(self, name, default_value=None):
        try:
            return self.__getattr__(name)
        except Exception as e:
            if default_value is not None:
                return default_value
            raise e

    def __getattr__(self, item: str):
        if item == '_report':
            return self._report
        try:
            result = super().__getattr__(item)
        except TomlDecodeError as e:
            raise TypeError("toml文件格式错误，{}".format(e))
        except Exception as e:
            raise KeyError("配置文件内未定义{}".format(item))
        for name, func in self._hook_list.items():
            if item.startswith(name):
                if item not in self._client_list:
                    if name not in self._hook_client_list:
                        self._hook_client_list[name] = []
                    self._client_list[item] = func(item, result)
                    self._hook_client_list[name].append(self._client_list[item])
                return self._client_list[item]
        return result

    def register_hook_close(self, name, func):
        self._hook_close_list[name] = func

    def execute_all_close_hook(self):
        for name, func in self._hook_close_list.items():
            if name in self._hook_client_list:
                for i in self._hook_client_list[name]:
                    try:
                        func(i)
                    except Exception:
                        logger.exception('execute_all_close_hook :')

    def register_hook(self, name, func):
        self._hook_list[name] = func

    def get_redis(self, item, config):
        new_config = copy.deepcopy(config)
        is_colony = new_config.get('is_colony', True)
        if 'is_colony' in new_config:
            del new_config['is_colony']
        obj = None
        if is_colony is True:
            if 'db' in new_config:
                del new_config['db']
            obj = RedisCluster(**new_config)
        else:
            obj = StrictRedis(**new_config)
        return obj

    def get_session(self, item, config) -> requestBase:
        request = requestBase()
        if config.get("base_url", None) is not None:
            request.base_url = config['base_url']
            request.kwargs = config
            for i in config.get('api', []):
                request.read_api_folder(*i)
        else:
            logger.error("{} 注册request失败, 配置信息:{}".format(item, config))
        logger.info('注册{}'.format(item))
        return request

    def get_sql(self, item, config) -> requestBase:
        sql = MySql()
        sql.connect(config)
        return sql

    def get_feishu(self, item, config):
        access_token = config.get('access_token')
        secret = config.get('secret')
        app_id = config.get('app_id')
        app_secret = config.get('app_secret')
        chat_id = config.get('chat_id')
        feishu = robot.LarkApi(app_id, app_secret, access_token, secret, chat_id, config)
        if config.get('sheet_token') is not None:
            feishu.sheet = feishu.get_sheet_object(config.get('sheet_token'))
        return feishu

    def get_websocket(self, item, config):
        ws = webSocket(config)
        for i in config.get('api', []):
            ws.read_api_folder(*i)
        return ws

    def get_browsert(self, item, config):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--blink-settings=imagesEnabled=true')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--proxy-excludeSwitcher=enable-automation')
        for k, v in config.items():
            chrome_options.add_argument(f'--{k}={v}')
        path = ChromeDriverManager().install()
        service = Service(executable_path=path)
        browser = webdriver.Chrome(service=service, options=chrome_options)
        browser.maximize_window()
        return browser

    def get_env_name(self):
        current_env = self.current_env
        tag_name_list = self.run.get('tag_name_list', None)
        if tag_name_list is None or current_env not in tag_name_list:
            if self.exists('name'):
                return self.name
            else:
                return current_env
        else:
            return self.run.tag_name_list[current_env]


settings = BaseDynaconf(envvar_prefix=False, merge_enabled=True, environments=True, load_dotenv=True,
                        env_switcher="ENV", root_path=constant.CONFIG_FOLDER, includes=['*.toml'])

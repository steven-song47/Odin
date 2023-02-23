import logging
import time
from typing import List
from common.common import ExecuteCMD, ReadConfig, JsonFileOperation, TimeOperation


# commented out function will be filtered
# def get_headers():
#     return {"User-Agent": "hrp"}


def get_user_agent():
    return "hrp/funppy"


def sleep(n_secs):
    time.sleep(n_secs)


def sum(*args):
    result = 0
    for arg in args:
        result += arg
    return result


def sum_ints(*args: List[int]) -> int:
    result = 0
    for arg in args:
        result += arg
    return result


def sum_two_int(a: int, b: int) -> int:
    return a + b


def sum_two_string(a: str, b: str) -> str:
    return a + b


def sum_strings(*args: List[str]) -> str:
    result = ""
    for arg in args:
        result += arg
    return result


def concatenate(*args: List[str]) -> str:
    result = ""
    for arg in args:
        result += str(arg)
    return result


def setup_hook_example(name):
    logging.warning("setup_hook_example")
    return f"setup_hook_example: {name}"


def teardown_hook_example(name):
    logging.warning("teardown_hook_example")
    return f"teardown_hook_example: {name}"


def save_response(step_resp, name):
    timeOperate = TimeOperation()
    time_str = str(timeOperate.get_now_int())
    jsonOperate = JsonFileOperation()
    history_data = {
        "result": "pass",
        "data:": step_resp["body"]
    }
    jsonOperate.write_json_to_file(time_str + "_" + name + ".json", history_data, "/history")
    return "res.json"


def completion_validation():
    pass


def get_token(service, env):
    token = ""
    cmd = ""
    read = ReadConfig()
    config = read.read_config()
    for service_config in config["services"]:
        if service_config["name"] == service:
            for env_config in service_config['env']:
                if env_config['name'] == env:
                    cmd = env_config['token_cmd']
    print("cmd:", cmd)
    execute = ExecuteCMD()
    output = execute.execute(cmd, outprint=True)
    token = output["tokenType"] + " " + output["accessToken"]
    return token


def get_host(service, env):
    host = ""
    read = ReadConfig()
    config = read.read_config()
    for service_config in config["services"]:
        if service_config["name"] == service:
            for env_config in service_config['env']:
                if env_config['name'] == env:
                    host = env_config['host']
    return host


if __name__ == '__main__':
    print(get_token("dashboard", "qa"))
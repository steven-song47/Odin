from common.common import ExecuteCMD, ReadConfig, JsonFileOperation
import copy, os


class ScriptOperate:

    def __init__(self):
        default_path = os.path.abspath(__file__)
        self.root_path = "/".join(default_path.split("/")[:-2])
        self.api_root_path = self.root_path + "/testcases/api"
        self.case_root_path = self.root_path + "/testcases/cases"
        self.filter_method = ["GET", "POST", "PUT"]

    def get_hosts_of_service(self, service_name):
        host_map = dict()
        rconfig = ReadConfig()
        config = rconfig.read_config()
        for service_config in config["services"]:
            if service_config["name"] == service_name:
                host_map = service_config['env']
        return host_map

    def match_host_with_map(self, host, host_map):
        env = ""
        for host_item in host_map:
            if host in host_item["host"]:
                env = host_item["name"]
        return env, host

    def search_host_in_url(self, url, host_map):
        env = ""
        host = ""
        for host_item in host_map:
            if host_item["host"] in url:
                env = host_item["name"]
                host = host_item["host"]
        return env, host

    def filter_method_of_url(self, data):
        api_list = list()
        for api in data:
            if api["method"] in self.filter_method:
                api_list.append(api)
        return api_list

    def deal_with_headers(self, header):
        if "Authorization" in header:
            header.pop("Authorization")
        return header

    def cut_json_to_api(self, service, data, host_map):
        api_info = list()
        for api in data["teststeps"]:
            api_orig_data = api["request"]
            if "headers" in api_orig_data and "Host" in api_orig_data["headers"]:
                env, host = self.match_host_with_map(api_orig_data["headers"]["Host"], host_map)
            else:
                env, host = self.search_host_in_url(api_orig_data["url"], host_map)
            if env:
                api_items = {
                    "name": api_orig_data["url"].split(host)[1],
                    "host": host,
                    "method": api_orig_data["method"],
                    "url": api_orig_data["url"].split(host)[1],
                    "headers": self.deal_with_headers(api_orig_data["headers"]),
                    "env": env,
                    "service": service
                }
                api_info.append(api_items)
        return api_info

    def _read_api_template(self):
        jfile = JsonFileOperation()
        data = jfile.read_json_from_file("template_for_api.json", "/testcases/api")
        return data

    def switch_har_to_json(self, har_file_path):
        file_name = har_file_path.split("/")[-1]
        execute = ExecuteCMD()
        cmd = "hrp convert " + har_file_path + " --output-dir " + self.root_path + "/temp"
        execute.execute(cmd)
        new_file_name = file_name.split(".")[0] + "_test.json"
        new_file_path = self.root_path + "/temp/" + new_file_name
        if os.path.exists(new_file_path):
            return new_file_path
        else:
            return ""

    def switch_json_to_api(self, api_info):
        template_json = self._read_api_template()
        api_list = list()
        for api in api_info:
            api_data = dict()
            api_data = copy.deepcopy(template_json)
            api_data["config"]["name"] = api["name"].split("/")[-1]
            api_data["config"]["variables"]["service"] = api["service"]
            api_data["config"]["variables"]["env"] = api["env"]
            api_data["config"]["variables"]["api_name"] = api["name"].split("/")[-1]
            api_data["teststeps"][0]["name"] = api["url"]
            api_data["teststeps"][0]["request"]["method"] = api["method"]
            api_data["teststeps"][0]["request"]["url"] = api["url"]
            api_list.append(api_data)
        return api_list

    def create_service_dir(self, service_name):
        api_dir_path = self.api_root_path + "/" + service_name
        if not os.path.exists(api_dir_path):
            os.mkdir(api_dir_path)
        case_dir_path = self.case_root_path + "/" + service_name
        if not os.path.exists(case_dir_path):
            os.mkdir(case_dir_path)

    def create_api_case(self, service_name, api_data):
        jfile = JsonFileOperation()
        name = api_data["teststeps"][0]["request"]["method"].upper() + "_" + api_data["config"]["variables"]["api_name"] + ".json"
        jfile.write_json_to_file(name, api_data, "/testcases/api/" + service_name)

    def create_case(self, service_name):
        pass

    def execute_scripts(self):
        pass


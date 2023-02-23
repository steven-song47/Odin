from subprocess import Popen, PIPE
import json, yaml, os, time


class FileOperate:

    def __init__(self):
        default_path = os.path.abspath(__file__)
        root_path = "/".join(default_path.split("/")[:-2])
        self.har_dir = root_path + "/har"

    def get_har_files(self, dir=None):
        file_paths = dict()
        if dir:
            self.har_dir = dir
        if not os.path.exists(self.har_dir):
            return
        dir_list = list()
        for root, directories, files in os.walk(self.har_dir):
            if root == self.har_dir:
                dir_list = directories
            min_dir = root.split("/")[-1]
            if min_dir in dir_list and directories == []:
                dir_files = list()
                for filename in files:
                    if os.path.splitext(filename)[-1] == ".har":
                        filepath = os.path.join(root, filename)
                        dir_files.append(filepath)
                file_paths[min_dir] = dir_files
        return file_paths


class ExecuteCMD:

    def __init__(self):
        pass

    def execute(self, cmd, shell=True, outprint=False):
        output = ""
        p = Popen(cmd, shell=shell, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        for line in iter(p.stdout.readline, b''):
            # print("line:", line)
            output += str(line, "UTF-8")
            if not Popen.poll(p) is None:
                if line == "":
                    break
        p.stdout.close()
        print(output)
        if outprint:
            output = json.loads(output)
        return output


class ReadConfig:

    def __init__(self):
        default_path = os.path.abspath(__file__)
        self.root_path = "/".join(default_path.split("/")[:-2])

    def read_config(self):
        path = self.root_path + "/config.yaml"
        with open(path, encoding="utf-8") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        return data


class JsonFileOperation:

    def __init__(self):
        default_path = os.path.abspath(__file__)
        self.root_path = "/".join(default_path.split("/")[:-2])

    def write_json_to_file(self, file_name, json_data, file_path=None, encoding="utf-8"):
        if not file_path:
            file_path = self.root_path
        else:
            file_path = self.root_path + file_path
        with open(file_path + "/" + file_name, "w", encoding=encoding) as f:
            f.write(json.dumps(json_data, indent=4, ensure_ascii=False))

    def read_json_from_file(self, file_name, file_path=None, encoding="utf-8"):
        if not file_path:
            file_path = self.root_path
        else:
            file_path = self.root_path + file_path
        with open(file_path + "/" + file_name, "r", encoding=encoding) as f:
            if ".json" in file_name:
                data = json.loads(f.read())
            else:
                data = f.read()
        return data


class TimeOperation:

    def __init__(self):
        pass

    @staticmethod
    def get_now_date(time_format="datetime"):
        if time_format == "datetime":
            return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        elif time_format == "date":
            return time.strftime("%Y-%m-%d", time.localtime())

    @staticmethod
    def get_now_int():
        return int(time.time())



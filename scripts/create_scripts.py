from common.common import FileOperate, JsonFileOperation
from common.script import ScriptOperate


def create_scripts_automatically():
    script_operate = ScriptOperate()
    jfile_operate = JsonFileOperation()

    # Get all the service dirs in the har dir
    f = FileOperate()
    file_paths = f.get_har_files()
    service_api = dict()
    for service_name in file_paths:
        # If some har files exist in this service dir
        if file_paths[service_name]:
            service_api[service_name] = list()
            for file in file_paths[service_name]:
                # Iterate over all the har files, and convert har file to json file which stored in temp dir
                file_path = script_operate.switch_har_to_json(file)
                if file_path:
                    # Get the json data from the json file in temp dir
                    file_name = file_path.split("/")[-1]
                    dir_path = "/temp"
                    data = jfile_operate.read_json_from_file(file_name, dir_path)
                    # Get the config
                    host_map = script_operate.get_hosts_of_service(service_name)
                    # Get the api info from the json data
                    api_list = script_operate.cut_json_to_api(service_name, data, host_map)
                    # Filter the method of the url (GET, POST, PUT)
                    api_list = script_operate.filter_method_of_url(api_list)
                    # Switch json data to api test script json
                    api_list = script_operate.switch_json_to_api(api_list)
                    # Create the service dir and api scripts in the testcases dir
                    script_operate.create_service_dir(service_name)
                    for api in api_list:
                        script_operate.create_api_case(service_name, api)


if __name__ == '__main__':
    create_scripts_automatically()

# ThousandEyes Grafana Dashboard 1.0.1
# CISCO SAMPLE CODE LICENSE Version 1.1, Cisco Systems 2021, flopach

import config
# import influxdb_connect
import time
import requests
import logging
import datetime
import json
from rich import print


json_results = {
    'json_input_1000eye_http_server_net_metrics_loss': {
        'metric_name': 'json_input_1000eye_http_server_net_metrics_loss',
        'help': 'http server net metrics',
        'type': 'gauge',
        'labels': ['measurement', 'testName', 'agentName', 'm_serverIp'],
        'values': []
    },
    'json_input_1000eye_http_server_net_metrics_jitter': {
        'metric_name': 'json_input_1000eye_http_server_net_metrics_jitter',
        'help': 'http server net metrics',
        'type': 'gauge',
        'labels': ['measurement', 'testName', 'agentName', 'm_serverIp'],
        'values': []
    },
    'json_input_1000eye_http_server_net_metrics_maxLatency': {
        'metric_name': 'json_input_1000eye_http_server_net_metrics_maxLatency',
        'help': 'http server net metrics',
        'type': 'gauge',
        'labels': ['measurement', 'testName', 'agentName', 'm_serverIp'],
        'values': []
    },
    'json_input_1000eye_http_server_net_metrics_avgLatency': {
        'metric_name': 'json_input_1000eye_http_server_net_metrics_avgLatency',
        'help': 'http server net metrics',
        'type': 'gauge',
        'labels': ['measurement', 'testName', 'agentName', 'm_serverIp'],
        'values': []
    },
    'json_input_1000eye_http_server_net_metrics_minLatency': {
        'metric_name': 'json_input_1000eye_http_server_net_metrics_minLatency',
        'help': 'http server net metrics',
        'type': 'gauge',
        'labels': ['measurement', 'testName', 'agentName', 'm_serverIp'],
        'values': []
    }
}

# set logger config
logging.getLogger().setLevel(logging.INFO)
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s")

def get_tests_by_type():
    """
    Returns a dictionary with of all tests sorted by the type, configured in ThousandEyes. 

    :return: dictionary, format: { "test-type" : [ list of tests ], "test-type" : [ list of tests ], ... }
    """
    try:

        headers = {
                "Accept": "application/json",
                "Authorization": "Bearer {}".format(config.oauth_bearer_token)
            }

        all_tests = {}

        # Get test details for each test type which is defined in config.py
        for config_test_type in config.test_types:

            # request the data
            try:

                r = requests.request('GET', f"{config.base_url}/tests/{config_test_type}.json", headers=headers)
                r.raise_for_status()

                test_per_type_list = []

                if r.status_code == 200:
                    logging.info(f"Successfully requested tests for type {config_test_type}.")

                    for te_test in r.json()["test"]:
                        test_instance = {
                            'testId': te_test["testId"],
		                    'testName': te_test["testName"],
                            'interval': te_test["interval"]
                        }
                        test_per_type_list.append(test_instance)

                    all_tests[config_test_type] = test_per_type_list

            except Exception as e:
                logging.exception(f"Error! Could not get data for test type {config_test_type}: {e}")
        
        logging.info(f"Got all test infos of all requested types.")

        #with open('tests.json', 'w') as outfile:
        #    json.dump(all_tests, outfile)

        return all_tests

    except Exception as e:
        logging.exception(f"Error! Could not create all_tests dictionary: {e}")

def get_tests_by_label():
    """
    Returns a dictionary with of all tests which are tagged with the define label in the config
    :return: dictionary, format: { "test-type" : [ list of tests ], "test-type" : [ list of tests ], ... }
    """

    try:
        # get groupId of the label to receive testIds
        label_groupId = _get_groupid_from_label(config.label_name)

        headers = {
            "Accept": "application/json",
            "Authorization": "Bearer {}".format(config.oauth_bearer_token)
        }

        all_tests = {}

        # request details (TestIds etc.) of the label group
        try:
            r = requests.request('GET', f"{config.base_url}/groups/{label_groupId}", headers=headers)
            r.raise_for_status()

            if r.status_code == 200:
                logging.info(f"Successfully requested tests for label {config.label_name}.")

                for te_test in r.json()["groups"][0]["tests"]:
                    test_instance = {
                        'testId': te_test["testId"],
                        'testName': te_test["testName"],
                        'interval': te_test["interval"]
                    }

                    # if list is not yet created, create one in the except clause
                    try:
                        all_tests[te_test["type"]].append(test_instance)
                    except KeyError:
                        all_tests[te_test["type"]] = []
                        all_tests[te_test["type"]].append(test_instance)
        
        except Exception as e:
            logging.exception(f"Error! Could not create all_tests dictionary: {e}")
        
        logging.info(f"Pulling data from these tests: {all_tests}.")
        return all_tests

    except Exception as e:
        logging.exception(f"Error! Could not create all_tests dictionary: {e}")

def _get_groupid_from_label(label_name):
    """
    Returns the groupId for the stated TE label (defined in TE dashboard)

    :return: int, groupId of variable label_name
    """
    try:

        headers = {
            "Accept": "application/json",
            "Authorization": "Bearer {}".format(config.oauth_bearer_token)
        }

        r = requests.request('GET', f"{config.base_url}/groups/tests/", headers=headers)
        r.raise_for_status()

        if r.status_code == 200:

            for group in r.json()["groups"]:
                if group["name"] == label_name:
                    return group["groupId"]

    except Exception as e:
        logging.exception(f"Error! Could not get data for label {label_name}: {e}")

# def _insert_to_influx_v2(insert_to_db,te_test):
#     """
#     :insert_to_db: JSON friendly format for InfluxDBv2
#     :te_test: Name of the TE Test

#     Insert to database
#     """
#     try:
#         influxdb_connect.write_api.write(
#             bucket=config.influx_bucket,
#             org=config.influx_org,
#             record=insert_to_db,
#             write_precision=influxdb_connect.WritePrecision.S)
#         logging.info(f"{te_test}: ...inserted into database.")
#     except Exception as e:
#         logging.exception(f"Can't insert data into Influx for test {te_test}: {e}")

def _parse_and_convert_http_server(resp,testId,testName):
    """
    Parsing Function for TE API response + converting response date to InfluxDBv2 friendly JSON format
    TE: (Web) HTTP server

    :resp: raw response from TE API to get detailed Test info. Example: /v6/web/http-server/{testId}
    :testId: Test ID
    :testName: Test  Name

    :return: InfluxDBv2 friendly List with datasets
    """
    te_test_dataset_group = []

    #Iterate through historical data and add it to a list
    for te_test_data in resp["web"]["httpServer"]:

        try:
            # converting time format to epoch time
            te_event_time = datetime.datetime.strptime(te_test_data["date"], "%Y-%m-%d %H:%M:%S").timestamp()

            #influxDB JSON format
            one_dataset = {
                "measurement": testId,
                "tags":
                    {
                        "testName": testName,
                        "agentName": te_test_data["agentName"]
                    },
                "fields": {
                        "errorType": te_test_data["errorType"],
                        "numRedirects": te_test_data["numRedirects"],
                        "responseCode": te_test_data["responseCode"]
                    },
                "time": round(te_event_time)
                }

            # just to be sure, adding for now IFs to surely add all data
            # Depending on the errorType, TE is not sending all keys

            if "serverIp" in te_test_data:
                one_dataset["tags"]["serverIp"] = te_test_data["serverIp"]

            if "throughput" in te_test_data:
                one_dataset["fields"]["throughput"] = te_test_data["throughput"]

            if "receiveTime" in te_test_data:
                one_dataset["fields"]["receiveTime"] = te_test_data["receiveTime"]

            if "connectTime" in te_test_data:
                one_dataset["fields"]["connectTime"] = te_test_data["connectTime"]

            if "sslTime" in te_test_data:
                one_dataset["fields"]["sslTime"] = te_test_data["sslTime"]

            if "dnsTime" in te_test_data:
                one_dataset["fields"]["dnsTime"] = te_test_data["dnsTime"]

            if "responseTime" in te_test_data:
                one_dataset["fields"]["responseTime"] = te_test_data["responseTime"]

            if "totalTime" in te_test_data:
                one_dataset["fields"]["totalTime"] = te_test_data["totalTime"]
            
            if "waitTime" in te_test_data:
                one_dataset["fields"]["waitTime"] = te_test_data["waitTime"]

            if "wireSize" in te_test_data:
                one_dataset["fields"]["wireSize"] = te_test_data["wireSize"]

            if "sslVersion" in te_test_data:
                one_dataset["tags"]["sslVersion"] = te_test_data["sslVersion"]

            # adding this cause: if number of redirects is 0, there is no key redirectTime
            if int(te_test_data["numRedirects"]) > 0:
                one_dataset["fields"]["redirectTime"] = te_test_data["redirectTime"]

            te_test_dataset_group.append(one_dataset)
        
        except Exception as e:
            logging.exception(f"Error when getting data from HTTP-Server test {testName}: {e}")

    return te_test_dataset_group

def _parse_and_convert_page_load(resp,testId,testName):
    """
    Parsing Function for TE API response + converting response date to InfluxDBv2 friendly JSON format
    TE: (Web) Page load

    :resp: raw response from TE API to get detailed Test info. Example: /v6/web/page-load/{testId}
    :testId: Test ID
    :testName: Test  Name

    :return: InfluxDBv2 friendly List with datasets
    """
    te_test_dataset_group = []

    #Iterate through historical data and add it to a list
    for te_test_data in resp["web"]["pageLoad"]:

        try:
            # converting time format to epoch time
            te_event_time = datetime.datetime.strptime(te_test_data["date"], "%Y-%m-%d %H:%M:%S").timestamp()

            #influxDB JSON format
            one_dataset = {
                "measurement": testId,
                "tags":
                    {
                        "testName": testName,
                        "agentName": te_test_data["agentName"]
                    },
                "fields": { },
                "time": round(te_event_time)
                }

            # Depending on the errror, TE is not sending all keys

            if "numErrors" in te_test_data:
                one_dataset["fields"]["numErrors"] = te_test_data["numErrors"]

            if "numObjects" in te_test_data:
                one_dataset["fields"]["numObjects"] = te_test_data["numObjects"]

            if "responseTime" in te_test_data:
                one_dataset["fields"]["responseTime"] = te_test_data["responseTime"]

            if "pageLoadTime" in te_test_data:
                one_dataset["fields"]["pageLoadTime"] = te_test_data["pageLoadTime"]

            if "domLoadTime" in te_test_data:
                one_dataset["fields"]["domLoadTime"] = te_test_data["domLoadTime"]

            if "totalSize" in te_test_data:
                one_dataset["fields"]["totalSize"] = te_test_data["totalSize"]

            te_test_dataset_group.append(one_dataset)
        
        except Exception as e:
            logging.exception(f"Error when getting data from Page-load test {testName}: {e}")

    return te_test_dataset_group

def _parse_and_convert_end_to_end(resp,testId,testName):
    """
    Parsing Function for TE API response + converting response date to InfluxDBv2 friendly JSON format
    TE: (Network) End-to-End metrics

    :resp: raw response from TE API to get detailed Test info. Example: /v6/net/metrics/{testId}
    :testId: Test ID
    :testName: Test  Name

    :return: InfluxDBv2 friendly List with datasets
    """
    te_test_dataset_group = []

    #Iterate through historical data and add it to a list
    for te_test_data in resp["net"]["metrics"]:

        try:
            # converting time format to epoch time
            te_event_time = datetime.datetime.strptime(te_test_data["date"], "%Y-%m-%d %H:%M:%S").timestamp()

            #influxDB JSON format
            one_dataset = {
                "measurement": testId,
                "tags":
                    {
                        "testName": testName,
                        "agentName": te_test_data["agentName"]
                    },
                "fields": {},
                "time": round(te_event_time)
                }

            # Depending on the error, TE is not sending all keys

            if "server" in te_test_data:
                one_dataset["tags"]["m_server"] = te_test_data["server"]

            if "serverIp" in te_test_data:
                one_dataset["tags"]["m_serverIp"] = te_test_data["serverIp"]

            if "loss" in te_test_data:
                one_dataset["fields"]["loss"] = te_test_data["loss"]

            if "jitter" in te_test_data:
                one_dataset["fields"]["jitter"] = te_test_data["jitter"]

            if "maxLatency" in te_test_data:
                one_dataset["fields"]["maxLatency"] = te_test_data["maxLatency"]

            if "avgLatency" in te_test_data:
                one_dataset["fields"]["avgLatency"] = te_test_data["avgLatency"]

            if "minLatency" in te_test_data:
                one_dataset["fields"]["minLatency"] = te_test_data["minLatency"]

            te_test_dataset_group.append(one_dataset)
        
        except Exception as e:
            logging.exception(f"Error when getting data from Page-load test {testName}: {e}")

    return te_test_dataset_group

def _parse_and_convert_path_vis(resp,testId,testName):
    """
    Parsing Function for TE API response + converting response date to InfluxDBv2 friendly JSON format
    TE: (Network) Path visualization

    :resp: raw response from TE API to get detailed Test info. Example: /v6/net/path-vis/{testId}
    :testId: Test ID
    :testName: Test  Name

    :return: InfluxDBv2 friendly List with datasets
    """
    te_test_dataset_group = []

    #Iterate through historical data and add it to a list
    for te_test_data in resp["net"]["pathVis"]:

        try:
            # converting time format to epoch time
            te_event_time = datetime.datetime.strptime(te_test_data["date"], "%Y-%m-%d %H:%M:%S").timestamp()

            #influxDB JSON format
            one_dataset = {
                "measurement": testId,
                "tags":
                    {
                        "testName": testName,
                        "agentName": te_test_data["agentName"]
                    },
                "fields": {
                        "server": te_test_data["server"]
                    },
                "time": round(te_event_time)
                }

            # Depending on the error, TE is not sending all keys

            if "serverIp" in te_test_data:
                one_dataset["tags"]["pathvis_serverIp"] = te_test_data["serverIp"]

            if "sourceIp" in te_test_data:
                one_dataset["tags"]["pathvis_sourceIp"] = te_test_data["sourceIp"]

            try:
                # summarizing the endpoints array - calcullating average
                avg_numberOfHops = 0
                avg_responseTime = 0

                for endpoint in te_test_data["endpoints"]:
                    avg_numberOfHops += endpoint["numberOfHops"]
                    avg_responseTime += endpoint["responseTime"]

                one_dataset["fields"]["avg_numberOfHops"] = round(avg_numberOfHops / 3)
                one_dataset["fields"]["avg_responseTime"] = round(avg_responseTime / 3)
            except:
                pass

            te_test_dataset_group.append(one_dataset)
        
        except Exception as e:
            logging.exception(f"Error when getting data from Page-load test {testName}: {e}")

    return te_test_dataset_group

def get_test_data_insert_to_db(te_tests,te_test_type,parsing_function,window):
    """
    Get data from TE tests

    :te_tests: list of tests from function get_tests_by_type(). List-Elements: testId, testName, interval
    :te_test_type: string, path of the API request URL for the specific test (https://developer.thousandeyes.com/v6/test_data/). Example: "web/http-server"
    :parsing_function: function for parsing the response from TE API
    :window: time-range, possible values see https://developer.thousandeyes.com/v6/#/timeranges

    :return: None, errors will be shown in the logs
    """

    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(config.oauth_bearer_token)
    }

    # when requesting data periodically, do not use a time window
    if window == "latest":
        params = {}
    else:
        params = {
            "window": window
        }

    try:

        # Iterate through each test which got requested by type. Elements: testId, testName, interval
        for te_test in te_tests:

            # request historical metrics for each testId
            try:
                insert_to_db = [] #list which will be inserted into InfluxDB

                r = requests.request('GET', f"{config.base_url}/{te_test_type}/{te_test['testId']}", headers=headers,params=params)
                resp = r.json()
                r.raise_for_status()

                if r.status_code == 200:
                    logging.info(f"{te_test['testName']}: Getting data...")
                    insert_to_db.extend(parsing_function(resp,te_test['testId'],te_test['testName']))

                    #pagination
                    while "next" in resp["pages"]:
                        logging.info(f"{te_test['testName']}: ...data on next page...")
                        r = requests.request('GET', resp["pages"]["next"], headers=headers)
                        resp = r.json()
                        insert_to_db.extend(parsing_function(resp,te_test['testId'],te_test['testName']))

                    # add the final list as a batch to influx db
                    # _insert_to_influx_v2(insert_to_db, te_test['testName'])
                    http_server_net_metrics(insert_to_db)
                else:
                    logging.warning(f"Response of {te_test['testName']} was not 200.")
                    
            except Exception as e:
                logging.exception(f"Error when getting data from test {te_test['testName']}: {e}")
        
        logging.info(f" === Success! Got ALL test data of type {te_test_type}. === ")

    except Exception as e:
        logging.exception(f"Error when iterating through the {te_test_type} tests: {e}")

def get_all_http_server_tests(window):
    #get_test_data_insert_to_db(all_tests["http-server"],"web/http-server",_parse_and_convert_http_server,window)
    get_test_data_insert_to_db(all_tests["http-server"],"net/metrics",_parse_and_convert_end_to_end,window)
    #get_test_data_insert_to_db(all_tests["http-server"],"net/path-vis",_parse_and_convert_path_vis,window)

def get_all_page_load_tests(window):
    get_test_data_insert_to_db(all_tests["page-load"],"web/page-load",_parse_and_convert_page_load,window)
    get_test_data_insert_to_db(all_tests["page-load"],"web/http-server",_parse_and_convert_http_server,window)
    get_test_data_insert_to_db(all_tests["page-load"],"net/metrics",_parse_and_convert_end_to_end,window)
    get_test_data_insert_to_db(all_tests["page-load"],"net/path-vis",_parse_and_convert_path_vis,window)

def get_all_agent_server_tests(window):
    get_test_data_insert_to_db(all_tests["agent-to-server"],"net/metrics",_parse_and_convert_end_to_end,window)
    get_test_data_insert_to_db(all_tests["agent-to-server"],"net/path-vis",_parse_and_convert_path_vis,window)

def get_all_agent_agent_tests(window):
    get_test_data_insert_to_db(all_tests["agent-to-agent"],"net/metrics",_parse_and_convert_end_to_end,window)
    get_test_data_insert_to_db(all_tests["agent-to-agent"],"net/path-vis",_parse_and_convert_path_vis,window)


def http_server_net_metrics(data):

    for result in data:
        json_results['json_input_1000eye_http_server_net_metrics_loss']['values'].append(
            {
                'value': result['fields']['loss'],
                'labels': [str(result['measurement']), result['tags']['testName'], result['tags']['agentName'], result['tags']['m_serverIp']]
            }
        )
        json_results['json_input_1000eye_http_server_net_metrics_jitter']['values'].append(
            {
                'value': result['fields']['jitter'],
                'labels': [str(result['measurement']), result['tags']['testName'], result['tags']['agentName'], result['tags']['m_serverIp']]
            }
        )
        json_results['json_input_1000eye_http_server_net_metrics_maxLatency']['values'].append(
            {
                'value': result['fields']['maxLatency'],
                'labels': [str(result['measurement']), result['tags']['testName'], result['tags']['agentName'], result['tags']['m_serverIp']]
            }
        )
        json_results['json_input_1000eye_http_server_net_metrics_avgLatency']['values'].append(
            {
                'value': result['fields']['avgLatency'],
                'labels': [str(result['measurement']), result['tags']['testName'], result['tags']['agentName'], result['tags']['m_serverIp']]
            }
        )
        json_results['json_input_1000eye_http_server_net_metrics_minLatency']['values'].append(
            {
                'value': result['fields']['minLatency'],
                'labels': [str(result['measurement']), result['tags']['testName'], result['tags']['agentName'], result['tags']['m_serverIp']]
            }
        )
    





if __name__ == "__main__":
    # time.sleep(60) #wait until InfluxDB and Grafana are ready
    logging.info(f"Starting! Getting data from TE API.")

    # # getting all data or just specific?
    if config.enable_label_specific == 1:
        all_tests = get_tests_by_label()
    # else:
    #     all_tests = get_tests_by_type()

    print(all_tests)
    # get historic data only if they are specified
    if "http-server" in all_tests:
        #get_all_http_server_tests(config.window)
        get_all_http_server_tests("latest")
    
    # if "page-load" in all_tests:
    #     get_all_page_load_tests(config.window)

    # if "agent-to-server" in all_tests:
    #     get_all_agent_server_tests(config.window)

    # if "agent-to-agent" in all_tests:
    #     get_all_agent_agent_tests(config.window)

    # logging.info(" === Success! Got ALL HISTORIC test data. Pulling new data now... === ")

    # # endless loop for pulling new data every x seconds
    # while True:
    #     time.sleep(config.interval)

    #     # get new data only if they are specified
    #     if "http-server" in all_tests:
    #         get_all_http_server_tests("latest")

    #     if "page-load" in all_tests:
    #         get_all_page_load_tests("latest")

    #     if "agent-to-server" in all_tests:
    #        get_all_agent_server_tests("latest")

    #     if "agent-to-agent" in all_tests:
    #        get_all_agent_agent_tests("latest")

    #     logging.info("Pulled new data.")

    with open('1000eye.json', 'w', encoding='utf-8') as f_json:
        json.dump(list(json_results.values()), f_json, ensure_ascii=False, indent=4)

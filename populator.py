#!/usr/bin/python3
import requests
import argparse
import json
import random


parser = argparse.ArgumentParser(description='Create a customizable number of services, rules, applications, plans')
parser.add_argument('--url',type=str,
                    help='Base URL of the admin portal (including protocol)', required=True)
parser.add_argument('--token',type=str,
                    help='A personal access token with RW permission on URL', required=True)
parser.add_argument('--services', type=int, help='Number of services', default=1)
parser.add_argument('--apps', type=int, help='Number of applications', default=1)
parser.add_argument('--rules', type=int, help='Number of rules', default=1)
parser.add_argument('--plans', type=int, help='Number of application plans', default=1)
args = parser.parse_args()

base_url = args.url
access_token = args.token
n_services = args.services
n_plans = args.plans
n_rules = args.rules
n_applications = args.apps
base_name = 'fakeservice'



for i in range(n_services):
    service_name = base_name + '_{0:04}'.format(i)
    #Create Service
    req = requests.post(
        base_url + "/admin/api/services.json", 
        data = {'access_token': access_token, 'name': service_name, 'deployment_option': 'self_managed', 'backend_version': 1,
        'system_name': service_name})
    ret = json.loads(req.text)
    service_id = ret["service"]["id"]
    print("Service {0} created".format(service_id))

    #Create Metric
    req = requests.post(
        base_url + "/admin/api/services/{0}/metrics.json".format(service_id),
        data={'access_token': access_token, 'unit': 'hits', 'friendly_name': service_name + '_hits'})
    ret = json.loads(req.text)
    metric_id = ret["metric"]["id"]
    print("Metric {0} created".format(metric_id))

    #Create Mapping rules
    for j in range(n_rules):
        req = requests.post(
            base_url + "/admin/api/services/{0}/proxy/mapping_rules.json".format(service_id),
            data={'access_token': access_token, 'http_method': 'PUT', 'pattern': "/{0}/{1}/".format(service_name, j), 'metric_id': metric_id, 'delta': 1})
        ret = json.loads(req.text)
        print("Mapping rule {0} created".format(ret["mapping_rule"]["id"]))
    
    plan_ids = []
    for j in range(n_plans):
        req = requests.post(
            base_url + "/admin/api/services/{0}/application_plans.json".format(service_id),
            data={'access_token': access_token, 'name': service_name + "_plan_{0:03}".format(j), 'approval_required': 'false', 'state_event': 'publish'})
        ret = json.loads(req.text)
        print("Application plan {0} created".format(ret["application_plan"]["id"]))
        plan_ids.append(ret["application_plan"]["id"])
    
    #Get account ids
    req = requests.get(base_url + "/admin/api/accounts.json", data = {"access_token": access_token})
    ret = json.loads(req.text)
    account_ids = []
    for account in ret["accounts"]:
        account_ids.append(account["account"]["id"])

    #Create applications
    for j in range(n_applications):
        req = req = requests.post(
            base_url + "/admin/api/accounts/{0}/applications.json".format(random.choice(account_ids)),
            data={'access_token': access_token, 'plan_id': random.choice(plan_ids), 'name': "{0}_app_{1:03}".format(service_name, j), 'description': 'This is a description'})
        ret = json.loads(req.text)
        print("Application {0} created for account {1} with plan {2}".format(
            ret["application"]["id"], ret["application"]["account_id"], ret["application"]["plan_id"]))

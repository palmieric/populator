#!/usr/bin/python3
import requests
import argparse
import json
import random
import re
import time


class URLValidator(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if not re.match("^(https?):/{2}", values):
            raise ValueError("URL must include {http|https}")
        setattr(namespace, self.dest, values)


def dump_log(failed=[]):
    """Create a reusable logfile to continue or rollback a populator execution

    Args:
        failed (list, optional): The list of failed objects creation.
        Defaults to [].
    """
    dump = {'url': base_url,
            'access_token': access_token,
            'service_ids': service_ids,
            'failed': failed}

    with open('populator.{0}.log'.format(time.time()), 'w') as f:
        json.dump(dump, f)


def rollback(service_ids):
    """Roll back the execution of populator

    Args:
        service_ids (list of integer): the list of services to delete
    """
    failed = set()
    for id in service_ids:
        # /admin/api/services/{id}.xml
        retry = 0
        while retry < 5:
            time.sleep(5 * retry)
            req = requests.delete(
                base_url + "/admin/api/services/{0}.json".format(id), data={
                    'access_token': access_token}, verify=args.insecure)
            if req.ok:
                print("Service {0} deleted".format(id))
                failed.discard(id)
            else:
                print("Cannot delete service: {0}: [{1}]". format(
                    id, req.status_code))
                retry += 1
                print("Will wait {0} seconds then try again. {1} "
                      "retries remaining.".format(5 * retry, 5 - retry))
                failed.add(id)
    if len(failed):
        print("Cannot delete services: {0}". format(failed))
    else:
        print("All services deleted")

    dump_log(failed)


def failure(req, obj_type, service_ids):
    """Print information about an incurred failure

    Args:
        req (request): the request object
        obj_type (string): the object type failed to create
        service_ids (integer): the service id the object belongs
    """
    print("Cannot create {0}: [{1}] {2}". format(
        obj_type, req.status_code, req.text))
    if args.failure_rollback:
        rollback(service_ids)
    exit()


requests.packages.urllib3.disable_warnings(
        requests.packages.urllib3.exceptions.InsecureRequestWarning)

parser = argparse.ArgumentParser(
    description='Create a customizable number of services, rules, '
    'applications, plans')
parser.add_argument(
    '-u', '--url', type=str, action=URLValidator,
    help='Base URL of the admin portal (including protocol http(s)://)',
    required=True)
parser.add_argument(
    '-t', '--token', type=str,
    help='A personal access token with RW permission on URL', required=True)
parser.add_argument(
    '-s', '--services', type=int, help='Number of services', default=1)
parser.add_argument(
    '-a', '--apps', type=int, help='Number of applications', default=1)
parser.add_argument(
    '-r', '--rules', type=int, help='Number of rules', default=1)
parser.add_argument(
    '-p', '--plans', type=int, help='Number of application plans', default=1)
parser.add_argument(
    '-k', '--insecure', help='Insecure connections', action='store_false')
parser.add_argument(
    '-n', '--service-name', type=str, help='Service base name',
    default="fakesvc")
parser.add_argument(
    '-f', '--failure-rollback', type=bool,
    help='Rollback on failure, default to False', default=False)
parser.add_argument(
    '-S', '--save-status', type=bool,
    help='Save the status of the execution to revert it later', default=False)


args = parser.parse_args()
base_url = args.url
access_token = args.token
n_services = args.services
n_plans = args.plans
n_rules = args.rules
n_applications = args.apps
base_name = args.service_name


# Get account ids
req = requests.get(base_url + "/admin/api/accounts.json", data={
    "access_token": access_token}, verify=args.insecure)
if not req.ok:
    print("Cannot get the accounts: {0}: {1}", req.status_code, req.text)
    exit()
account_ids = []
service_ids = []

for account in req.json()["accounts"]:
    account_ids.append(account["account"]["id"])

for i in range(n_services):
    service_name = base_name + '_{0:04}'.format(i)
    # Create Service
    req = requests.post(
        base_url + "/admin/api/services.json", data={
            'access_token': access_token, 'name': service_name,
            'deployment_option': 'self_managed',
            # ver < 2.5 doesn't have 'deployment_option'
            'backend_version': 1,
            'system_name': service_name}, verify=args.insecure)
    if req.ok:
        ret = req.json()
        service_id = ret["service"]["id"]
        service_ids.append(service_id)
        print("Service {0} created".format(service_id))
    else:
        failure(req, 'service', service_ids)

    # Create Metric
    req = requests.post(
        base_url + "/admin/api/services/{0}/metrics.json".format(service_id),
        data={
            'access_token': access_token, 'unit': 'hits',
            'friendly_name': service_name + '_hits'}, verify=args.insecure)
    if req.ok:
        ret = req.json()
        metric_id = ret["metric"]["id"]
        print("Metric {0} created".format(metric_id))
    else:
        failure(req, 'metric', service_ids)

    # Create Mapping rules
    for j in range(n_rules):
        req = requests.post(
            base_url + "/admin/api/services/{0}"
            "/proxy/mapping_rules.json".format(service_id), data={
                'access_token': access_token, 'http_method': 'PUT',
                'pattern': "/{0}/{1}/".format(service_name, j),
                'metric_id': metric_id, 'delta': 1},
            verify=args.insecure)
        if req.ok:
            ret = req.json()
            print("Mapping rule {0} created".format(ret["mapping_rule"]["id"]))
        else:
            failure(req, 'mapping rule', service_ids)

    plan_ids = []
    for j in range(n_plans):
        req = requests.post(
            base_url + "/admin/api/services/{0}/"
            "application_plans.json".format(service_id), data={
                'access_token': access_token,
                'name': service_name + "_plan_{0:03}".format(j),
                'approval_required': 'false', 'state_event': 'publish'},
            verify=args.insecure)
        ret = req.json()
        if req.ok:
            print("Application plan {0} created".format(
                ret["application_plan"]["id"]))
            plan_ids.append(ret["application_plan"]["id"])
        else:
            failure(req, 'application plan', service_ids)

    # Create applications
    for j in range(n_applications):
        req = requests.post(
            base_url + "/admin/api/accounts/{0}/applications.json".format(
                random.choice(account_ids)),
            data={
                'access_token': access_token,
                'plan_id': random.choice(plan_ids),
                'name': "{0}_app_{1:03}".format(service_name, j),
                'description': 'This is a description'}, verify=args.insecure)
        ret = req.json()
        if req.ok:
            print(
                "Application {0} created for account {1} with plan {2}".
                format(ret["application"]["id"], ret["application"][
                    "account_id"], ret["application"]["plan_id"]))
        else:
            failure(req, 'application plan', service_ids)

if args.save_status:
    dump_log()

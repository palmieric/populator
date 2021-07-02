# populator

An utility to populate a 3scale instance with synthetic data. The tool will create:

- **N** services (default: 1)
- **1** metric per service
- **N** backends per service (default: 1)
- **N** rules per service (default: 1)
- **N** application plans per service (default: 1)
- **N** application per service (default: 1)

**Populator** will create the applications under a (random) already existent account picking one of the application plan created.

## Known issues

- The services are not promoted to staging neither production
- The services are not intended to be consistent or working
- It doesn't work with 3scale amp <= 2.5

## Install and run

The only requirement is to have python3 installed.

To run **populator**:

- clone the repo:
  - `git clone <https://github.com/palmieric/populator.git>`

- cd into the directory:
  - `cd populator`
- install the requirements:
  - `python3 -m pip install -r requirements.txt [--user]`
- run:
  - `/populator.py --help`  
    or  
    `python3 populator.py --help`

## Usage

~~~bash
usage: populator.py [-h] -u URL -t TOKEN [-s SERVICES] [-b BACKENDS] [-a APPS]
                    [-r RULES] [-p PLANS] [-n SERVICE_NAME] [-k] [-f] [-S]

Create a customizable number of services, rules, applications, plans

optional arguments:
  -h, --help            show the help message and exit
  -u URL, --url URL     Base URL of the admin portal (including protocol
                        http(s)://)
  -t TOKEN, --token TOKEN
                        A personal access token with RW permission on URL
  -s SERVICES, --services SERVICES
                        Number of services
  -b BACKENDS, --backends BACKENDS
                        Number of backends per service
  -a APPS, --apps APPS  Number of applications
  -r RULES, --rules RULES
                        Number of rules
  -p PLANS, --plans PLANS
                        Number of application plans
  -n SERVICE_NAME, --service-name SERVICE_NAME
                        Service base name
  -k, --insecure        Insecure connections
  -f, --failure-rollback
                        Rollback on failure, default to False
  -S, --save-status     Save the status of the execution to revert it later

~~~

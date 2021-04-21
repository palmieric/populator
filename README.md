# populator

An utility to populate a 3scale instance with synthetic data. The tool will create:

- **N** services (default: 1)
- **1** metric per service
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
  - git clone <https://github.com/palmieric/populator.git>

- cd into the directory:
  - cd populator
- install the requirements:
  - python3 -m pip install -r requirements.txt [--user]
- run:
  - /populator.py --help or python3 populator.py --help

## Usage

~~~bash
usage: populator.py [-h] --url URL --token TOKEN [--services SERVICES]
                    [--apps APPS] [--rules RULES] [--plans PLANS] [-k]
                    [--service-name SERVICE_NAME]
                    [--failure-rollback FAILURE_ROLLBACK]
                    [--save-status SAVE_STATUS]

Create a customizable number of services, rules, applications, plans

optional arguments:
  -h, --help            show this help message and exit
  --url URL             Base URL of the admin portal(including protocol
                        http(s)://)
  --token TOKEN         A personal access token with RW permission on URL
  --services SERVICES   Number of services
  --apps APPS           Number of applications
  --rules RULES         Number of rules
  --plans PLANS         Number of application plans
  -k                    Insecure connections
  --service-name SERVICE_NAME
                        Service base name
  --failure-rollback FAILURE_ROLLBACK
                        Rollback on failure, default to False
  --save-status SAVE_STATUS
                        Save the status of the execution to revert it later
~~~

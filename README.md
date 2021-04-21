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
  - git clone https://github.com/palmieric/populator.git

- cd into the directory:
  - cd populator
- install the requirements:
  - python3 -m pip install -r requirements.txt [--user]
- run:
  - /populator.py --help or python3 populator.py --help

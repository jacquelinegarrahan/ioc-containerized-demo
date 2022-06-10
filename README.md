# Demo of containerized programmatic EPICS IOC

For the SDF-based Online Modeling Service, our hosted IOCs will serve pvAccess pvs ONLY.

## IOC

For the SDF-based Online Modeling Service, our hosted IOCs will serve pvAccess pvs ONLY. The code packaged in the `ioc/demo-containerized-ioc/demo_server` subdir is flexible enough to host two, which was self-serving in that this code will serve as a skeleton for updating the [`lume-epics`](https://github.com/slaclab/lume-epics) package for implementing the templated output IOCs. 

I used mambaforge's minimal Ubuntu-focal-based [image base](https://github.com/conda-forge/miniforge-images/blob/master/ubuntu/Dockerfile), and created an environment using the conda YAML spec in `ioc/environment.yml`. The pvAcess package p4p release on conda-forge is pinned to a max of Python 3.8, but p4p itself is now built against Python through 3.10. I'm going to work with devs to update the conda-forge release so we can migrate to newer Python. 3.8 is perfectly fine for now (as far as I know)...

To build IOC:
```
docker build -t demo-ioc ioc
```
To build client:
```
docker build -t demo-client client
```

### Running the pvAccess Dockerized IOC




### Running the Channel Access IOC
Because the client will read EPICS Channel Access pvs, a second ioc has been packaged with this example. First set up the environment:
```
conda env create -f ioc/environment.yml
conda activate ioc-demo
pip install -e ioc/demo-containerized-ioc/setup.py
```

Next, run with appropriate EPICS_CA environment variables set (described below):
```
python ioc/example_ca_ioc.py
```


## Dockerized client
The client packages epics-base using the same mambaforge base image. EPICS cli commands can be executed inside the container shell. To run:

```
docker run -e EPICS_CA_ADDR_LIST=host.docker.internal -i -t demo-client
```


### Environment variables
The `demo_server` package uses [`caproto`](https://nsls-ii.github.io/caproto/servers.html) for Channel Access [`p4p`](https://github.com/mdavidsaver/p4p) for pvAccess. Each respect the typical EPICS environment variables, `EPICS_CA_` and `EPICS_PVAS_` prefixed. Descriptions for env var function for Channel Access can be found [here](https://epics.anl.gov/EpicsDocumentation/AppDevManuals/ChannelAccess/cadoc_4.htm). Descriptions for pvAccess variables can be found [here](https://mdavidsaver.github.io/pvxs/netconfig.html).


| Protocol                      | Variables                      |
|-------------------------------|--------------------------------|
| Channel Access                | EPICS_CA_ADDR_LIST             |
|                               | EPICS_CA_AUTO_ADDR_LIST        |
|                               | EPICS_CA_CONN_TMO              |
|                               | EPICS_CA_BEACON_PERIOD         |
|                               | EPICS_CA_REPEATER_PORT         |
|                               | EPICS_CA_SERVER_PORT           |
|                               | EPICS_CA_MAX_ARRAY_BYTES       |
|-------------------------------|--------------------------------|
| pvAccess                      | EPICS_PVAS_ADDR_LIST           |
|                               | EPICS_PVAS_AUTO_ADDR_LIST      |
|                               | EPICS_PVAS_CONN_TMO            |
|                               | EPICS_PVAS_BEACON_PERIOD       |
|                               | EPICS_PVAS_SERVER_PORT         |


Without set variables, the IOC will run on the defaults. 

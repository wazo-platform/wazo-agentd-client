# xivo-agentd-client

[![Build Status](https://jenkins.wazo.community/buildStatus/icon?job=xivo-agentd-client)](https://jenkins.wazo.community/job/xivo-agentd-client)

A python library to access the REST API of xivo-agentd.

## Usage

```python
from xivo_agentd_client import Client

c = Client('agentd.example.com')

agent_status = c.agents.get_agent_status_by_number('1002')
```


Running unit tests
------------------

```
apt-get install libpq-dev python-dev libffi-dev libyaml-dev
pip install tox
tox --recreate -e py27
```

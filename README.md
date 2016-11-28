# xivo-agentd-client

[![Build Status](https://travis-ci.org/wazo-pbx/xivo-agentd-client.svg?branch=master)](https://travis-ci.org/wazo-pbx/xivo-agentd-client)

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

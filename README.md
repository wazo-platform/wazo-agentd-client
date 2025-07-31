# wazo-agentd-client

[![Build Status](https://jenkins.wazo.community/buildStatus/icon?job=wazo-agentd-client)](https://jenkins.wazo.community/job/wazo-agentd-client)

A python library to access the REST API of wazo-agentd.

## Usage

```python
from wazo_agentd_client import Client

c = Client('agentd.example.com')

c.agents.add_agent_to_queue(agent_id=12, queue_id=13)
c.agents.remove_agent_from_queue(agent_id=12, queue_id=13)

queues = c.agents.list_queues(agent_id=12)
queues = c.agents.list_queues_by_number(agent_number='1234')
queues = c.agents.list_user_queues()

c.agents.login_agent(agent_id=12, extension='5678', context='internal')
c.agents.logoff_agent(agent_id=12)

c.agents.login_agent_by_number(agent_number='1234', extension='5678', context='internal')
c.agents.logoff_agent_by_number(agent_number='1234')

c.agents.logoff_all_agents()
c.agents.relog_all_agents()

c.agents.pause_agent_by_number(agent_number='1234')
c.agents.unpause_agent_by_number(agent_number='1234')

c.agents.login_user_agent(line_id=1)
c.agents.pause_user_agent()
c.agents.unpause_user_agent()
c.agents.logoff_user_agent()
c.agents.get_user_agent_status()

status = c.agents.get_agent_status(agent_id=12)
status = c.agents.get_agent_status_by_number(agent_number='1234')
status = c.agents.get_agent_statuses()

print(status.id)
print(status.number)
print(status.origin_uuid)
print(status.logged)
print(status.extension)
print(status.context)
print(status.state_interface)
print(status.paused)
print(status.paused_reason)
```


## Running unit tests

```
apt-get install libpq-dev python3-dev libffi-dev libyaml-dev
pip install tox
tox --recreate -e py39
```

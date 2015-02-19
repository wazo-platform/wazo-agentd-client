XiVO agentd client
=================
[![Build Status](https://travis-ci.org/xivo-pbx/xivo-agentd-client.svg?branch=master)](https://travis-ci.org/xivo-pbx/xivo-agentd-client)

A python library to connect to xivo-agentd.

Usage:

```python
from xivo_agentd_client import Client

c = Client('agentd.example.com')

agent_status = c.agents.get_agent_status(4)
```

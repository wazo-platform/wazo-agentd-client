#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2015 Avencall
# SPDX-License-Identifier: GPL-3.0-or-later

from setuptools import setup
from setuptools import find_packages

setup(
    name='xivo-agentd-client',
    version='0.1.1',

    description='a simple client library for the xivo-agentd HTTP interface',

    author='Wazo Authors',
    author_email='dev.wazo@gmail.com',

    url='http://wazo.community',

    packages=find_packages(),

    entry_points={
        'agentd_client.commands': [
            'agents = xivo_agentd_client.commands.agents:AgentsCommand',
        ],
    }
)

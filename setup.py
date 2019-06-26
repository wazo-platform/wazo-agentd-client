#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2015-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from setuptools import setup
from setuptools import find_packages

setup(
    name='wazo-agentd-client',
    version='0.1.1',

    description='a simple client library for the wazo-agentd HTTP interface',

    author='Wazo Authors',
    author_email='dev.wazo@gmail.com',

    url='http://wazo.community',

    packages=find_packages(),

    entry_points={
        'agentd_client.commands': [
            'agents = wazo_agentd_client.commands.agents:AgentsCommand',
        ],
    }
)

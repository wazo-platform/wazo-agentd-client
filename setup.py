#!/usr/bin/env python3

# Copyright 2015-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from setuptools import find_packages, setup

setup(
    name='wazo-agentd-client',
    version='0.1.1',
    description='a simple client library for the wazo-agentd HTTP interface',
    author='Wazo Authors',
    author_email='dev.wazo@gmail.com',
    url='http://wazo.community',
    packages=find_packages(),
    entry_points={
        'wazo_agentd_client.commands': [
            'agents = wazo_agentd_client.commands.agents:AgentsCommand',
            'status = wazo_agentd_client.commands.status:StatusCommand',
        ],
    },
)

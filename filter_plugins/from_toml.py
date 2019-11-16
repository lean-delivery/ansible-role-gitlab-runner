#!/usr/bin/python3

DOCUMENTATION = '''
---
module: to_toml, from_toml
version_added: "2.8"
short_description: Converts Python data to TOML and TOML to Python data.
author:
    - "Samy Coenen (contact@samycoenen.be)"
'''

from toml import toml

def to_toml(data):
    ''' Convert the value to TOML '''
    return toml.dumps(data)

def from_toml(data):
    ''' Convert TOML to Python data '''
    return toml.loads(data)

class FilterModule(object):
    ''' Ansible TOML jinja2 filters '''

    def filters(self):
        return {
            # toml
            'to_toml': to_toml,
            'from_toml': from_toml
        }
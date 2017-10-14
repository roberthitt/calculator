"""
Module for loading config files.
"""

from collections import namedtuple

import yaml
import numpy as np


class Configuration():
    """
    Class for loading YAML config file.
    """

    OpInfo = namedtuple('Operator', 'precedence assoc operation operand_count')

    def __init__(self, config_path):
        """
        Load YAML config file.

        Args:
            config_path: file path of config file
        """

        with open(config_path, 'r') as stream:
            data = yaml.load(stream)

            self.ops = {op['symbol']: self.create_op_info(op)
                        for op in data['operators']}
            print(self.ops)

    def create_op_info(self, op_dict):
        """
        Creates a namedtuple from the given dict.

        args:
            op_dict: dictionary to be parsed.

        returns:
            namedtuple with the parsed data
        """

        return self.OpInfo(precedence=op_dict['precedence'],
                           assoc=op_dict['assoc'],
                           operation=getattr(np, op_dict['operation']),
                           operand_count=op_dict['operand_count'])


c = Configuration('config.yaml')

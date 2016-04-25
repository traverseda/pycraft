from collections import OrderedDict

import pytest
import yaml


class SequentialLoader(yaml.Loader):
    """
    Loads and holds data in an ordered dictionary to preserve data sequence

    Note that this is probably not necessary for python 3, but it is
    necessary for python 2 and pypy.
    """
    container = OrderedDict

    def __init__(self, *args, **kwds):
        yaml.Loader.__init__(self, *args, **kwds)
        self.add_constructor(u'tag:yaml.org,2002:map', type(self).construct_yaml_map)
        self.add_constructor(u'tag:yaml.org,2002:omap', type(self).construct_yaml_map)

    def construct_yaml_map(self, node):
        data = self.container()
        yield data
        value = self.construct_mapping(node)
        data.update(value)

    def construct_mapping(self, node, deep=None):
        if isinstance(node, yaml.MappingNode):
            self.flatten_mapping(node)
        else:
            if hasattr(node, 'id') and hasattr(node, 'start_mark'):
                error = 'expected a mapping node, but found {}'.format(node.id)
                raise yaml.constructorConstructorError(None, None, error, node.start_mark)
            else:
                error = 'Invalid type for node variable: {} - {}'.format(type(node), node)
                raise TypeError(error)

        mapping = self.container()
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            try:
                hash(key)
            except TypeError as e:
                raise yaml.constructorConstructorError(
                    'while constructing a mapping',
                    node.start_mark,
                    'found unacceptable key ({})'.format(e),
                    key_node.start_mark
                )
            value = self.construct_object(value_node, deep=deep)
            mapping[key] = value
        return mapping


def pytest_addoption(parser):
    parser.addoption("--stress", action="store_true", help="run stress tests")


@pytest.fixture(scope="module")
def options():
    """Captures configuration data from config file and validates that
    data is available"""
    import yaml
    import os

    config_file = os.path.realpath(os.path.join(os.path.dirname(__file__), 'config.yaml'))
    assert os.path.exists(config_file)
    with open(config_file, 'r') as fd:
        config = yaml.load(fd.read(), SequentialLoader)

    return config

import os
from yaml import load as yamlload
from yaml.reader import Reader
from yaml.scanner import Scanner
from yaml.parser import Parser
from yaml.composer import Composer
from yaml.resolver import Resolver
from yaml.constructor import Constructor


class YamlConstructor(Constructor):
    def construct_os_env(self, node):
        return os.environ.get(self.construct_scalar(node))

    def construct_os_expandvars(self, node):
        f = os.path.expandvars(self.construct_scalar(node))
        return f


YamlConstructor.add_constructor('tag:yaml.org,2002:os/env', YamlConstructor.construct_os_env)
YamlConstructor.add_constructor('tag:yaml.org,2002:os/expandvars', YamlConstructor.construct_os_expandvars)


class YamlLoader(Reader, Scanner, Parser, Composer, YamlConstructor, Resolver):
    def __init__(self, stream):
        Reader.__init__(self, stream)
        Scanner.__init__(self)
        Parser.__init__(self)
        Composer.__init__(self)
        YamlConstructor.__init__(self)
        Resolver.__init__(self)


def load(stream, Loader=YamlLoader):
    return yamlload(stream=stream, Loader=Loader)

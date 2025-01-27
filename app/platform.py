#!/usr/bin/env python
# _*_ coding:utf-8 _*_


class ManageProcessor(object):
    PLUGINS = {}

    def process(self, ip, port, plugins=()):
        if plugins is ():
            for plugin_name in self.PLUGINS.keys():
                try:
                    print(Color.OKYELLOW + "[*]", plugin_name + Color.ENDC)
                    self.PLUGINS[plugin_name]().process(ip, port)
                except:
                    print(Color.WARNING + "[-]{}".format(plugin_name) + Color.ENDC)
        else:
            for plugin_name in plugins:
                try:
                    print("[*]", self.PLUGINS[plugin_name])
                    self.PLUGINS[plugin_name]().process(ip, port)
                except:
                    print("[-]{}".format(self.PLUGINS[plugin_name]))
        return

    @classmethod
    def plugin_register(cls, plugin_name):
        def wrapper(plugin):
            cls.PLUGINS.update({plugin_name: plugin})
            return plugin

        return wrapper


class Color:
    HEADER = '\033[95m'
    FAIL = '\033[90m'
    OKGREEN = '\033[92m'
    OKYELLOW = '\33[93m'
    WARNING = '\033[91m'
    OKBLUE = '\033[91m'
    ENDC = '\033[0m'

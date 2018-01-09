# plugins.py
import os
import importlib
import sys
sys.path.append('.')

pluginDir = 'plugins'

def dynamic_import(pluginfile):
    return importlib.import_module(pluginfile)

def getPluginNames(pluginDir):
    return os.listdir(pluginDir)

def loadPlugins():
    plugins = []
    for pluginName in getPluginNames(pluginDir):
        sys.path.append(pluginDir+"/"+pluginName)
        plugins.append(dynamic_import(pluginName))
    return plugins

### Testing ###
def printPlugin(plugin):
    print("{:34}".format(plugin.details()['name']) +
          "{:14}".format(plugin.details()["section"]) +
          "{:50}".format(plugin.details()["description"]) +
          "{:<12}".format(plugin.details()["version"])
    )

if __name__ == '__main__':
    # Load Plugins
    pluginList = loadPlugins()

    for plugin in pluginList:
        printPlugin(plugin)

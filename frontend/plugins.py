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
    plugins = {}
    for pluginName in getPluginNames(pluginDir):
        sys.path.append(pluginDir+"/"+pluginName)
        plugin          = dynamic_import(pluginName)
        plugin.id       = pluginName
        plugin.enabled  = False
        plugins[pluginName] = plugin
    return plugins

### Testing ###
def printPlugin(plugin):
    print("{:30}".format(plugin.id) +
          "{:34}".format(plugin.details()['name']) +
          "{:14}".format(plugin.details()["section"]) +
          "{:50}".format(plugin.details()["description"]) +
          "{:<12}".format(plugin.details()["version"])
    )

if __name__ == '__main__':
    # Load Plugins
    pluginMap = loadPlugins()

    for plugin in pluginMap.values():
    pluginList = loadPlugins()

    for plugin in pluginList: 
        printPlugin(plugin)

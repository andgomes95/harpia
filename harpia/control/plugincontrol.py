# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
"""
This module contains the PortControl class.
"""
import ast
import os
import inspect  # For module inspect
import pkgutil  # For dynamic package load
from os.path import expanduser
from harpia.utils.XMLUtils import XMLParser
from harpia.utils.PythonUtils import PythonParser
from harpia.model.plugin import Plugin

class PluginControl():
    """
    This class contains methods related the PortControl class.
    """

    # ----------------------------------------------------------------------

    def __init__(self):
        pass

    # ----------------------------------------------------------------------
    @classmethod
    def load(cls, file_name):
        """
        This method loads the plugin from XML file.

        Returns:

            * **Types** (:class:`boolean<boolean>`)
        """
        if os.path.exists(file_name) is False:
            return
        parser = XMLParser(file_name)

        if parser.getTag("HarpiaPlugin") is None:
            return None

        plugin = Plugin()

        plugin.type = parser.getTagAttr("HarpiaPlugin", "type")
        plugin.language = parser.getTagAttr("HarpiaPlugin", "language")
        plugin.framework = parser.getTagAttr("HarpiaPlugin", "framework")

        plugin.label = parser.getTagAttr("HarpiaPlugin", "label")
        plugin.group = parser.getTagAttr("HarpiaPlugin", "group")
        plugin.color = parser.getTagAttr("HarpiaPlugin", "color")
        plugin.help = parser.getTagAttr("HarpiaPlugin", "help")
        plugin.source = parser.getTagAttr("HarpiaPlugin", "source")

        count = 0
        for code in plugin.codes:
            plugin.codes[count] = parser.getTag("HarpiaPlugin").getTag("code" + str(count)).getText()
            count = count + 1

        props = parser.getTag("HarpiaPlugin").getTag(
                    "properties").getChildTags("property")
        for prop in props:
            plugin.properties.append(ast.literal_eval(prop.getAttr("value")))

        in_ports = parser.getTag("HarpiaPlugin").getTag(
                    "in_ports").getChildTags("port")
        for port in in_ports:
            plugin.in_ports.append(ast.literal_eval(port.getAttr("value")))

        out_ports = parser.getTag("HarpiaPlugin").getTag(
                    "out_ports").getChildTags("port")
        for port in out_ports:
            plugin.out_ports.append(ast.literal_eval(port.getAttr("value")))

        if plugin.type == "harpia.model.plugin":
            return None
        return plugin

    # ----------------------------------------------------------------------
    @classmethod
    def save(cls, plugin):
        """
        This method save the plugin in user space.

        Returns:

            * **Types** (:class:`boolean<boolean>`)
        """
        from harpia.system import System
        plugin.source = "xml"
        parser = XMLParser()
        main = parser.addTag('HarpiaPlugin')
        parser.setTagAttr('HarpiaPlugin','type', plugin.type)
        parser.setTagAttr('HarpiaPlugin','language', plugin.language)
        parser.setTagAttr('HarpiaPlugin','framework', plugin.framework)

        parser.setTagAttr('HarpiaPlugin','label', plugin.label)
        parser.setTagAttr('HarpiaPlugin','group', plugin.group)
        parser.setTagAttr('HarpiaPlugin','color', plugin.color)
        parser.setTagAttr('HarpiaPlugin','help', plugin.help)
        parser.setTagAttr('HarpiaPlugin','source', plugin.source)

        count = 0
        for code in plugin.codes:
            parser.appendToTag('HarpiaPlugin', 'code' + str(count)).string = str(plugin.codes[count])
            count = count + 1

        parser.appendToTag('HarpiaPlugin', 'properties')
        for key in plugin.properties:
            parser.appendToTag('properties', 'property', value=key)

        parser.appendToTag('HarpiaPlugin', 'in_ports')
        for key in plugin.in_ports:
            parser.appendToTag('in_ports', 'port', value=key)

        parser.appendToTag('HarpiaPlugin', 'out_ports')
        for key in plugin.out_ports:
            parser.appendToTag('out_ports', 'port', value=key)

        try:
            data_dir = System.get_user_dir() + "/extensions/"
            data_dir = data_dir + plugin.language + "/" + plugin.framework + "/"
            if not os.path.isdir(data_dir):
                try:
                    os.makedirs(data_dir)
                except:
                    pass
            file_name = data_dir + plugin.type + ".xml"
            plugin_file = file(os.path.expanduser(file_name), 'w')
            plugin_file.write(parser.getXML())
            plugin_file.close()
        except IOError as e:
            return False
        return True
    # ----------------------------------------------------------------------
    @classmethod
    def save_python(cls, plugin):
        """
        This method save the port in user space in python extension.

        Returns:

            * **Types** (:class:`boolean<boolean>`)
        """
        from harpia.system import System
        parser = PythonParser()

        parser.class_name = plugin.label.replace(' ', '')
        parser.dependencies = [{'from':'harpia.model.plugin', 'import':'Plugin'}]
        parser.inherited_classes = ['Plugin']
        parser.setAttribute('id', plugin.id)
        parser.setAttribute('type', plugin.type)
        parser.setAttribute('language', plugin.language)
        parser.setAttribute('framework', 'python')
        parser.setAttribute('source', plugin.source)
        parser.setAttribute('help', plugin.help)
        parser.setAttribute('label', plugin.label)
        parser.setAttribute('color', plugin.color)
        parser.setAttribute('group', plugin.group)
        parser.setAttribute('help', plugin.help)
        parser.setAttribute('in_ports', plugin.in_ports)
        parser.setAttribute('out_ports', plugin.out_ports)
        parser.setAttribute('properties', plugin.properties)
        parser.setAttribute('codes', plugin.codes)

        try:
            data_dir = System.get_user_dir() + "/extensions/"
            data_dir = data_dir + plugin.language + "/" + plugin.framework + "/"
            if not os.path.isdir(data_dir):
                try:
                    os.makedirs(data_dir)
                except:
                    pass
            file_name = data_dir + plugin.label.lower().replace(' ', '_') + ".py"
            parser.save(file_name)
        except IOError as e:
            return False
        return True
    # ----------------------------------------------------------------------
    @classmethod
    def add_plugin(cls, plugin):
        # first, save it
        PluginControl.save(plugin)
        # Then add it to system
        from harpia.system import System
        System.plugins[plugin.type] = plugin

    # ----------------------------------------------------------------------
    @classmethod
    def delete_plugin(cls, plugin):
        from harpia.system import System
        if plugin.source == "xml":
            data_dir = System.get_user_dir() + "/extensions/"
            file_name = data_dir + plugin.type + ".xml"
            os.remove(file_name)
            System.plugins.pop(plugin.type, None)
            return True
        else:
            return False

    # ----------------------------------------------------------------------
    @classmethod
    def print_plugin(cls, plugin):
        """
        This method prints the plugin properties.
        """
        print 'Plugin.id =', plugin.id
        print 'Plugin.x =', plugin.x
        print 'Plugin.y =', plugin.y

        print 'Plugin.type =', plugin.type
        print 'Plugin.language =', plugin.language
        print 'Plugin.framework =', plugin.framework
        print 'Plugin.source =', plugin.source

        # Appearance
        print 'Plugin.help =', plugin.help
        print 'Plugin.label =', plugin.label
        print 'Plugin.color =', plugin.color
        print 'Plugin.group =', plugin.group
        print 'Plugin.in_ports =', plugin.in_ports
        print 'Plugin.out_ports =', plugin.out_ports

        # Code generation
        print 'Plugin.properties =', plugin.properties
        print 'Plugin.codes =', plugin.codes

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the menu bar.
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from harpia.system import System as System
import gettext

_ = gettext.gettext


class Menu(Gtk.MenuBar):
    """
    This class contains methods related the Menu class
    """
    # ----------------------------------------------------------------------

    def __init__(self, main_window):
        """Constructor."""
        Gtk.MenuBar.__init__(self)
        self.main_window = main_window

        mc = self.main_window.main_control
        self.accel_group = Gtk.AccelGroup()
        self.main_window.add_accel_group(self.accel_group)
        # dictionary component: action
        self.list_of_examples = []
        self.actions = {}
        # -------------------------- File -------------------------------------
        file_menu = Gtk.Menu()
        self.recent_files_menu = Gtk.Menu()
        self.__create_menu(_("New"), "<Control>N", file_menu, mc.new)
        self.__create_menu(_("Open"), "<Control>O", file_menu, mc.select_open)
        self.__create_menu(_("Close"), "<Control>W", file_menu, mc.close)
        recents = self.__create_menu(_("Recents"), None, file_menu, None)
        recents.set_submenu(self.recent_files_menu)
        file_menu.append(Gtk.SeparatorMenuItem())
        self.__create_menu(_("Save"), "<Control>S", file_menu, mc.save)
        self.__create_menu(_("Save As..."), None, file_menu, mc.save_as)
        self.__create_menu(_("Export Diagram As PNG..."), "<Control>E",
                           file_menu, mc.export_diagram)
        file_menu.append(Gtk.SeparatorMenuItem())
        self.__create_menu(_("Exit"), "<Control>Q", file_menu, mc.exit)
        self.__add_menu_category(_("File"), file_menu)

        # -------------------------- Edit -------------------------------------
        edit_menu = Gtk.Menu()
        self.__create_menu(_("Undo"), "<Control>Z", edit_menu, mc.undo)
        self.__create_menu(_("Redo"), "<Shift><Control>Z", edit_menu, mc.redo)
        edit_menu.append(Gtk.SeparatorMenuItem())
        self.__create_menu(
            _("Select All"), "<Control>A", edit_menu, mc.select_all)
        self.__create_menu(_("Cut"), "<Control>X", edit_menu, mc.cut)
        self.__create_menu(_("Copy"), "<Control>C", edit_menu, mc.copy)
        self.__create_menu(_("Paste"), "<Control>V", edit_menu, mc.paste)
        self.__create_menu(_("Delete"), "Delete", edit_menu, mc.delete)
        edit_menu.append(Gtk.SeparatorMenuItem())
        self.__create_menu(_("Align Top"), "<Control>1", edit_menu, mc.align_top)
        self.__create_menu(_("Align Bottom"), "<Control>2", edit_menu, mc.align_bottom)
        self.__create_menu(_("Align Left"), "<Control>3", edit_menu, mc.align_left)
        self.__create_menu(_("Align Right"), "<Control>4", edit_menu, mc.align_right)
        edit_menu.append(Gtk.SeparatorMenuItem())
        self.__create_menu(
            _("Clear Console"), "<Control>L", edit_menu, mc.clear_console)
        edit_menu.append(Gtk.SeparatorMenuItem())
        self.__create_menu(_("Preferences"), None, edit_menu, mc.preferences)
        self.__add_menu_category(_("Edit"), edit_menu)

        # -------------------------- View -------------------------------------
        view_menu = Gtk.Menu()
        self.__create_menu(_("Zoom In"), None, view_menu, mc.zoom_in)
        self.__create_menu(_("Zoom Out"), None, view_menu, mc.zoom_out)
        self.__create_menu(
            _("Normal Size"), "<Control>0", view_menu, mc.zoom_normal)

        edit_menu.append(Gtk.SeparatorMenuItem())
        self.__create_check_menu(_("Show Grid"), "<Control>g", view_menu, mc.show_grid)
        self.__add_menu_category(_("View"), view_menu)

        # -------------------------- Process --------------------------------
        process_menu = Gtk.Menu()
        self.__create_menu(_("Run"), "<Control>R", process_menu, mc.run)
        self.__create_menu(_("Save Source"), None,
                           process_menu, mc.save_source)
        self.__create_menu(_("View Source"), None,
                           process_menu, mc.view_source)
        self.__add_menu_category(_("Process"), process_menu)

        # -------------------------- Plugin --------------------------------
        plugin_menu = Gtk.Menu()
        self.__create_menu(_("Code Template Manager"), None,
                           plugin_menu, mc.code_template_manager)
        self.__create_menu(_("Plugin Manager"), None,
                           plugin_menu, mc.plugin_manager)
        self.__create_menu(_("Port Manager"), None,
                           plugin_menu, mc.port_manager)
        plugin_menu.append(Gtk.SeparatorMenuItem())
        self.export_plugins_menu = Gtk.Menu()
        export_plugins = self.__create_menu(_("Export As..."), None, plugin_menu, None)
        export_plugins.set_submenu(self.export_plugins_menu)
        self.__create_menu(_("Python"), None, self.export_plugins_menu, mc.export_python_dialog)
        self.__create_menu(_("XML"), None, self.export_plugins_menu, mc.export_xml_dialog)

        self.__add_menu_category(_("Plugins"), plugin_menu)

        # -------------------------- Help -----------------------------------
        # Cria sub menu
        help_menu = Gtk.Menu()
        self.example_menu = Gtk.Menu()
        examples = self.__create_menu(_("Example"), None, help_menu, None)
        examples.set_submenu(self.example_menu)
        help_menu.append(Gtk.SeparatorMenuItem())
        self.__create_menu(_("About"), None, help_menu, mc.about)
        self.__add_menu_category(_("Help"), help_menu)

    # ----------------------------------------------------------------------
    def __create_menu(self, name, accel, menu, action):
        """
        This method create the menu
            Parameters:
                * **name** (:class:`str<str>`): Name the menu.
                * **accel** (:class:`str<str>`):
                menu(Gtk.Menu): GTK.Menu().
                action(Objeto): Instance.
            Returns:
                Return menu.

        """
        item = Gtk.MenuItem(name)
        if accel is not None:
            key, mod = Gtk.accelerator_parse(accel)
            item.add_accelerator(
                "activate", self.accel_group, key, mod, Gtk.AccelFlags.VISIBLE)
        menu.append(item)
        if action is not None:
            item.connect("activate", self.__menu_clicked, None)
            self.actions[item] = action
        return item

    def __create_check_menu(self, name, accel, menu, action):
        item = Gtk.CheckMenuItem(name)
        if accel is not None:
            key, mod = Gtk.accelerator_parse(accel)
            item.add_accelerator(
                "activate", self.accel_group, key, mod, Gtk.AccelFlags.VISIBLE)
        menu.append(item)
        if action is not None:
            item.connect("activate", action)
            self.actions[item] = action
        return item

    # ----------------------------------------------------------------------
    def __add_menu_category(self, name, submenu):
        """
        This method add a category in menu.

            Parameters:
                * **name** (:class:`str<str>`):
                * **submenu** (:class:`str<str>`):
        """
        menu_item = Gtk.MenuItem(name)
        menu_item.show()
        menu_item.set_submenu(submenu)
        self.append(menu_item)

    # ----------------------------------------------------------------------
    def __menu_clicked(self, widget, data):
        """
        This method monitors if the menu was cliked.

            Parameters:
                widget:
                data:
        """
        self.actions[widget]()

    # ----------------------------------------------------------------------
    def __load_recent(self, widget, data):
        """
        This method monitors the lasts files loaded.

            Parameters:
                widget:
                data:
            Returns:
                None.
        """
        self.main_window.main_control.open(widget.get_label())

    # ----------------------------------------------------------------------
    def add_example(self, example):
        """
        This method add a file at list of examples.

            Parameters:
                * **self** (:class:`Menu<harpia.GUI.menu>`)
                * **example** (:class:`str<str>`)

        """
        self.list_of_examples.append(example)
        menu_item = Gtk.MenuItem(example.split("/").pop())
        self.example_menu.append(menu_item)
        menu_item.connect(
            "activate", self.__load_example, len(self.list_of_examples) - 1)
        self.example_menu.show_all()

    # ----------------------------------------------------------------------
    def __load_example(self, widget, data):
        """
        This method load a example.

            Parameters:
                widget:
                data:

        """
        self.main_window.main_control.open(self.list_of_examples[int(data)])

    # ----------------------------------------------------------------------
    def update_recent_file(self):
        """
        This method update recent files.
        """

        for widget in self.recent_files_menu.get_children():
            self.recent_files_menu.remove(widget)
        for recent_file in System.properties.recent_files:
            self.add_recent_file(recent_file)

    # ----------------------------------------------------------------------
    def add_recent_file(self, recent_file):
        """
        This method add a file in recent files.

            Parameters:
                recent_file: The file to add.

        """
        menu_item = Gtk.MenuItem(recent_file)
        self.recent_files_menu.append(menu_item)
        menu_item.connect("activate", self.__load_recent, None)
        self.recent_files_menu.show_all()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from prompt_toolkit.completion import Completer, Completion
import six
import re


class VaultCompleter(Completer):
    def __init__(self, vault_commandhandler, resource, helper_buffer):
        self.vault_commandhandler = vault_commandhandler
        self.resource = resource
        self.helper_buffer = helper_buffer

    def parse_document(self, document):
        cmdlist = document.text.split(" ")
        # for cmd in cmdlist:
        #     if cmd == "" or cmd == " ":
        #         cmdlist.remove(cmd)

        return cmdlist

    def get_current_command_options(self, cmdlist):
        """
        Get the options for the current comamnd
        """
        help_string = "Helpstr..."
        cmdobj = self.vault_commandhandler.get_command_tree(cmdlist)
        if 'options' in cmdobj.keys():
            help_string = cmdobj['usage']
            help_string = six.text_type(help_string)
            options = cmdobj['options']
        else:
            options = cmdobj.keys()


        # Before we return the list of options, filter them based on
        # what is already processed.
        matches = []
        matches_prefix = []
        last_cmd = cmdlist[-2]
        for option in options:
            if option.startswith(last_cmd):
                matches.append(option)
                matches_prefix.append(option.split("=")[0])

        for cmdoption in cmdlist[1:-2]:
            if cmdoption.split("=")[0] in matches_prefix:
                remove_idx = matches_prefix.index(cmdoption.split("=")[0])
                remove_obj = matches[remove_idx]
                matches.remove(remove_obj)

        return (matches, help_string)

    def get_completions(self, document, complete_event):
        """
        Override this function from the parent class. It should
        return an iterator
        """
        cmdlist = self.parse_document(document)

        (completion_options, help_string) = \
            self.get_current_command_options(cmdlist)
        self.helper_buffer.text = help_string

        for option in completion_options:
            yield Completion(option, start_position=0)

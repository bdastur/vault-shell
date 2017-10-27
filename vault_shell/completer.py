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
        self.help_string = "Helpstr..."

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
        cmdobj = self.vault_commandhandler.get_command_tree(cmdlist)
        if 'options' in cmdobj.keys():
            self.help_string = cmdobj['usage']
            options = cmdobj['options']
        else:
            options = cmdobj.keys()


        # Before we return the list of options, filter them based on
        # what is already processed
        matches = []
        matches_prefix = []
        last_cmd = cmdlist[-2]

        # This filters out options starting with the option/Command
        # at the cursor.
        # Eg: vault> token-   (options should all start with token-*)
        # Eg: vault> token-create -p (options should be -policy=, -period=)
        for option in options:
            if option.startswith(last_cmd):
                matches.append(option)
                matches_prefix.append(option.split("=")[0])

        # Once we have our list of options, we add second filter for
        # options or commands that are already entered/parsed.
        # Eg: vault> token-create -use-limit=1 _ (at this point the options
        # should not have -use-limit in the options list.)
        for cmdoption in cmdlist[1:-2]:
            if cmdoption.split("=")[0] in matches_prefix:
                remove_idx = matches_prefix.index(cmdoption.split("=")[0])
                remove_obj = matches[remove_idx]
                matches.remove(remove_obj)

        if len(matches) == 1:
            if 'options' in cmdobj.keys():
                helpstr = cmdobj['options'][matches[0]]['helpstr']
                self.help_string += "\n" + "Option help:\n  " + helpstr

        help_string = six.text_type(self.help_string)
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

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from prompt_toolkit.completion import Completer, Completion


class VaultCompleter(Completer):
    def __init__(self, vault_commandhandler, resource):
        self.vault_commandhandler = vault_commandhandler
        self.resource = resource

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
            options = cmdobj['options']
        else:
            options = cmdobj.keys()

        # Before we return the list of options, filter them based on
        # what is already processed.
        matches = []
        last_cmd = cmdlist[-2]
        for option in options:
            if option.startswith(last_cmd):
                matches.append(option)

        return matches


    def get_completions(self, document, complete_event):
        """
        Override this function from the parent class. It should
        return an iterator
        """
        cmdlist = self.parse_document(document)
        completion_options = self.get_current_command_options(cmdlist)

        for option in completion_options:
            yield Completion(option, start_position=0)

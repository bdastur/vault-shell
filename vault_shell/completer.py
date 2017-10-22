#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from prompt_toolkit.completion import Completer, Completion


class VaultCompleter(Completer):
    def __init__(self, vault_commandhandler, resource):
        self.vault_commandhandler = vault_commandhandler
        self.resource = resource

    def get_completions(self, document, complete_event):
        """
        Override this function from the parent class. It should
        return an iterator
        """
        print "..document: ", document

        cmdlist = ["vault", "create", "list"]
        for option in cmdlist:
            yield Completion(option, start_position=0)

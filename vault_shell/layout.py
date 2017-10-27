#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from prompt_toolkit.layout.containers import VSplit, Window
from prompt_toolkit.layout.dimension import LayoutDimension as D
from prompt_toolkit.layout.controls import BufferControl, FillControl
from prompt_toolkit.token import Token
from prompt_toolkit.shortcuts import create_prompt_layout
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.enums import DEFAULT_BUFFER
from prompt_toolkit.buffer import AcceptAction
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory


from vault_shell.lexer import VaultLexer
from vault_shell.toolbar import Toolbar
from vault_shell.resources import Resource
from vault_shell.completer import VaultCompleter
from vault_shell.vault_commandhelper import VaultCommandHelper


class VaultBuffer(object):
    def __init__(self):
        history = InMemoryHistory()
        vault_commandhandler = VaultCommandHelper()
        resource = Resource()

        self.helper_buffer = Buffer(is_multiline=True,
                                    complete_while_typing=True,
                                    enable_history_search=False,
                                    initial_document=None,
                                    accept_action=AcceptAction.IGNORE)

        self.vault_completer = VaultCompleter(vault_commandhandler,
                                              resource,
                                              self.helper_buffer)

        self.main_buffer = Buffer(completer=self.vault_completer,
                                  auto_suggest=AutoSuggestFromHistory(),
                                  history=history,
                                  validator=None,
                                  tempfile_suffix='',
                                  complete_while_typing=True,
                                  initial_document=None,
                                  accept_action=AcceptAction.RETURN_DOCUMENT)

        self.helper_buffer.text = "Vault Help"

        self.vault_completer.help_buffer = self.helper_buffer

        self.buffers = {
            DEFAULT_BUFFER: self.main_buffer,
            'HELP': self.helper_buffer
        }



class VaultLayout(object):
    def __init__(self,
                 message="vault> ",
                 menu_height=19,
                 multiwindow=True):
        toolbar = Toolbar()
        main_layout = create_prompt_layout(
             message=message,
             lexer=VaultLexer,
             get_bottom_toolbar_tokens=toolbar.handler,
             reserve_space_for_menu=menu_height)

        if multiwindow:
            self.mlayout = VSplit([
                main_layout,
                Window(width=D.exact(1),
                       content=FillControl('|', token=Token.Line)),
                Window(width=D.exact(90),
                       wrap_lines=True,
                       content=BufferControl(buffer_name='HELP')),
            ])

        if multiwindow:
            self.layout = self.mlayout
        else:
            self.layout = main_layout


    def get_layout(self):
        return self.layout

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import sys
import os
from prompt_toolkit import Application, CommandLineInterface, AbortAction
from prompt_toolkit.key_binding.manager import KeyBindingManager
from prompt_toolkit.keys import Keys
from prompt_toolkit.shortcuts import create_eventloop

from prompt_toolkit.styles import PygmentsStyle

from vault_shell.vault_commandhelper import VaultCommandHelper
from vault_shell.style import VaultStyle
from vault_shell.layout import VaultLayout
from vault_shell.layout import VaultBuffer

VaultKeyBinder = KeyBindingManager(enable_search=True,
                                   enable_abort_and_exit_bindings=True,
                                   enable_system_bindings=True,
                                   enable_auto_suggest_bindings=True)
manager = KeyBindingManager.for_prompt()

@manager.registry.add_binding(Keys.ControlQ)
def _controlQKey(event):
    def print_hello():
        print "Key pressed"
    event.cli.run_in_terminal(print_hello)


def run():
    cli_buffer = VaultBuffer()
    vault_layout = VaultLayout(multiwindow=True)

    application = Application(
        style=PygmentsStyle(VaultStyle),
        layout=vault_layout.layout,
        buffers=cli_buffer.buffers,
        on_exit=AbortAction.RAISE_EXCEPTION,
        key_bindings_registry=VaultKeyBinder.registry,
        use_alternate_screen=False)

    cli = CommandLineInterface(application=application,
                               eventloop=create_eventloop())

    while True:
        try:
            document = cli.run(reset_current_buffer=True)
            process_document(document)
        except KeyboardInterrupt:
            print "Keyboard interrupt generated"
            continue
        except EOFError:
            print "ctrl-D"
            sys.exit()


def process_document(document):
    if document.text == "quit" or document.text == "exit":
        print "Exit now!"
        sys.exit()

    if len(document.text) == 0:
        return

    cmdlist = document.text.split(" ")
    vault_cmdhelper = VaultCommandHelper()
    cmdlist.insert(0, 'vault')
    output = vault_cmdhelper.execute_vault_commands(cmdlist)
    print output

if __name__ == '__main__':
    run()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import vault_shell.vault_commandhelper as VaultHelper

class VaultShellTests(unittest.TestCase):
    def test_basic(self):
        print "test basic. Pass"
        vaulthelper = VaultHelper.VaultCommandHelper()
        self.failUnless(vaulthelper is not None)

    def test_execute_vault_commands(self):
        vaulthelper = VaultHelper.VaultCommandHelper()
        output = vaulthelper.execute_vault_commands(['vault'])
        self.failUnless(output is not None)

    def test_get_commandkey_from_cmdlist(self):
        vaulthelper = VaultHelper.VaultCommandHelper()
        cmdkey = vaulthelper.get_commandkey_from_cmdlist(["token-create"])
        self.assertEqual(cmdkey,
                         "vault_token-create",
                         msg="cmdkey did not match")

    def test_parse_vault_command_output(self):
        vaulthelper = VaultHelper.VaultCommandHelper()
        output = vaulthelper.execute_vault_commands(['vault'])
        cmdkey = vaulthelper.get_commandkey_from_cmdlist([])
        vaulthelper.parse_vault_command_output(output, cmdkey)

        vault_commands = ['token-create', 'revoke', 'step-down', 'seal',
            'remount', 'policy-delete', 'audit-disable', 'policy-write',
            'audit-list', 'unseal', 'unmount', 'token-revoke', 'generate-root',
            'capabilities', 'write', 'init', 'version', 'token-renew',
            'token-lookup', 'usage', 'status', 'unwrap', 'read', 'auth-enable',
            'auth', 'auth-disable', 'key-status', 'ssh', 'path-help', 'rotate',
            'rekey', 'mount', 'audit-enable', 'list', 'server', 'mount-tune',
            'renew', 'policies', 'mounts', 'delete']
        self.assertEquals(vaulthelper.cmd_dict[cmdkey].keys(),
                          vault_commands,
                          msg="Vault commands did not match")

    def test_parse_vault_command_output_tokencreate(self):
        vaulthelper = VaultHelper.VaultCommandHelper()
        output = vaulthelper.get_vault_help_options(["token-create"])
        cmdkey = vaulthelper.get_commandkey_from_cmdlist(["token-create"])
        vaulthelper.parse_vault_command_output(output, cmdkey)
        import pprint
        pp = pprint.PrettyPrinter()
        pp.pprint(vaulthelper.cmd_dict)

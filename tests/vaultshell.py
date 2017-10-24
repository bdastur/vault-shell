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

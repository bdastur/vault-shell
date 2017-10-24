#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
import subprocess


class VaultCommandHelper(object):
    def __init__(self):
        self.cmd_dict = {}

    def execute_vault_commands(self, vault_cmdlist):
        print "vault cmd: ", vault_cmdlist

        try:
            sproc = subprocess.Popen(vault_cmdlist,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)
        except OSError:
            # An excepton is thrown. In cases where the cmdlist is not valid.
            # we can simply return None.
            return None

        stdout, stderr = sproc.communicate()

        if stdout:
            output = stdout
        else:
            output = stderr

        return output

    def get_commandkey_from_cmdlist(self, cmdlist):
        '''
        Return a string that can be used as a key to index the cached
        commands and arguments
        '''
        cmdkey = "vault"
        for cmd in cmdlist:
            cmdkey += "_" + cmd

        return cmdkey

    def parse_vault_command_output(self, cmdoutput, cmdkey):
        """
        Parse the output.
        """
        self.cmd_dict[cmdkey] = {}

        cur_option = None
        cmd_type = 'subcmds'
        for line in cmdoutput.splitlines():
            if not line:
                print "continue"
                continue

            # print "Line: ", line
            if re.match(r'.*Common commands:', line, re.IGNORECASE):
                parse_stage = 2
                cmd_type = 'subcmds'
                continue

            if re.match(r'All other commands:', line, re.IGNORECASE):
                parse_stage = 2
                cmd_type = 'subcmds'
                continue

            if re.match(r'.*General Options:', line, re.IGNORECASE):
                parse_stage = 3
                cmd_type = "options"
                continue

            if re.match(r'usage:.*', line, re.IGNORECASE):
                parse_stage = 1
                self.cmd_dict[cmdkey]['usage'] = line + "\n"
                continue

            if parse_stage == 1:
                self.cmd_dict[cmdkey]['usage'] += line + "\n"
                continue

            if line.startswith("           "):
                mobj = re.match(r'\s+(\S+.*)', line)
                if mobj:
                    self.cmd_dict[cmdkey][cur_option]['helpstr'] += \
                        mobj.group(1) + "\n"
                    continue

            mobj = re.match(r'\s+(\S+)\s*(\w+.*)', line)
            if mobj:
                #print "matched: ", mobj.group(1), mobj.group(2)
                cur_option = mobj.group(1)
                self.cmd_dict[cmdkey][cur_option] = {}
                self.cmd_dict[cmdkey][cur_option]['helpstr'] = \
                    mobj.group(2) + "\n"

        print self.cmd_dict

    def get_command_tree(self, cmdlist):

        # When cmdlist is None, it means we are executing  the command
        # from top
        if cmdlist == None:
            cmdlist = ["vault"]

        cmdkey = self.get_commandkey_from_cmdlist(cmdlist)
        output = self.execute_vault_commands(cmdlist)
        self.parse_vault_command_output(output, cmdkey)

        print "output: ", output

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygments.lexer import RegexLexer
from pygments.token import Keyword, Operator

__all__ = ["VaultLexer"]

class VaultLexer(RegexLexer):
    name = "VaultShell"
    aliases = ["vaultshell"]
    filenames = ["*.vaultshell"]

    tokens = {
        'root': [
            (r'(read|write|create'
             r'|usage|user|volume)', Keyword),
            (r'--(ip-version|project|project-domain|share|no-share'
             r'|consumer-secret|request-secret|verifier|compute|network'
             r'|role|impersonate|expiration|trustor-domain|trustee-domain)',
             Operator)],
    }

    

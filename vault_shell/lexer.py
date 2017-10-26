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
            (r'(delete|path-help|read|renew|revoke|server|status|write|unwrap'
             r'|audit-disable|audit-enable|audit-list|auth|auth-disable'
             r'|auth-enable|capabilities|generate-root|init|key-status|list'
             r'|key-status|list|mount|mount-tune|mounts|policies|policy-delete'
             r'|policy-write|rekey|remount|rotate|seal|ssh|step-down'
             r'|token-create|token-lookup|token-renew|token-revoke|unmount'
             r'|unseal|version)',
             Keyword),
            (r'-(address|ca-cert|ca-path|client|client-key|tls-skip-verify'
             r'|wrap-ttl|format|field|force|dev|config|dev-root-token-id'
             r'|dev-listen-address|log-level|description|path|local'
             r'|method|method-help|methods|no-verify|no-store|token-only'
             r'|plugin-name|init|cancel|status|decode|genotp|otp|pgp-key|nonce'
             r'|check|key-shares|key-threshold|stored-shares|pgp-keys'
             r'|root-token-pgp-key|recovery-shares|recovery-threshold'
             r'|recovery-pgp-keys|auto|consul-service|default-lease-ttl'
             r'|max-lease-ttl|force-no-cache|backup|recovery-key'
             r'|role|no-exec|mount-point|format|strict-host-key-checking'
             r'|user-known-hosts-file|public-key-path|private-key-path'
             r'|host-key-mount-point|host-key-hostnames|id|display-name'
             r'|ttl|explicit-max-ttl|period|renewable|metadata|orphan'
             r'|no-default-policy|policy|use-limit|reset)',
             Operator)],
    }

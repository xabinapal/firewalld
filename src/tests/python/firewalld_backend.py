#!/usr/bin/python
# SPDX-License-Identifier: GPL-2.0-or-later
#
# Copyright (C) 2025 Red Hat, Inc.
#
# Authors:
# Xabier Napal <xabier.napal@dvzr.io>

# To use in git tree: PYTHONPATH=.. python firewalld-test.py

import sys
import unittest
from unittest.mock import patch
from firewall.core import fw


class TestFirewallBackend(unittest.TestCase):
    def test_iptables_backend_without_nftables_module(self):
        """Test that iptables backend works when nftables module is missing"""
        with patch.dict("sys.modules", {"firewall.core.nftables": None}):
            import importlib

            if "firewall.core.fw" in sys.modules:
                importlib.reload(fw)

            firewall = fw.Firewall(offline=True)
            firewall._firewall_backend = "iptables"
            firewall._select_firewall_backend("iptables")

            self.assertFalse(firewall.nftables_enabled)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFirewallBackend)
    results = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(0 if results.wasSuccessful() else 1)

# TestSwiftPrivateDeclName.py
#
# This source file is part of the Swift.org open source project
#
# Copyright (c) 2014 - 2016 Apple Inc. and the Swift project authors
# Licensed under Apache License v2.0 with Runtime Library Exception
#
# See https://swift.org/LICENSE.txt for license information
# See https://swift.org/CONTRIBUTORS.txt for the list of Swift project authors
#
# ------------------------------------------------------------------------------
"""
Test that we correctly find private decls
"""
import lldb
from lldbsuite.test.lldbtest import *
from lldbsuite.test.decorators import *
import lldbsuite.test.lldbutil as lldbutil
import os
import unittest2


class TestSwiftPrivateDeclName(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.a_source = "a.swift"
        self.a_source_spec = lldb.SBFileSpec(self.a_source)
        self.b_source = "b.swift"
        self.b_source_spec = lldb.SBFileSpec(self.b_source)

    @swiftTest
    def test_swift_private_decl_name(self):
        """Test that we correctly find private decls"""
        self.build()

        # Create the target
        target = self.dbg.CreateTarget(self.getBuildArtifact())
        self.assertTrue(target, VALID_TARGET)

        # Set the breakpoints
        a_breakpoint = target.BreakpointCreateBySourceRegex(
            'break here', self.a_source_spec)
        self.assertTrue(a_breakpoint.GetNumLocations() > 0, VALID_BREAKPOINT)
        b_breakpoint = target.BreakpointCreateBySourceRegex(
            'break here', self.b_source_spec)
        self.assertTrue(b_breakpoint.GetNumLocations() > 0, VALID_BREAKPOINT)

        process = target.LaunchSimple(None, None, os.getcwd())
        self.assertTrue(process, PROCESS_IS_VALID)

        threads = lldbutil.get_threads_stopped_at_breakpoint(
            process, a_breakpoint)

        self.assertTrue(len(threads) == 1)

        var = self.frame().FindVariable("a")
        child_a = var.GetChildMemberWithName("a")
        child_b = var.GetChildMemberWithName("b")
        child_c = var.GetChildMemberWithName("c")
        lldbutil.check_variable(self, var, False, typename="a.S.A")
        lldbutil.check_variable(self, child_a, False, value="1")
        lldbutil.check_variable(self, child_b, False, '"hello"')
        lldbutil.check_variable(self, child_c, False, value='1.25')

        process.Continue()
        threads = lldbutil.get_threads_stopped_at_breakpoint(
            process, b_breakpoint)

        self.assertTrue(len(threads) == 1)

        var = self.frame().FindVariable("a")
        child_a = var.GetChildMemberWithName("a")
        child_b = var.GetChildMemberWithName("b")
        child_c = var.GetChildMemberWithName("c")
        lldbutil.check_variable(self, var, False, typename="a.S.A")
        lldbutil.check_variable(self, child_a, False, value="3")
        lldbutil.check_variable(self, child_b, False, '"goodbye"')
        lldbutil.check_variable(self, child_c, False, value='1.25')


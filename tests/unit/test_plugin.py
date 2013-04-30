# Copyright 2012-2013 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.
import sys
from tests import unittest

from awscli import plugin
from botocore import hooks


class FakeModule(object):
    def __init__(self):
        self.called = False
        self.context = None
        self.events_seen = []

    def awscli_initialize(self, context):
        self.called = True
        self.context = context
        self.context.register(
            'before_operation',
            (lambda **kwargs: self.events_seen.append(kwargs)))


class TestPlugins(unittest.TestCase):

    def setUp(self):
        self.fake_module = FakeModule()
        sys.modules['__fake_plugin__'] = self.fake_module

    def tearDown(self):
        del sys.modules['__fake_plugin__']

    def test_plugin_register(self):
        emitter = plugin.load_plugins({'fake_plugin': '__fake_plugin__'})
        self.assertTrue(self.fake_module.called)
        self.assertTrue(isinstance(emitter, hooks.HierarchicalEmitter))
        self.assertTrue(isinstance(self.fake_module.context, plugin.CLI))

    def test_event_hooks_can_be_passed_in(self):
        hooks = plugin.EventHooks()
        emitter = plugin.load_plugins({'fake_plugin': '__fake_plugin__'},
                                      event_hooks=hooks)
        emitter.emit('before_operation')
        self.assertEqual(len(self.fake_module.events_seen), 1)



if __name__ == '__main__':
    unittest.main()

#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""A sample test module to exercise the code.

For the sake of exploratory development.
"""

import os
import sys

from gabbi import driver
# TODO(cdent): test_pytest allows pytest to see the tests this module
# produces. Without it, the generator will not run. It is a todo because
# needing to do this is annoying and gross.
from gabbi.driver import test_pytest  # noqa
from gabbi import fixture
from gabbi.handlers import base
from gabbi.tests import simple_wsgi
from gabbi.tests import util


TESTS_DIR = 'gabbits_intercept'


class FixtureOne(fixture.GabbiFixture):
    """Drive the fixture testing weakly."""
    pass


class FixtureTwo(fixture.GabbiFixture):
    """Drive the fixture testing weakly."""
    pass


class EnvironFixture(fixture.GabbiFixture):
    """Set some stuff in the environment."""
    # In the shell environment, environment variables are
    # always strings, so make that explicit here.
    os.environ['INT'] = "1"
    os.environ['FLOAT'] = "1.5"
    # For making sure something that looks like a number stays
    # a string?
    os.environ['STR'] = "2"
    os.environ['TBOOL'] = "True"
    os.environ['FBOOL'] = "False"


class StubResponseHandler(base.ResponseHandler):
    """A sample response handler just to test."""

    test_key_suffix = 'test'
    test_key_value = []

    def preprocess(self, test):
        """Add some data if the data is a string."""
        try:
            test.output = test.output + '\nAnother line'
        except TypeError:
            pass

    def action(self, test, item, value=None):
        item = item.replace('COW', '', 1)
        test.assertIn(item, test.output)


# Incorporate the SkipAllFixture into this namespace so it can be used
# by tests (cf. skipall.yaml).
SkipAllFixture = fixture.SkipAllFixture


BUILD_TEST_ARGS = dict(
    intercept=simple_wsgi.SimpleWsgi,
    fixture_module=sys.modules[__name__],
    prefix=os.environ.get('GABBI_PREFIX'),
    response_handlers=[StubResponseHandler]
)


def load_tests(loader, tests, pattern):
    """Provide a TestSuite to the discovery process."""
    # Set and environment variable for one of the tests.
    util.set_test_environ()

    test_dir = os.path.join(os.path.dirname(__file__), TESTS_DIR)
    return driver.build_tests(test_dir, loader,
                              test_loader_name=__name__,
                              **BUILD_TEST_ARGS)


def pytest_generate_tests(metafunc):
    util.set_test_environ()
    test_dir = os.path.join(os.path.dirname(__file__), TESTS_DIR)
    driver.py_test_generator(test_dir, metafunc=metafunc,
                             test_loader_name=__name__,
                             **BUILD_TEST_ARGS)

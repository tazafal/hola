#!/usr/bin/python
#
# Copyright (C) 2006 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__author__ = 'jscudder@google.com (Jeff Scudder)'

import unittest
import app_service

class AtomServiceUnitTest(unittest.TestCase):
  
  def setUp(self):
    pass

  def tearDown(self):
    pass

  def testBuildUriWithNoParams(self):
    x = app_service.BuildUri('/base/feeds/snippets')
    self.assert_(x == '/base/feeds/snippets')

  def testBuildUriWithParams(self):
    # Add parameters to a URI
    x = app_service.BuildUri('/base/feeds/snippets', url_params={'foo': 'bar', 
                                                     'bq': 'digital camera'})
    self.assert_(x == '/base/feeds/snippets?foo=bar&bq=digital+camera')
    self.assert_(x.startswith('/base/feeds/snippets'))
    self.assert_(x.count('?') == 1)
    self.assert_(x.count('&') == 1)
    self.assert_(x.index('?') < x.index('&'))
    self.assert_(x.index('bq=digital+camera') != -1)

    # Add parameters to a URI that already has parameters
    x = app_service.BuildUri('/base/feeds/snippets?bq=digital+camera', 
                             url_params={'foo': 'bar', 'max-results': '250'})
    self.assert_(x.startswith('/base/feeds/snippets?bq=digital+camera'))
    self.assert_(x.count('?') == 1)
    self.assert_(x.count('&') == 2)
    self.assert_(x.index('?') < x.index('&'))
    self.assert_(x.index('max-results=250') != -1)
    self.assert_(x.index('foo=bar') != -1)


  def testBuildUriWithoutParameterEscaping(self):
    x = app_service.BuildUri('/base/feeds/snippets', 
            url_params={'foo': ' bar', 'bq': 'digital camera'}, 
            escape_params=False)
    self.assert_(x.index('foo= bar') != -1)
    self.assert_(x.index('bq=digital camera') != -1)




if __name__ == '__main__':
  unittest.main()
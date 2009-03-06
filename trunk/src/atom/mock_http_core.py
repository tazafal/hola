#!/usr/bin/env python
#
# Copyright (C) 2009 Google Inc.
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


# This module is used for version 2 of the Google Data APIs.


__author__ = 'j.s@google.com (Jeff Scudder)'


import StringIO
import pickle
import os.path
import tempfile
import atom.http_core


class MockHttpClient(object):

  real_client = None

  def __init__(self, recordings=None, real_client=None):
    self._recordings = recordings or []
    if real_client is not None:
      self.real_client = real_client

  def add_response(self, http_request, status, reason, headers=None, 
      body=None):
    if body is not None:
      if hasattr(body, 'read'):
        copied_body = body.read()
      else:
        copied_body = body
    else:
      copied_body = None
    response = atom.http_core.HttpResponse(status, reason, headers, 
                                           copied_body)
    # TODO Scrub the request and the response.
    self._recordings.append((http_request._copy(), response))

  AddResponse = add_response
  
  def request(self, http_request):
    """Provide a recorded response, or record a response for replay.

    If the real_client is set, the request will be made using the
    real_client, and the response from the server will be recorded.
    If the real_client is None (the default), this method will examine
    the recordings and find the first which matches. 
    """
    request = http_request._copy()
    _scrub_request(request)
    if self.real_client is None:
      for recording in self._recordings:
        if _match_request(recording[0], request):
          return recording[1]
    else:
      response = self.real_client.request(http_request)
      _scrub_response(response)
      self.add_response(request, response.status, response.reason, 
          dict(response.getheaders()), response.read())
      # Return the recording which we just added.
      return self._recordings[-1][1]
    return None

  Request = request
    
  def _save_recordings(self, filename):
    recording_file = open(os.path.join(tempfile.gettempdir(), filename), 
                          'wb')
    pickle.dump(self._recordings, recording_file)

  def _load_recordings(self, filename):
    recording_file = open(os.path.join(tempfile.gettempdir(), filename), 
                          'rb')
    self._recordings = pickle.load(recording_file)

  def _delete_recordings(self, filename):
    # TODO: add tests for this method.
    os.remove(os.path.join(tempfile.gettempdir(), filename))

  def _load_or_use_client(self, filename, http_client):
    if os.path.exists(os.path.join(tempfile.gettempdir(), filename)):
      self._load_recordings(filename)
    else:
      self.real_client = http_client


def _match_request(http_request, stored_request):
  """Determines whether a request is similar enough to a stored request 
     to cause the stored response to be returned."""
  # Check to see if the host names match.
  if (http_request.uri.host is not None 
      and http_request.uri.host != stored_request.uri.host):
    return False
  # Check the request path in the URL (/feeds/private/full/x)
  elif http_request.uri.path != stored_request.uri.path:
    return False
  # Check the method used in the request (GET, POST, etc.)
  elif http_request.method != stored_request.method:
    return False
  # If there is a gsession ID in either request, make sure that it is matched
  # exactly.
  elif ('gsessionid' in http_request.uri.query 
        or 'gsessionid' in stored_request.uri.query):
    if 'gsessionid' not in stored_request.uri.query:
      return False
    elif 'gsessionid' not in http_request.uri.query:
      return False
    elif (http_request.uri.query['gsessionid'] 
          != stored_request.uri.query['gsessionid']):
      return False
  # Ignores differences in the query params (?start-index=5&max-results=20),
  # the body of the request, the port number, HTTP headers, just to name a 
  # few.
  return True


def _scrub_request(http_request):
  # TODO: Remove authorization token from the request.
  # TODO: Remove an email address and password from a client login request. 
  pass


def _scrub_response(http_response):
  # TODO: Remove authorization token from the response.
  # TODO: Might want to remove email addresses as well.
  pass

    
class EchoHttpClient(object):
  """Sends the request data back in the response.

  Used to check the formatting of the request as it was sent. Always responds
  with a 200 OK, and some information from the HTTP request is returned in
  special Echo-X headers in the response. The following headers are added
  in the response:
  'Echo-Host': The host name and port number to which the HTTP connection is
               made. If no port was passed in, the header will contain
               host:None.
  'Echo-Uri': The path portion of the URL being requested. /example?x=1&y=2
  'Echo-Scheme': The beginning of the URL, usually 'http' or 'https'
  'Echo-Method': The HTTP method being used, 'GET', 'POST', 'PUT', etc.
  """
  
  def request(self, http_request):
    return self._http_request(http_request.uri, http_request.method, 
                              http_request.headers, http_request._body_parts)

  def _http_request(self, uri, method, headers=None, body_parts=None):
    body = StringIO.StringIO()
    response = atom.http_core.HttpResponse(status=200, reason='OK', body=body)
    if headers is None:
      response._headers = {}
    else:
      # Copy headers from the request to the response but convert values to
      # strings. Server response headers always come in as strings, so an int
      # should be converted to a corresponding string when echoing.
      for header, value in headers.iteritems():
        response._headers[header] = str(value)
    response._headers['Echo-Host'] = '%s:%s' % (uri.host, str(uri.port))
    response._headers['Echo-Uri'] = uri._get_relative_path()
    response._headers['Echo-Scheme'] = uri.scheme
    response._headers['Echo-Method'] = method
    for part in body_parts:
      if isinstance(part, str):
        body.write(part)
      elif hasattr(part, 'read'):
        body.write(part.read())
    body.seek(0)
    return response


class SettableHttpClient(object):
  """An HTTP Client which responds with the data given in set_response."""

  def __init__(self, status, reason, body, headers):
    self.set_response(status, reason, body, headers)

  def set_response(self, status, reason, body, headers):
    """Determines the response which will be sent for each request.

    Args:
      status: An int for the HTTP status code, example: 200, 404, etc.
      reason: String for the HTTP reason, example: OK, NOT FOUND, etc.
      body: The body of the HTTP response as a string or a file-like 
            object (something with a read method). 
      headers: dict of strings containing the HTTP headers in the response.
    """
    self.response = atom.http_core.HttpResponse(status=status, reason=reason,
        body=body)
    self.response._headers = headers.copy()

  def request(self, http_request):
    return self.response
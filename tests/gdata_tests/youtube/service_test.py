#!/usr/bin/python
#
# Copyright (C) 2007 Google Inc.
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

__author__ = 'api.jhartmann@gmail.com (Jochen Hartmann)'

import getpass
import time
import unittest
import StringIO
import gdata.youtube.service
import gdata.youtube
import atom
import random

YOUTUBE_TEMPLATE = '{http://gdata.youtube.com/schemas/2007}%s'
YOUTUBE_TEST_CLIENT_ID = 'ytapi-pythonclientlibrary_servicetest'


class YouTubeServiceTest(unittest.TestCase):

  def setUp(self):
    self.client = gdata.youtube.service.YouTubeService()
    self.client.email = username
    self.client.password = password
    self.client.source = YOUTUBE_TEST_CLIENT_ID
    self.client.developer_key = developer_key
    self.client.client_id = YOUTUBE_TEST_CLIENT_ID
    self.client.ProgrammaticLogin()

  def testRetrieveVideoFeed(self):
    feed = self.client.GetYouTubeVideoFeed(
        'http://gdata.youtube.com/feeds/api/standardfeeds/recently_featured');
    self.assert_(isinstance(feed, gdata.youtube.YouTubeVideoFeed))
    self.assert_(len(feed.entry) > 0)
    for entry in feed.entry:
      self.assert_(entry.title.text != '')

  def testRetrieveTopRatedVideoFeed(self):
    feed = self.client.GetTopRatedVideoFeed()
    self.assert_(isinstance(feed, gdata.youtube.YouTubeVideoFeed))
    self.assert_(len(feed.entry) > 10)

  def testRetrieveMostViewedVideoFeed(self):
    feed = self.client.GetMostViewedVideoFeed()
    self.assert_(isinstance(feed, gdata.youtube.YouTubeVideoFeed))
    self.assert_(len(feed.entry) > 10)

  def testRetrieveRecentlyFeaturedVideoFeed(self):
    feed = self.client.GetRecentlyFeaturedVideoFeed()
    self.assert_(isinstance(feed, gdata.youtube.YouTubeVideoFeed))
    self.assert_(len(feed.entry) > 10)

  def testRetrieveWatchOnMobileVideoFeed(self):
    feed = self.client.GetWatchOnMobileVideoFeed()
    self.assert_(isinstance(feed, gdata.youtube.YouTubeVideoFeed))
    self.assert_(len(feed.entry) > 10)

  def testRetrieveTopFavoritesVideoFeed(self):
    feed = self.client.GetTopFavoritesVideoFeed()
    self.assert_(isinstance(feed, gdata.youtube.YouTubeVideoFeed))
    self.assert_(len(feed.entry) > 10)

  def testRetrieveMostRecentVideoFeed(self):
    feed = self.client.GetMostRecentVideoFeed()
    self.assert_(isinstance(feed, gdata.youtube.YouTubeVideoFeed))
    self.assert_(len(feed.entry) > 10)

  def testRetrieveMostDiscussedVideoFeed(self):
    feed = self.client.GetMostDiscussedVideoFeed()
    self.assert_(isinstance(feed, gdata.youtube.YouTubeVideoFeed))
    self.assert_(len(feed.entry) > 10)

  def testRetrieveMostLinkedVideoFeed(self):
    feed = self.client.GetMostLinkedVideoFeed()
    self.assert_(isinstance(feed, gdata.youtube.YouTubeVideoFeed))
    self.assert_(len(feed.entry) > 10)

  def testRetrieveMostRespondedVideoFeed(self):
    feed = self.client.GetMostRespondedVideoFeed()
    self.assert_(isinstance(feed, gdata.youtube.YouTubeVideoFeed))
    self.assert_(len(feed.entry) > 10)

  def testRetrieveVideoEntryByUri(self):
    entry = self.client.GetYouTubeVideoEntry(
        'http://gdata.youtube.com/feeds/videos/Ncakifd_16k')
    self.assert_(isinstance(entry, gdata.youtube.YouTubeVideoEntry))
    self.assert_(entry.title.text != '')

  def testRetrieveVideoEntryByVideoId(self):
    entry = self.client.GetYouTubeVideoEntry(video_id='Ncakifd_16k')
    self.assert_(isinstance(entry, gdata.youtube.YouTubeVideoEntry))
    self.assert_(entry.title.text != '')

  def testRetrieveUserVideosbyUri(self):
    feed = self.client.GetYouTubeUserFeed(
        'http://gdata.youtube.com/feeds/users/gdpython/uploads')
    self.assert_(isinstance(feed, gdata.youtube.YouTubeVideoFeed))
    self.assert_(len(feed.entry) > 0)

  def testRetrieveUserVideosbyUsername(self):
    feed = self.client.GetYouTubeUserFeed(username='gdpython')
    self.assert_(isinstance(feed, gdata.youtube.YouTubeVideoFeed))
    self.assert_(len(feed.entry) > 0)

  def testSearchWithVideoQuery(self):
    query = gdata.youtube.service.YouTubeVideoQuery()
    query.vq = 'google'
    query.max_results = 8
    feed = self.client.YouTubeQuery(query)
    self.assert_(isinstance(feed, gdata.youtube.YouTubeVideoFeed))
    self.assertEquals(len(feed.entry), 8)

  def testDirectVideoUploadStatusUpdateAndDeletion(self):
    self.assertEquals(self.client._developer_key, developer_key)
    self.assertEquals(self.client._client_id, YOUTUBE_TEST_CLIENT_ID)
    self.assertEquals(self.client.additional_headers['X-GData-Key'],
        'key=' + developer_key)
    self.assertEquals(self.client.additional_headers['X-Gdata-Client'],
        YOUTUBE_TEST_CLIENT_ID)

    test_video_title = 'my cool video ' + str(random.randint(1000,5000))
    test_video_description = 'description ' + str(random.randint(1000,5000))

    my_media_group = gdata.media.Group(
      title = gdata.media.Title(text=test_video_title),
      description = gdata.media.Description(description_type='plain',
                                            text=test_video_description),
      keywords = gdata.media.Keywords(text='video, foo'),
      category = gdata.media.Category(
          text='Autos',
          scheme='http://gdata.youtube.com/schemas/2007/categories.cat',
          label='Autos'),
      player=None
    )
    self.assert_(isinstance(my_media_group, gdata.media.Group))

    video_entry = gdata.youtube.YouTubeVideoEntry(media=my_media_group)
    self.assert_(isinstance(video_entry, gdata.youtube.YouTubeVideoEntry))

    new_entry = self.client.InsertVideoEntry(video_entry, video_file_location)
    self.assert_(isinstance(new_entry, gdata.youtube.YouTubeVideoEntry))
    self.assertEquals(new_entry.title.text, test_video_title)
    self.assertEquals(new_entry.media.description.text, test_video_description)
    self.assert_(new_entry.id.text)

    # check upload status also
    upload_status = self.client.CheckUploadStatus(new_entry)
    self.assert_(upload_status[0] != '')

    # test updating entry meta-data
    new_video_description = 'description ' + str(random.randint(1000,5000))
    new_entry.media.description.text = new_video_description

    updated_entry = self.client.UpdateVideoEntry(new_entry)

    self.assert_(isinstance(updated_entry, gdata.youtube.YouTubeVideoEntry))
    self.assertEquals(updated_entry.media.description.text,
        new_video_description)

    # sleep for 10 seconds
    time.sleep(10)

    # test to delete the entry
    value = self.client.DeleteVideoEntry(updated_entry)

    if not value:
      # sleep more and try again
      time.sleep(20)
      # test to delete the entry
      value = self.client.DeleteVideoEntry(updated_entry)

    self.assert_(value == True)

  def testBrowserBasedVideoUpload(self):
    self.assertEquals(self.client._developer_key, developer_key)
    self.assertEquals(self.client._client_id, YOUTUBE_TEST_CLIENT_ID)
    self.assertEquals(self.client.additional_headers['X-GData-Key'],
        'key=' + developer_key)
    self.assertEquals(self.client.additional_headers['X-Gdata-Client'],
        YOUTUBE_TEST_CLIENT_ID)
    test_video_title = 'my cool video ' + str(random.randint(1000,5000))
    test_video_description = 'description ' + str(random.randint(1000,5000))

    my_media_group = gdata.media.Group(
      title = gdata.media.Title(text=test_video_title),
      description = gdata.media.Description(description_type='plain',
                                            text=test_video_description),
      keywords = gdata.media.Keywords(text='video, foo'),
      category = gdata.media.Category(
          text='Autos',
          scheme='http://gdata.youtube.com/schemas/2007/categories.cat',
          label='Autos'),
      player=None
    )
    self.assert_(isinstance(my_media_group, gdata.media.Group))

    video_entry = gdata.youtube.YouTubeVideoEntry(media=my_media_group)
    self.assert_(isinstance(video_entry, gdata.youtube.YouTubeVideoEntry))

    response = self.client.GetFormUploadToken(video_entry)
    self.assert_(response[0].startswith(
        'http://uploads.gdata.youtube.com/action/FormDataUpload/'))
    self.assert_(len(response[0]) > 55)
    self.assert_(len(response[1]) > 100)

  def testRetrieveRelatedVideoFeedByUri(self):
    feed = self.client.GetYouTubeRelatedVideoFeed(
        'http://gdata.youtube.com/feeds/videos/Ncakifd_16k/related')
    self.assert_(isinstance(feed, gdata.youtube.YouTubeVideoFeed))
    self.assert_(len(feed.entry) > 0)

  def testRetrieveRelatedVideoFeedById(self):
    feed = self.client.GetYouTubeRelatedVideoFeed(video_id = 'Ncakifd_16k')
    self.assert_(isinstance(feed, gdata.youtube.YouTubeVideoFeed))
    self.assert_(len(feed.entry) > 0)

  def testRetrieveResponseVideoFeedByUri(self):
    feed = self.client.GetYouTubeVideoResponseFeed(
        'http://gdata.youtube.com/feeds/videos/Ncakifd_16k/responses')
    self.assert_(isinstance(feed, gdata.youtube.YouTubeVideoResponseFeed))
    self.assert_(len(feed.entry) > 0)

  def testRetrieveResponseVideoFeedById(self):
    feed = self.client.GetYouTubeVideoResponseFeed(video_id='Ncakifd_16k')
    self.assert_(isinstance(feed, gdata.youtube.YouTubeVideoResponseFeed))
    self.assert_(len(feed.entry) > 0)

  def testAddVideoResponse(self):
    # TODO (jhartmann) - this works but needs to be removed since others can't
    # post my video as a response
    video_id_to_respond_to = 'Ncakifd_16k'
    response_video_id = '9g6buYJTt_g'
    video_entry = self.client.GetYouTubeVideoEntry(video_id=response_video_id)
    self.client.AddVideoResponse(video_id_to_respond_to, video_entry)
    response_feed = self.client.GetYouTubeVideoResponseFeed(
        video_id='Ncakifd_16k')
    self.assert_(isinstance(response_feed,
                            gdata.youtube.YouTubeVideoResponseFeed))

  def testRetrieveVideoCommentFeedByUri(self):
    feed = self.client.GetYouTubeVideoCommentFeed(
        'http://gdata.youtube.com/feeds/api/videos/Ncakifd_16k/comments')
    self.assert_(isinstance(feed, gdata.youtube.YouTubeVideoCommentFeed))
    self.assert_(len(feed.entry) > 0)

  def testRetrieveVideoCommentFeedByVideoId(self):
    feed = self.client.GetYouTubeVideoCommentFeed(video_id='Ncakifd_16k')
    self.assert_(isinstance(feed, gdata.youtube.YouTubeVideoCommentFeed))
    self.assert_(len(feed.entry) > 0)

  def testAddComment(self):
    video_id = '9g6buYJTt_g'
    video_entry = self.client.GetYouTubeVideoEntry(video_id=video_id)
    random_comment_text = 'test_comment_' + str(random.randint(1000,50000))
    self.client.AddComment(comment_text=random_comment_text,
                           video_entry=video_entry)
    comment_feed = self.client.GetYouTubeVideoCommentFeed(video_id=video_id)
    for item in comment_feed.entry:
      if (item.content.text == random_comment_text):
        comment_found = True
    self.assertEquals(comment_found, True)

  def testAddRating(self):
    video_id_to_rate = 'Ncakifd_16k'
    video_entry = self.client.GetYouTubeVideoEntry(video_id=video_id_to_rate)
    response = self.client.AddRating(3, video_entry)
    self.assert_(isinstance(response, gdata.GDataEntry))

  def testRetrievePlaylistFeedByUri(self):
    feed = self.client.GetYouTubePlaylistFeed(
        'http://gdata.youtube.com/feeds/users/gdpython/playlists')
    self.assert_(isinstance(feed, gdata.youtube.YouTubePlaylistFeed))
    self.assert_(len(feed.entry) > 0)

  def testRetrievePlaylistListFeedByUsername(self):
    feed = self.client.GetYouTubePlaylistFeed(username='gdpython')
    self.assert_(isinstance(feed, gdata.youtube.YouTubePlaylistFeed))
    self.assert_(len(feed.entry) > 0)

  def testRetrievePlaylistVideoFeed(self):
    feed = self.client.GetYouTubePlaylistVideoFeed(
        'http://gdata.youtube.com/feeds/api/playlists/BCB3BB96DF51B505')
    self.assert_(isinstance(feed, gdata.youtube.YouTubePlaylistVideoFeed))
    self.assert_(len(feed.entry) > 0)
    self.assert_(isinstance(feed.entry[0],
        gdata.youtube.YouTubePlaylistVideoEntry))

  def testAddAndDeletePlaylist(self):
    test_playlist_title = 'my test playlist ' + str(random.randint(1000,3000))
    test_playlist_description = 'test playlist '
    response = self.client.AddPlaylist(test_playlist_title,
                                       test_playlist_description)
    self.assert_(isinstance(response, gdata.youtube.YouTubePlaylistEntry))
    # delete it
    playlist_uri = response.id.text
    response = self.client.DeletePlaylist(playlist_uri)
    self.assertEquals(response, True)

  def testAddAndDeletePrivatePlaylist(self):
    test_playlist_title = 'my test playlist ' + str(random.randint(1000,3000))
    test_playlist_description = 'test playlist '
    response = self.client.AddPlaylist(test_playlist_title,
                                       test_playlist_description,
                                       playlist_private=True)
    self.assert_(isinstance(response, gdata.youtube.YouTubePlaylistEntry))
    # delete it
    playlist_uri = response.id.text
    response = self.client.DeletePlaylist(playlist_uri)
    self.assertEquals(response, True)

  def testAddEditAndDeleteVideoFromPlaylist(self):
    test_playlist_title = 'my test playlist ' + str(random.randint(1000,3000))
    test_playlist_description = 'test playlist '
    response = self.client.AddPlaylist(test_playlist_title,
                                       test_playlist_description)
    self.assert_(isinstance(response, gdata.youtube.YouTubePlaylistEntry))

    # add a video entry to the playlist with custom title and description
    custom_video_title = 'my test video on my test playlist'
    custom_video_description = 'this is a test video on my test playlist'
    video_id = 'Ncakifd_16k'
    playlist_uri = response.feed_link[0].href

    response = self.client.AddPlaylistVideoEntryToPlaylist(
        playlist_uri,
        video_id,
        custom_video_title,
        custom_video_description)
    self.assert_(isinstance(response, gdata.youtube.YouTubePlaylistVideoEntry))

    # update the title and description of the YouTubePlaylistVideoEntry
    playlist_entry_id = response.id.text.split('/')[-1]
    playlist_uri = response.id.text.split(playlist_entry_id)[0][:-1]
    new_video_title = 'video number ' + str(random.randint(1000,3000))
    new_video_description = 'test video'
    response = self.client.UpdatePlaylistVideoEntryMetaData(
        playlist_uri,
        playlist_entry_id,
        new_video_title,
        new_video_description,
        1)
    self.assert_(isinstance(response, gdata.youtube.YouTubePlaylistVideoEntry))

    # delete the playlist
    playlist_uri = response.id.text
    response = self.client.DeletePlaylist(playlist_uri)
    self.assertEquals(response, True)

  def testRetrieveSubscriptionFeedByUri(self):
    feed = self.client.GetYouTubeSubscriptionFeed(
        'http://gdata.youtube.com/feeds/users/gdpython/subscriptions')
    self.assert_(isinstance(feed, gdata.youtube.YouTubeSubscriptionFeed))
    self.assertEquals(len(feed.entry), 1)
    for entry in feed.entry:
      self.assert_(isinstance(entry, gdata.youtube.YouTubeSubscriptionEntry))

  def testRetrieveSubscriptionFeedByUsername(self):
    feed = self.client.GetYouTubeSubscriptionFeed(username='gdpython')
    self.assert_(isinstance(feed, gdata.youtube.YouTubeSubscriptionFeed))
    self.assertEquals(len(feed.entry), 1)
    for entry in feed.entry:
      self.assert_(isinstance(entry, gdata.youtube.YouTubeSubscriptionEntry))

  def testRetrieveUserProfileByUri(self):
    user = self.client.GetYouTubeUserEntry(
        'http://gdata.youtube.com/feeds/users/gdpython')
    self.assert_(isinstance(user, gdata.youtube.YouTubeUserEntry))
    self.assertEquals(user.location.text, 'US')

  def testRetrieveUserProfileByUsername(self):
    user = self.client.GetYouTubeUserEntry(username='gdpython')
    self.assert_(isinstance(user, gdata.youtube.YouTubeUserEntry))
    self.assertEquals(user.location.text, 'US')

  def testRetrieveUserFavoritesFeed(self):
    feed = self.client.GetUserFavoritesFeed(username='gdpython')
    self.assert_(isinstance(feed, gdata.youtube.YouTubeVideoFeed))
    self.assert_(len(feed.entry) > 0)

  def testRetrieveDefaultUserFavoritesFeed(self):
    feed = self.client.GetUserFavoritesFeed()
    self.assert_(isinstance(feed, gdata.youtube.YouTubeVideoFeed))
    self.assert_(len(feed.entry) > 0)

  def testAddAndDeleteVideoFromFavorites(self):
    video_id = 'Ncakifd_16k'
    video_entry = self.client.GetYouTubeVideoEntry(video_id=video_id)
    response = self.client.AddVideoEntryToFavorites(video_entry)
    self.assert_(isinstance(response, gdata.GDataEntry))
    # delete it
    response = self.client.DeleteVideoEntryFromFavorites(video_id)
    self.assertEquals(response, True)

  def testRetrieveContactFeedByUri(self):
    feed = self.client.GetYouTubeContactFeed(
        'http://gdata.youtube.com/feeds/users/gdpython/contacts')
    self.assert_(isinstance(feed, gdata.youtube.YouTubeContactFeed))
    self.assertEquals(len(feed.entry), 1)

  def testRetrieveContactFeedByUsername(self):
    feed = self.client.GetYouTubeContactFeed(username='gdpython')
    self.assert_(isinstance(feed, gdata.youtube.YouTubeContactFeed))
    self.assertEquals(len(feed.entry), 1)

if __name__ == '__main__':
  print ('NOTE: Please run these tests only with a test account. '
         'The tests may delete or update your data.')
  username = raw_input('Please enter your username: ')
  password = getpass.getpass()
  developer_key = raw_input('Please enter your developer key: ')
  video_file_location = raw_input(
      'Please enter the absolute path to a video file: ')
  unittest.main()
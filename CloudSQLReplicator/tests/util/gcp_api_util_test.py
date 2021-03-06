# Copyright 2018 The Pontem Authors. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests GCP API utility functions."""

import unittest
import mock
from mock import MagicMock
from google.auth import compute_engine
from google.cloud import storage

from google.cloud.pontem.sql.replicator.util import gcp_api_util


@mock.patch.object(
    compute_engine, 'Credentials',
    return_value=(None)
)
@mock.patch.object(
    storage, 'Client'
)
class TestStorageMethods(unittest.TestCase):
  """Test Storage methods"""


  def test_create_bucket(self, mock_compute_credentials, mock_storage_client):
    """Test that create bucket calls client correctly."""
    bucket_name = 'test_bucket'
    mock_storage_client.return_value = MagicMock()
    mock_create_bucket = mock_storage_client.return_value.create_bucket
    mock_create_bucket.return_value.name = 'test_bucket'

    gcp_api_util.create_bucket(bucket_name)

    mock_compute_credentials.assert_called_with()
    mock_create_bucket.assert_called_with(bucket_name)


  def test_delete_bucket(self, mock_compute_credentials, mock_storage_client):
    """Test that delete bucket calls client correctly."""
    bucket_name = 'test_bucket'
    mock_storage_client.return_value = MagicMock()
    mock_get_bucket = mock_storage_client.return_value.get_bucket
    mock_get_bucket.return_value.name = 'test_bucket'
    mock_get_bucket.return_value.delete = MagicMock()
    mock_delete_bucket = mock_get_bucket.return_value.delete

    gcp_api_util.delete_bucket(bucket_name)

    mock_compute_credentials.assert_called_with()
    mock_get_bucket.assert_called_with(bucket_name)
    mock_delete_bucket.assert_called_once_with()

  def test_delete_blob(self, mock_compute_credentials, mock_storage_client):
    """Test that delete bucket calls client correctly."""
    bucket_name = 'test_bucket'
    blob_name = 'test_blob'
    mock_storage_client.return_value = MagicMock()
    mock_get_bucket = mock_storage_client.return_value.get_bucket
    mock_get_bucket.return_value.name = 'test_bucket'
    mock_get_bucket.return_value.blob = MagicMock()
    mock_blob = mock_get_bucket.return_value.blob
    mock_blob.return_value.delete = MagicMock()
    mock_delete_blob = mock_blob.delete

    gcp_api_util.delete_blob(bucket_name, blob_name)

    mock_compute_credentials.assert_called_with()
    mock_get_bucket.assert_called_with(bucket_name)
    mock_blob.assert_called_once_with(blob_name)
    mock_delete_blob.assert_called_once_with()

if __name__ == '__main__':
  unittest.main()

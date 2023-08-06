# -*- coding:utf-8 -*-
#
# Copyright 2019, Couchbase, Inc.
# All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from couchbase_tests.base import CollectionTestCase
from couchbase.cluster import ClusterOptions, ClassicAuthenticator, PasswordAuthenticator
from couchbase.collection import GetOptions, UpsertOptions, ReplaceOptions, InsertOptions, \
    RemoveOptions
from couchbase.durability import ServerDurability, ClientDurability, Durability, PersistTo, ReplicateTo
from couchbase.exceptions import InvalidArgumentException, DocumentExistsException, DocumentNotFoundException, \
    TemporaryFailException, PathNotFoundException, DocumentLockedException, CASMismatchException
import unittest
from datetime import timedelta
from unittest import SkipTest
from couchbase.diagnostics import ServiceType
import logging
from couchbase.management.collections import CollectionSpec
import uuid
from datetime import datetime
from flaky import flaky
import warnings
import time


class CollectionTests(CollectionTestCase):
    """
    These tests should just test the collection interface, as simply
    as possible.  We have the Scenario tests for more complicated
    stuff.
    """
    CONTENT = {"some": "content"}
    KEY = "imakey"
    NOKEY = "somerandomkey"

    def setUp(self):
        super(CollectionTests, self).setUp()
        # retry just in case doc is locked from previous test
        self.try_n_times(10, 3, self.cb.upsert, self.KEY, self.CONTENT)
        # be sure NOKEY isn't in there
        try:
            self.cb.remove(self.NOKEY)
        except DocumentNotFoundException as e:
            pass
        # make sure NOKEY is gone
        self.try_n_times_till_exception(10, 1, self.cb.get, self.NOKEY)

    def test_exists(self):
        if self.is_mock:
            raise SkipTest("mock does not support exists")
        self.assertTrue(self.cb.exists(self.KEY).exists)

    def test_exists_when_it_does_not_exist(self):
        if self.is_mock:
            raise SkipTest("mock does not support exists")
        key = str(uuid.uuid4())
        self.assertRaises(DocumentNotFoundException, self.cb.get, key)
        self.assertFalse(self.cb.exists(key).exists)

    def test_exists_with_recently_removed_key(self):
        if self.is_mock:
            raise SkipTest("mock does not support exists")
        self.cb.remove(self.KEY)
        self.assertRaises(DocumentNotFoundException, self.cb.get, self.KEY)
        self.assertFalse(self.cb.exists(self.KEY).exists)

    def test_upsert(self):
        self.cb.upsert(self.NOKEY, {"some": "thing"},
                       UpsertOptions(timeout=timedelta(seconds=3)))
        result = self.try_n_times(10, 1, self.cb.get, self.NOKEY)
        self.assertEqual(self.NOKEY, result.id)
        self.assertDictEqual({"some": "thing"}, result.content_as[dict])

    def test_upsert_preserve_expiry_not_used(self):
        if self.is_mock:
            raise SkipTest("Mock does not support preserve expiry")
        if int(self.get_cluster_version().split('.')[0]) < 7:
            raise SkipTest("Preserve expiry only in CBS 7.0+")
        result = self.cb.upsert(self.KEY, {"some": "other content"}, UpsertOptions(
            expiry=timedelta(seconds=5)))
        expiry1 = self.cb.get(self.KEY, GetOptions(
            with_expiry=True)).expiryTime
        result = self.cb.upsert(self.KEY, {"some": "replaced content"})
        self.assertTrue(result.success)
        expiry2 = self.cb.get(self.KEY, GetOptions(
            with_expiry=True)).expiryTime
        self.assertIsNotNone(expiry1)
        self.assertIsInstance(expiry1, datetime)
        self.assertIsNone(expiry2)
        self.assertNotEqual(expiry1, expiry2)
        # if expiry was set, should be expired by now
        time.sleep(6)
        result = self.cb.get(self.KEY)
        self.assertIsNotNone(result)

    def test_upsert_preserve_expiry(self):
        if self.is_mock:
            raise SkipTest("Mock does not support preserve expiry")
        if int(self.get_cluster_version().split('.')[0]) < 7:
            raise SkipTest("Preserve expiry only in CBS 7.0+")
        result = self.cb.upsert(self.KEY, {"some": "other content"}, UpsertOptions(
            expiry=timedelta(seconds=5)))
        expiry1 = self.cb.get(self.KEY, GetOptions(
            with_expiry=True)).expiryTime
        result = self.cb.upsert(
            self.KEY, {"some": "replaced content"}, UpsertOptions(preserve_expiry=True))
        self.assertTrue(result.success)
        expiry2 = self.cb.get(self.KEY, GetOptions(
            with_expiry=True)).expiryTime
        self.assertIsNotNone(expiry1)
        self.assertIsInstance(expiry1, datetime)
        self.assertIsNotNone(expiry2)
        self.assertIsInstance(expiry2, datetime)
        self.assertEqual(expiry1, expiry2)
        # if expiry was preserved, should be expired by now
        time.sleep(6)
        with self.assertRaises(DocumentNotFoundException):
            self.cb.get(self.KEY)

    def test_insert(self):
        self.cb.insert(self.NOKEY, {"some": "thing"})
        result = self.try_n_times(10, 1, self.cb.get, self.NOKEY)
        self.assertEqual(self.NOKEY, result.id)
        self.assertDictEqual({"some": "thing"}, result.content_as[dict])

    def test_insert_fail(self):
        self.assertRaises(DocumentExistsException,
                          self.cb.insert, self.KEY, self.CONTENT)

    def test_replace(self):
        result = self.cb.replace(self.KEY, {"some": "other content"})
        self.assertTrue(result.success)

    def test_replace_preserve_expiry_not_used(self):
        if self.is_mock:
            raise SkipTest("Mock does not support preserve expiry")
        if int(self.get_cluster_version().split('.')[0]) < 7:
            raise SkipTest("Preserve expiry only in CBS 7.0+")
        result = self.cb.upsert(self.KEY, {"some": "other content"}, UpsertOptions(
            expiry=timedelta(seconds=5)))
        expiry1 = self.cb.get(self.KEY, GetOptions(
            with_expiry=True)).expiryTime
        result = self.cb.replace(self.KEY, {"some": "replaced content"})
        self.assertTrue(result.success)
        expiry2 = self.cb.get(self.KEY, GetOptions(
            with_expiry=True)).expiryTime
        self.assertIsNotNone(expiry1)
        self.assertIsInstance(expiry1, datetime)
        self.assertIsNone(expiry2)
        self.assertNotEqual(expiry1, expiry2)
        # if expiry was set, should be expired by now
        time.sleep(6)
        result = self.cb.get(self.KEY)
        self.assertIsNotNone(result)

    def test_replace_preserve_expiry(self):
        if self.is_mock:
            raise SkipTest("Mock does not support preserve expiry")
        if int(self.get_cluster_version().split('.')[0]) < 7:
            raise SkipTest("Preserve expiry only in CBS 7.0+")
        result = self.cb.upsert(self.KEY, {"some": "other content"}, UpsertOptions(
            expiry=timedelta(seconds=5)))
        expiry1 = self.cb.get(self.KEY, GetOptions(
            with_expiry=True)).expiryTime
        result = self.cb.replace(
            self.KEY, {"some": "replaced content"}, ReplaceOptions(preserve_expiry=True))
        self.assertTrue(result.success)
        expiry2 = self.cb.get(self.KEY, GetOptions(
            with_expiry=True)).expiryTime
        self.assertIsNotNone(expiry1)
        self.assertIsInstance(expiry1, datetime)
        self.assertIsNotNone(expiry2)
        self.assertIsInstance(expiry2, datetime)
        self.assertEqual(expiry1, expiry2)
        # if expiry was preserved, should be expired by now
        time.sleep(6)
        with self.assertRaises(DocumentNotFoundException):
            self.cb.get(self.KEY)

    def test_replace_preserve_expiry_fail(self):
        if self.is_mock:
            raise SkipTest("Mock does not support preserve expiry")
        if int(self.get_cluster_version().split('.')[0]) < 7:
            raise SkipTest("Preserve expiry only in CBS 7.0+")
        opts = ReplaceOptions(
            expiry=timedelta(
                seconds=5),
            preserve_expiry=True)
        with self.assertRaises(InvalidArgumentException):
            self.cb.replace(self.KEY, {"some": "other content"}, opts)

    def test_replace_with_cas(self):
        old_cas = self.cb.get(self.KEY).cas
        result = self.cb.replace(
            self.KEY, self.CONTENT, ReplaceOptions(cas=old_cas))
        self.assertTrue(result.success)
        # try same cas again, must fail.
        self.assertRaises(CASMismatchException, self.cb.replace,
                          self.KEY, self.CONTENT, ReplaceOptions(cas=old_cas))

    def test_replace_fail(self):
        self.assertRaises(DocumentNotFoundException, self.cb.get, self.NOKEY)
        self.assertRaises(DocumentNotFoundException,
                          self.cb.replace, self.NOKEY, self.CONTENT)

    def test_remove(self):
        result = self.cb.remove(self.KEY)
        self.assertTrue(result.success)
        self.try_n_times_till_exception(10, 1, self.cb.get, self.KEY)

    def test_remove_fail(self):
        self.assertRaises(DocumentNotFoundException,
                          self.cb.remove, self.NOKEY)

    def test_get(self):
        result = self.cb.get(self.KEY)
        self.assertIsNotNone(result.cas)
        self.assertEqual(result.id, self.KEY)
        self.assertIsNone(result.expiryTime)
        self.assertDictEqual(self.CONTENT, result.content_as[dict])

    def test_get_options(self):
        result = self.cb.get(self.KEY, GetOptions(
            timeout=timedelta(seconds=2), with_expiry=False))
        self.assertIsNotNone(result.cas)
        self.assertEqual(result.id, self.KEY)
        self.assertIsNone(result.expiryTime)
        self.assertDictEqual(self.CONTENT, result.content_as[dict])

    def test_get_fails(self):
        self.assertRaises(DocumentNotFoundException, self.cb.get, self.NOKEY)

    def test_expiry_really_expires(self):
        result = self.coll.upsert(
            self.KEY, self.CONTENT, UpsertOptions(expiry=timedelta(seconds=3)))
        self.assertTrue(result.success)
        time.sleep(4)
        with self.assertRaises(DocumentNotFoundException):
            self.coll.get(self.KEY)

    def test_get_with_expiry(self):
        if self.is_mock:
            raise SkipTest("mock will not return the expiry in the xaddrs")
        self.coll.upsert(self.KEY, self.CONTENT, UpsertOptions(
            expiry=timedelta(seconds=1000)))

        result = self.coll.get(self.KEY, GetOptions(with_expiry=True))
        self.assertIsNotNone(result.expiryTime)
        self.assertDictEqual(self.CONTENT, result.content_as[dict])
        expires_in = (result.expiryTime - datetime.now()).total_seconds()
        self.assertTrue(1001 >= expires_in > 0,
                        msg="Expected expires_in {} to be between 1000 and 0".format(expires_in))

    def test_deprecated_expiry(self):
        # PYCBC-999 Deprecate GetResult.expiry()
        # expiry returned datetime, was replaced by expiryTime which returns
        # an instant (aka unix timestamp)
        if self.is_mock:
            raise SkipTest("mock will not return the expiry in the xaddrs")
        self.coll.upsert(self.KEY, self.CONTENT, UpsertOptions(
            expiry=timedelta(seconds=1000)))
        result = self.coll.get(self.KEY, GetOptions(with_expiry=True))
        warnings.resetwarnings()
        with warnings.catch_warnings(record=True) as w:
            self.assertIsNotNone(result.expiry)
            self.assertEqual(len(w), 1)

        expires_in = (result.expiry - datetime.now()).total_seconds()
        self.assertTrue(1001 >= expires_in > 0,
                        msg="Expected expires_in {} to be between 1000 and 0".format(expires_in))

    def test_project(self):
        content = {"a": "aaa", "b": "bbb", "c": "ccc"}
        cas = self.coll.upsert(self.KEY, content).cas

        def cas_matches(c, new_cas):
            if new_cas != c.get(self.KEY).cas:
                raise Exception("nope")

        self.try_n_times(10, 3, cas_matches, self.coll, cas)
        result = self.coll.get(self.KEY, GetOptions(project=["a"]))
        self.assertEqual({"a": "aaa"}, result.content_as[dict])
        self.assertIsNotNone(result.cas)
        self.assertEqual(result.id, self.KEY)
        self.assertIsNone(result.expiryTime)

    def test_project_bad_path(self):
        result = self.coll.get(self.KEY, GetOptions(project=["some", "qzx"]))
        self.assertTrue(result.success)
        with self.assertRaisesRegex(PathNotFoundException, 'qzx'):
            result.content_as[dict]

    def test_project_bad_project_string(self):
        with self.assertRaises(InvalidArgumentException):
            self.coll.get(self.KEY, GetOptions(project="something"))

    def test_project_bad_project_too_long(self):
        project = []
        for _ in range(17):
            project.append("something")

        with self.assertRaisesRegex(InvalidArgumentException, "16 operations or less"):
            self.coll.get(self.KEY, GetOptions(project=project))

    def _check_replicas(self, all_up=True):
        num_replicas = self.bucket.configured_replica_count
        if num_replicas < 1:
            raise SkipTest('need replicas to test get_all/get_any_replicas')
            # TODO: this is far to difficult - having to use the test framework
            # to get the bucket
        kv_results = self.bucket.ping().endpoints.get(ServiceType.KeyValue, None)
        # 2 means at least one replica is up
        num_expected = num_replicas + 1 if all_up else 2
        if not kv_results or len(kv_results) < num_expected:
            raise SkipTest('not all replicas are online')

    def test_get_any_replica(self):
        self._check_replicas(False)
        self.coll.upsert('imakey100', self.CONTENT)
        result = self.try_n_times(
            10, 3, self.coll.get_any_replica, 'imakey100')
        self.assertDictEqual(self.CONTENT, result.content_as[dict])

    def test_get_all_replicas(self):
        self._check_replicas()
        self.coll.upsert(self.KEY, self.CONTENT)
        # wait till it it there...
        result = self.try_n_times(10, 3, self.coll.get_all_replicas, self.KEY)
        if not hasattr(result, '__iter__'):
            result = [result]
        for r in result:
            self.assertDictEqual(self.CONTENT, r.content_as[dict])

    def test_get_all_replicas_returns_master(self):
        self._check_replicas()
        self.coll.upsert('imakey100', self.CONTENT)
        result = self.try_n_times(
            10, 3, self.coll.get_all_replicas, 'imakey100')
        if not hasattr(result, '__iter__'):
            result = [result]
        active_cnt = 0
        replica_cnt = 0
        for r in result:
            self.assertDictEqual(self.CONTENT, r.content_as[dict])
            if r.is_active:
                active_cnt += 1
            else:
                replica_cnt += 1

        self.assertEqual(active_cnt, 1)
        self.assertGreaterEqual(replica_cnt, active_cnt)

    def test_touch(self):
        self.cb.touch(self.KEY, timedelta(seconds=3))
        time.sleep(4)
        with self.assertRaises(DocumentNotFoundException):
            self.cb.get(self.KEY)

    def test_touch_no_expire(self):
        if self.is_mock:
            self.cb.touch(self.KEY, timedelta(seconds=0))
            time.sleep(1)
            res = self.cb.get(self.KEY)
            self.assertIsNotNone(res.content_as[dict])
        else:
            self.cb.touch(self.KEY, timedelta(seconds=15))
            expiry = self.cb.get(
                self.KEY, GetOptions(
                    with_expiry=True)).expiryTime
            self.assertIsNotNone(expiry)
            self.cb.touch(self.KEY, timedelta(seconds=0))
            expiry = self.cb.get(
                self.KEY, GetOptions(
                    with_expiry=True)).expiryTime
            self.assertIsNone(expiry)

    def _authenticator(self):
        if self.is_mock:
            return ClassicAuthenticator(
                self.cluster_info.admin_username, self.cluster_info.admin_password)
        return PasswordAuthenticator(
            self.cluster_info.admin_username, self.cluster_info.admin_password)

    def _create_cluster_opts(self, **kwargs):
        return ClusterOptions(self._authenticator(), **kwargs)

    def _mock_hack(self):
        if self.is_mock:
            return {'bucket': self.bucket_name}
        return {}

    def test_get_and_touch(self):
        self.cb.get_and_touch(self.KEY, timedelta(seconds=3))
        self.cb.get(self.KEY)
        self.try_n_times_till_exception(
            10, 3, self.cb.get, self.KEY, DocumentNotFoundException)

    def test_get_and_touch_no_expire(self):
        if self.is_mock:
            self.cb.get_and_touch(self.KEY, timedelta(seconds=0))
            time.sleep(1)
            res = self.cb.get(self.KEY)
            self.assertIsNotNone(res.content_as[dict])
        else:
            self.cb.get_and_touch(self.KEY, timedelta(seconds=15))
            expiry = self.cb.get(
                self.KEY, GetOptions(
                    with_expiry=True)).expiryTime
            self.assertIsNotNone(expiry)
            self.cb.get_and_touch(self.KEY, timedelta(seconds=0))
            expiry = self.cb.get(
                self.KEY, GetOptions(
                    with_expiry=True)).expiryTime
            self.assertIsNone(expiry)

    def test_get_and_lock(self):
        self.cb.get_and_lock(self.KEY, timedelta(seconds=3))
        # upsert should definitely fail
        self.assertRaises(DocumentLockedException,
                          self.cb.upsert, self.KEY, self.CONTENT)
        # but succeed eventually
        self.try_n_times(10, 1, self.cb.upsert, self.KEY, self.CONTENT)

    def test_get_after_lock(self):
        orig = self.cb.get_and_lock(self.KEY, timedelta(seconds=3))
        # GET operation is allowed on locked document; however, returned CAS
        # should be invalid
        res = self.cb.get(self.KEY)
        self.assertEqual(orig.content_as[dict], res.content_as[dict])
        self.assertNotEqual(orig.cas, res.cas)

    def test_get_and_lock_upsert_with_cas(self):
        result = self.cb.get_and_lock(self.KEY, timedelta(seconds=15))
        cas = result.cas
        self.assertRaises(DocumentLockedException,
                          self.cb.upsert, self.KEY, self.CONTENT)
        self.cb.replace(self.KEY, self.CONTENT, ReplaceOptions(cas=cas))

    def test_unlock(self):
        cas = self.cb.get_and_lock(self.KEY, timedelta(seconds=15)).cas
        self.cb.unlock(self.KEY, cas)
        self.cb.upsert(self.KEY, self.CONTENT)

    @flaky(5, 1)
    def test_unlock_wrong_cas(self):
        cas = self.cb.get_and_lock(self.KEY, timedelta(seconds=15)).cas
        expectedException = TemporaryFailException if self.is_mock else DocumentLockedException
        self.assertRaises(expectedException, self.cb.unlock, self.KEY, 100)
        self.cb.unlock(self.KEY, cas)

    def test_client_durable_upsert(self):
        num_replicas = self.bucket._bucket.configured_replica_count
        durability = ClientDurability(
            persist_to=PersistTo.ONE, replicate_to=ReplicateTo(num_replicas))
        self.cb.upsert(self.NOKEY, self.CONTENT,
                       UpsertOptions(durability=durability))
        result = self.cb.get(self.NOKEY)
        self.assertEqual(self.CONTENT, result.content_as[dict])

    def test_server_durable_upsert(self):
        if not self.supports_sync_durability():
            raise SkipTest("ServerDurability not supported")
        durability = ServerDurability(level=Durability.PERSIST_TO_MAJORITY)
        self.cb.upsert(self.NOKEY, self.CONTENT,
                       UpsertOptions(durability=durability))
        result = self.cb.get(self.NOKEY)
        self.assertEqual(self.CONTENT, result.content_as[dict])

    def test_client_durable_insert(self):
        num_replicas = self.bucket._bucket.configured_replica_count
        durability = ClientDurability(
            persist_to=PersistTo.ONE, replicate_to=ReplicateTo(num_replicas))
        self.cb.insert(self.NOKEY, self.CONTENT,
                       InsertOptions(durability=durability))
        result = self.cb.get(self.NOKEY)
        self.assertEqual(self.CONTENT, result.content_as[dict])

    def test_server_durable_insert(self):
        if not self.supports_sync_durability():
            raise SkipTest("ServerDurability not supported")
        durability = ServerDurability(level=Durability.PERSIST_TO_MAJORITY)
        self.cb.insert(self.NOKEY, self.CONTENT,
                       InsertOptions(durability=durability))
        result = self.cb.get(self.NOKEY)
        self.assertEqual(self.CONTENT, result.content_as[dict])

    def test_client_durable_replace(self):
        num_replicas = self.bucket._bucket.configured_replica_count
        content = {"new": "content"}
        durability = ClientDurability(
            persist_to=PersistTo.ONE, replicate_to=ReplicateTo(num_replicas))
        self.cb.replace(self.KEY, content,
                        ReplaceOptions(durability=durability))
        result = self.cb.get(self.KEY)
        self.assertEqual(content, result.content_as[dict])

    def test_server_durable_replace(self):
        content = {"new": "content"}
        if not self.supports_sync_durability():
            raise SkipTest("ServerDurability not supported")
        durability = ServerDurability(level=Durability.PERSIST_TO_MAJORITY)
        self.cb.replace(self.KEY, content,
                        ReplaceOptions(durability=durability))
        result = self.cb.get(self.KEY)
        self.assertEqual(content, result.content_as[dict])

    @unittest.skip("Client Durable remove not yet supported (CCBC-1199)")
    def test_client_durable_remove(self):
        num_replicas = self.bucket._bucket.configured_replica_count
        durability = ClientDurability(
            persist_to=PersistTo.ONE, replicate_to=ReplicateTo(num_replicas))
        self.cb.remove(self.KEY, RemoveOptions(durability=durability))
        self.assertRaises(DocumentNotFoundException, self.cb.get, self.KEY)

    def test_server_durable_remove(self):
        if not self.supports_sync_durability():
            raise SkipTest("ServerDurability not supported")
        durability = ServerDurability(level=Durability.PERSIST_TO_MAJORITY)
        self.cb.remove(self.KEY, RemoveOptions(durability=durability))
        self.assertRaises(DocumentNotFoundException, self.cb.get, self.KEY)

    def test_collection_access(self,  # type: CollectionTests
                               ):
        if not self.supports_collections():
            raise SkipTest()

        value = uuid.uuid4().int
        value_1 = str(value)
        value_2 = str(value + 1)
        value_3 = str(value + 2)
        value_4 = str(value + 3)
        test_dict = {
            "scope_1": {
                "collection_1": {"key_1": value_1},
                "collection_2": {"key_1": value_2},
            },
            "scope_2": {
                "collection_1": {"key_1": value_3},
                "collection_2": {"key_1": value_4},
            }
        }

        bucket = self.cluster.bucket(self.cluster_info.bucket_name)
        cm = bucket.collections()

        def upsert_values(coll, scope_name, coll_name,
                          result_key_dict, key, value):
            return coll.upsert(key, value)
        from collections import defaultdict

        def recurse():
            return defaultdict(recurse)
        resultdict = recurse()

        def check_values(coll, scope_name, coll_name,
                         result_key_dict, key, value):
            result_key_dict[key] = coll.get(key).content
            return True
        for action in [upsert_values, check_values]:
            self._traverse_scope_tree(
                bucket, cm, resultdict, test_dict, action)

        self.assertSanitizedEqual(test_dict, resultdict)

    def _traverse_scope_tree(
            self, bucket, cm, result_dict, test_dict, coll_verb):
        for scope_name, coll_dict in test_dict.items():
            result_coll_dict = result_dict[scope_name]
            logging.error("Creating scope {}".format(scope_name))
            try:
                cm.create_scope(scope_name)
            except BaseException:
                pass
            scope = bucket.scope(scope_name)
            for coll_name, key_dict in coll_dict.items():
                result_key_dict = result_coll_dict[coll_name]
                logging.error(
                    "Creating collection {} in scope {}".format(
                        coll_name, scope_name)
                )
                try:
                    cm.create_collection(
                        CollectionSpec(scope_name=scope_name,
                                       collection_name=coll_name)
                    )
                except BaseException:
                    pass
                coll = scope.collection(coll_name)
                for key, value in key_dict.items():
                    result = coll_verb(
                        coll, scope_name, coll_name, result_key_dict, key, value)
                    logging.error(
                        "Called {} on {} to {} in {} and got {}".format(
                            coll_verb,
                            key,
                            value,
                            dict(scope_name=scope_name, coll_name=coll_name),
                            result,
                        )
                    )

    def test_document_expiry_values(self):
        if self.is_mock:
            raise SkipTest("Mock will not return the expiry in the xaddrs")

        fifty_years = 50 * 365 * 24 * 60 * 60
        thirty_days = 30 * 24 * 60 * 60
        now = int(time.time() - 1.0)
        ttls = [
            fifty_years + 1,
            fifty_years,
            thirty_days - 1,
            thirty_days,
            now + 60,
            60,
            -1
        ]

        options = GetOptions(with_expiry=True)

        for ttl in ttls:
            warns = []
            expiry = timedelta(seconds=ttl)
            warnings.resetwarnings()
            with warnings.catch_warnings(record=True) as ws:
                try:
                    result = self.cb.upsert(self.NOKEY, {"x": "y"},
                                            expiry=expiry)
                    self.assertTrue(result.success)
                    warns = ws
                except InvalidArgumentException:
                    if ttl != -1:
                        raise
                    continue
            result = self.try_n_times(10, 1, self.cb.get, self.NOKEY, options)

            then = int(time.time() + 1.0)
            # PYCBC-1177: removed deprecated code, so no more warnings
            self.assertEqual(len(warns), 0)
            # server interprets ttl < 30 day sas duration, ttl >= 30 days
            # client converts to timestamp. Either way expiryTime is a timestamp.
            self.assertTrue(
                now + ttl <= int(result.expiryTime.timestamp()) <= then + ttl)

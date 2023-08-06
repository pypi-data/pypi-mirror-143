# -*- coding:utf-8 -*-
#
# Copyright 2020, Couchbase, Inc.
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

from unittest import SkipTest

import couchbase.search as search
from couchbase.management.search import SearchIndex
from couchbase.search import MatchOperator, SearchResult, SearchOptions
from couchbase.mutation_state import MutationState
from couchbase_tests.base import CouchbaseTestCase, CollectionTestCase
from couchbase.exceptions import NotSupportedException
import string
import random

try:
    from abc import ABC
except BaseException:
    from abc import ABCMeta

import datetime

import couchbase.exceptions

from datetime import timedelta
from couchbase_core import iterable_wrapper

from couchbase_tests.base import ClusterTestCase
import couchbase.management
import json
import os
from couchbase.tests_v3.cases import sdk_testcases
import time

search_testcases = os.path.join(sdk_testcases, "search")


class MRESWrapper(object):
    def __init__(self, **orig_json):
        self._orig_json = orig_json
        self._hits = self._orig_json['data'].pop('hits')
        self.done = False
        try:
            self._iterhits = iter(self._hits)
        except Exception as e:
            raise

    @property
    def value(self):
        return self._orig_json['data']

    def fetch(self, _):
        yield from self._iterhits
        self.done = True


class SearchRequestMock(search.SearchRequest):
    def __init__(self, body, parent, orig_json, **kwargs):
        self._orig_json = orig_json
        super(SearchRequestMock, self).__init__(body, parent, **kwargs)

    def _start(self):
        if self._mres:
            return

        self._mres = {None: MRESWrapper(**self._orig_json)}
        self.__raw = self._mres[None]

    @property
    def raw(self):
        try:
            return self._mres[None]
        except Exception as e:
            raise


class SearchResultMock(search.SearchResultBase,
                       iterable_wrapper(SearchRequestMock)):
    pass


class SearchResultTest(CouchbaseTestCase):

    def _check_search_result(self, initial, min_hits, x):
        duration = datetime.datetime.now() - initial

        SearchResultTest._check_search_results_min_hits(self, min_hits, x)
        took = x.metadata().metrics.took
        self.assertIsInstance(took, timedelta)
        # commented out because 'took' doesn't seem to be accurate
        # self.assertAlmostEqual(took.total_seconds(), duration.total_seconds(), delta=2)

    def _check_search_results_min_hits(self, min_hits, x):
        self.assertGreaterEqual(len(x.rows()), min_hits)
        for entry in x.rows():
            self.assertIsInstance(entry, search.SearchRow)
            self.assertIsInstance(entry.id, str)
            self.assertIsInstance(entry.score, float)
            self.assertIsInstance(entry.index, str)
            self.assertIsInstance(entry.fields, dict)
            self.assertIsInstance(entry.locations, search.SearchRowLocations)
            for location in entry.fields:
                self.assertIsInstance(location, str)
        metadata = x.metadata()
        self.assertIsInstance(metadata, search.SearchMetaData)
        metrics = metadata.metrics
        self.assertIsInstance(metrics.error_partition_count, int)
        self.assertIsInstance(metrics.max_score, float)
        self.assertIsInstance(metrics.success_partition_count, int)
        self.assertEqual(metrics.error_partition_count +
                         metrics.success_partition_count, metrics.total_partition_count)
        took = metrics.took
        # TODO: lets revisit why we chose this 0.1.  I often find the difference is greater,
        # running the tests locally.  Commenting out for now...
        self.assertGreater(took.total_seconds(), 0)
        self.assertIsInstance(metadata.metrics.total_partition_count, int)
        min_partition_count = min(
            metadata.metrics.total_partition_count, min_hits)
        self.assertGreaterEqual(
            metadata.metrics.success_partition_count, min_partition_count)
        self.assertGreaterEqual(metadata.metrics.total_rows, min_hits)

    def test_parsing_locations(self):
        with open(os.path.join(search_testcases, "good-response-61.json")) as good_response_f:
            input = good_response_f.read()
            raw_json = json.loads(input)
            good_response = SearchResultMock(None, None, raw_json)
            first_row = good_response.rows()[0]
            self.assertIsInstance(first_row, search.SearchRow)
            locations = first_row.locations
            self.assertEqual(
                [search.SearchRowLocation(field='airlineid', term='airline_137', position=1, start=0, end=11, array_positions=None)], locations.get("airlineid", "airline_137"))
            self.assertEqual([search.SearchRowLocation(field='airlineid', term='airline_137',
                             position=1, start=0, end=11, array_positions=None)], locations.get_all())
            self.assertSetEqual({'airline_137'}, locations.terms())
            self.assertEqual(['airline_137'], locations.terms_for("airlineid"))
            self._check_search_results_min_hits(1, good_response)


# YUCK!  But, easiest way to keep state w/o a significant change
# The problem:
#   cbdyncluster w/in Jenkins on typically on CBS 6.0.3 & 6.5.x will not populate
#   the FTS index causing all tests to fail.  So, it is a substantial waste of time
#   to try and complete the tests in this scenario, just skip them all
#
# TODO:
#   * move away from nose to remove the lack of flexibility w/in the current test suite
#   * figure out a better way to populate the FTS index...assuming it is possible
#       maybe load it when building the cluster?
#
_SKIP_TESTS_NO_DOCS_INDEXED = False


class SearchTest(ClusterTestCase):

    @classmethod
    def setUpClass(cls) -> None:
        global _SKIP_TESTS_NO_DOCS_INDEXED
        _SKIP_TESTS_NO_DOCS_INDEXED = False
        super(SearchTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        global _SKIP_TESTS_NO_DOCS_INDEXED
        _SKIP_TESTS_NO_DOCS_INDEXED = False
        super(SearchTest, cls).tearDownClass()

    def setUp(self, *args, **kwargs):
        super(SearchTest, self).setUp(**kwargs)
        if self.is_mock:
            raise SkipTest("Search not available on Mock")

        global _SKIP_TESTS_NO_DOCS_INDEXED
        if _SKIP_TESTS_NO_DOCS_INDEXED is True:
            raise SkipTest("No docs indexed, skipping test.")

        self.sm = self.cluster.search_indexes()
        with open(os.path.join(search_testcases, "beer-search-index-params.json")) as params_file:
            input = params_file.read()
            params_json = json.loads(input)
            try:
                self.sm.get_index('beer-search-index')
                # total of 3 minutes
                indexed_docs = self._check_indexed_docs(retries=18, delay=10)
            except Exception:
                self.sm.upsert_index(
                    SearchIndex(name="beer-search-index",
                                idx_type="fulltext-index",
                                source_name="beer-sample",
                                source_type="couchbase",
                                params=params_json)
                )
                # make sure the index loads...
                indexed_docs = self._check_indexed_docs()

        if indexed_docs == 0:
            _SKIP_TESTS_NO_DOCS_INDEXED = True

        if _SKIP_TESTS_NO_DOCS_INDEXED is True:
            raise SkipTest("No docs indexed, skipping test.")

    def _check_indexed_docs(self, retries=20, delay=30, num_docs=3000, idx="beer-search-index"):
        indexed_docs = 0
        no_docs_cutoff = 300
        for i in range(retries):
            # if no docs after waiting for a period of time, exit
            if indexed_docs == 0 and i * delay >= no_docs_cutoff:
                return 0
            indexed_docs = self.try_n_times(
                10, 10, self.sm.get_indexed_documents_count, idx)
            if indexed_docs >= num_docs:
                break
            print('Found {} indexed docs, waiting a bit...'.format(
                indexed_docs))
            time.sleep(delay)

        return indexed_docs

    def test_cluster_search(self):
        initial = datetime.datetime.now()
        x = self.try_n_times_decorator(self.cluster.search_query, 10, 10)("beer-search-index",
                                                                          search.TermQuery(
                                                                              "north"),
                                                                          search.SearchOptions(limit=10))  # type: SearchResult
        SearchResultTest._check_search_result(self, initial, 1, x)

    def test_cluster_search_fields(self  # type: SearchTest
                                   ):
        if self.is_mock:
            raise SkipTest("F.T.S. not supported by mock")
        test_fields = ['category', 'name']
        initial = datetime.datetime.now()
        # verify fields works w/in kwargs
        x = self.try_n_times_decorator(self.cluster.search_query, 10, 10)("beer-search-index",
                                                                          search.TermQuery(
                                                                              "north"),
                                                                          fields=test_fields)  # type: SearchResult

        first_entry = x.rows()[0]
        self.assertNotEqual(first_entry.fields, {})
        res = list(map(lambda f: f in test_fields, first_entry.fields.keys()))
        self.assertTrue(all(res))
        SearchResultTest._check_search_result(self, initial, 1, x)

        # verify fields works w/in SearchOptions
        x = self.try_n_times_decorator(self.cluster.search_query, 10, 10)("beer-search-index",
                                                                          search.TermQuery(
                                                                              "north"),
                                                                          search.SearchOptions(fields=test_fields))  # type: SearchResult
        first_entry = x.rows()[0]
        self.assertNotEqual(first_entry.fields, {})
        res = list(map(lambda f: f in test_fields, first_entry.fields.keys()))
        self.assertTrue(all(res))

    def test_cluster_search_term_facets(self  # type: SearchTest
                                        ):
        if self.is_mock:
            raise SkipTest("F.T.S. not supported by mock")

        facet_name = 'beers'
        facet = search.TermFacet('category', 10)
        x = self.try_n_times_decorator(self.cluster.search_query, 10, 10)("beer-search-index",
                                                                          search.TermQuery(
                                                                              "north"),
                                                                          search.SearchOptions(facets={
                                                                              facet_name: facet
                                                                          }))  # type: SearchResult

        x.rows()
        result_facet = x.facets()[facet_name]
        self.assertIsInstance(result_facet, search.SearchFacetResult)
        self.assertEqual(facet_name, result_facet.name)
        self.assertEqual(facet.field, result_facet.field)
        self.assertGreaterEqual(facet.limit, len(result_facet.terms))

        self.assertRaises(couchbase.exceptions.SearchException, self.cluster.search_query,
                          "beer-search-index",
                          search.TermQuery("north"),
                          facets={'beers': None})

    def test_cluster_search_numeric_facets(self  # type: SearchTest
                                           ):
        if self.is_mock:
            raise SkipTest("F.T.S. not supported by mock")

        facet_name = 'abv'
        facet = search.NumericFacet('abv')
        facet.add_range('low', max=7)
        facet.add_range('med', min=7, max=10)
        facet.add_range('high', min=10)
        x = self.try_n_times_decorator(self.cluster.search_query, 10, 10)("beer-search-index",
                                                                          search.TermQuery(
                                                                              "north"),
                                                                          search.SearchOptions(facets={
                                                                              facet_name: facet
                                                                          }))  # type: SearchResult

        x.rows()
        result_facet = x.facets()[facet_name]
        self.assertIsInstance(result_facet, search.SearchFacetResult)
        self.assertEqual(facet_name, result_facet.name)
        self.assertEqual(facet.field, result_facet.field)
        # if a limit is not provided, only the top-level facet results are
        # provided
        self.assertEqual(0, len(result_facet.numeric_ranges))

        # try again but verify the limit is applied (i.e. limit <
        # len(numeric_ranges))
        facet.limit = 2
        x = self.try_n_times_decorator(self.cluster.search_query, 10, 10)("beer-search-index",
                                                                          search.TermQuery(
                                                                              "north"),
                                                                          search.SearchOptions(facets={
                                                                              facet_name: facet
                                                                          }))  # type: SearchResult

        x.rows()
        result_facet = x.facets()[facet_name]
        self.assertIsInstance(result_facet, search.SearchFacetResult)
        self.assertEqual(facet_name, result_facet.name)
        self.assertEqual(facet.field, result_facet.field)
        self.assertGreaterEqual(facet.limit, len(result_facet.numeric_ranges))
        self.assertEqual(facet.limit, len(result_facet.numeric_ranges))
        self.assertRaises(couchbase.exceptions.SearchException, self.cluster.search_query,
                          "beer-search-index",
                          search.TermQuery("north"),
                          facets={'abv': search.NumericFacet('abv', 10)})

    def test_cluster_search_date_facets(self  # type: SearchTest
                                        ):
        if self.is_mock:
            raise SkipTest("F.T.S. not supported by mock")

        facet_name = 'updated'
        facet = search.DateFacet('updated')
        facet.add_range('early', end='2010-12-01T00:00:00Z')
        facet.add_range('mid', start='2010-12-01T00:00:00Z',
                        end='2011-01-01T00:00:00Z')
        facet.add_range('late', start='2011-01-01T00:00:00Z')
        x = self.try_n_times_decorator(self.cluster.search_query, 10, 10)("beer-search-index",
                                                                          search.TermQuery(
                                                                              "north"),
                                                                          search.SearchOptions(facets={
                                                                              facet_name: facet
                                                                          }))  # type: SearchResult

        x.rows()
        result_facet = x.facets()[facet_name]
        self.assertIsInstance(result_facet, search.SearchFacetResult)
        self.assertEqual(facet_name, result_facet.name)
        self.assertEqual(facet.field, result_facet.field)
        # if a limit is not provided, only the top-level facet results are
        # provided
        self.assertEqual(0, len(result_facet.date_ranges))

        # try again but verify the limit is applied (i.e. limit <
        # len(date_ranges))
        facet.limit = 2
        x = self.try_n_times_decorator(self.cluster.search_query, 10, 10)("beer-search-index",
                                                                          search.TermQuery(
                                                                              "north"),
                                                                          search.SearchOptions(facets={
                                                                              facet_name: facet
                                                                          }))  # type: SearchResult

        x.rows()
        result_facet = x.facets()[facet_name]
        self.assertIsInstance(result_facet, search.SearchFacetResult)
        self.assertEqual(facet_name, result_facet.name)
        self.assertEqual(facet.field, result_facet.field)
        self.assertEqual(facet.limit, len(result_facet.date_ranges))

        self.assertRaises(couchbase.exceptions.SearchException, self.cluster.search_query,
                          "beer-search-index",
                          search.TermQuery("north"),
                          facets={'abv': search.DateFacet('abv', 10)})

    def test_cluster_search_disable_scoring(self  # type: SearchTest
                                            ):
        if self.is_mock:
            raise SkipTest("F.T.S. not supported by mock")

        if float(self.cluster_version[0:3]) < 6.5:
            raise SkipTest(
                "Disable scoring not available on server version < 6.5")

        # verify disable scoring works w/in SearchOptions
        x = self.try_n_times_decorator(self.cluster.search_query, 10, 10)("beer-search-index",
                                                                          search.TermQuery(
                                                                              "north"),
                                                                          search.SearchOptions(limit=10,
                                                                                               disable_scoring=True))  # type: SearchResult
        rows = x.rows()
        res = list(map(lambda r: r.score == 0, rows))
        self.assertTrue(all(res))

        # verify disable scoring works w/in kwargs
        x = self.try_n_times_decorator(self.cluster.search_query, 10, 10)("beer-search-index",
                                                                          search.TermQuery(
                                                                              "north"),
                                                                          search.SearchOptions(
                                                                              limit=10),
                                                                          disable_scoring=True)  # type: SearchResult
        rows = x.rows()
        res = list(map(lambda r: r.score == 0, rows))
        self.assertTrue(all(res))

        x = self.try_n_times_decorator(self.cluster.search_query, 10, 10)("beer-search-index",
                                                                          search.TermQuery(
                                                                              "north"),
                                                                          search.SearchOptions(limit=10,
                                                                                               disable_scoring=False))  # type: SearchResult

        rows = x.rows()
        res = list(map(lambda r: r.score != 0, rows))
        self.assertTrue(all(res))

        x = self.try_n_times_decorator(self.cluster.search_query, 10, 10)("beer-search-index",
                                                                          search.TermQuery(
                                                                              "north"),
                                                                          search.SearchOptions(limit=10))  # type: SearchResult

        rows = x.rows()
        res = list(map(lambda r: r.score != 0, rows))
        self.assertTrue(all(res))

    def test_cluster_search_highlight(self  # type: SearchTest
                                      ):
        if self.is_mock:
            raise SkipTest("F.T.S. not supported by mock")

        initial = datetime.datetime.now()
        # verify locations/fragments works w/in SearchOptions
        x = self.try_n_times_decorator(self.cluster.search_query, 10, 10)("beer-search-index",
                                                                          search.TermQuery(
                                                                              "north"),
                                                                          search.SearchOptions(highlight_style=search.HighlightStyle.Html, limit=10))  # type: SearchResult

        rows = x.rows()
        self.assertGreaterEqual(10, len(rows))
        locations = rows[0].locations
        fragments = rows[0].fragments
        self.assertIsInstance(fragments, dict)
        res = list(map(lambda l: isinstance(
            l, search.SearchRowLocation), locations.get_all()))
        self.assertTrue(all(res))
        self.assertIsInstance(locations, search.SearchRowLocations)
        SearchResultTest._check_search_result(self, initial, 1, x)

        initial = datetime.datetime.now()
        # verify locations/fragments works w/in kwargs
        x = self.try_n_times_decorator(self.cluster.search_query, 10, 10)("beer-search-index",
                                                                          search.TermQuery(
                                                                              "north"),
                                                                          search.SearchOptions(
                                                                              limit=10),
                                                                          highlight_style='html')  # type: SearchResult

        rows = x.rows()
        self.assertGreaterEqual(10, len(rows))
        locations = rows[0].locations
        fragments = rows[0].fragments
        self.assertIsInstance(fragments, dict)
        res = list(map(lambda l: isinstance(
            l, search.SearchRowLocation), locations.get_all()))
        self.assertTrue(all(res))
        self.assertIsInstance(locations, search.SearchRowLocations)
        SearchResultTest._check_search_result(self, initial, 1, x)

    def test_cluster_search_scan_consistency(self  # type: SearchTest
                                             ):
        if self.is_mock:
            raise SkipTest("F.T.S. not supported by mock")

        initial = datetime.datetime.now()
        # verify scan consistency works w/in SearchOptions
        x = self.try_n_times_decorator(self.cluster.search_query, 2, 1)("beer-search-index",
                                                                        search.TermQuery(
                                                                            "north"),
                                                                        search.SearchOptions(scan_consistency=search.SearchScanConsistency.NOT_BOUNDED))  # type: SearchResult

        rows = x.rows()
        self.assertGreaterEqual(10, len(rows))
        SearchResultTest._check_search_result(self, initial, 1, x)

        initial = datetime.datetime.now()
        # verify scan consistency works w/in SearchOptions
        x = self.try_n_times_decorator(self.cluster.search_query, 2, 1)("beer-search-index",
                                                                        search.TermQuery(
                                                                            "north"),
                                                                        search.SearchOptions(scan_consistency=search.SearchScanConsistency.AT_PLUS))  # type: SearchResult

        rows = x.rows()
        self.assertGreaterEqual(10, len(rows))
        SearchResultTest._check_search_result(self, initial, 1, x)

    def test_cluster_sort_str(self  # type: SearchTest
                              ):
        if self.is_mock:
            raise SkipTest("F.T.S. not supported by mock")
        # score - ascending
        x = self.try_n_times_decorator(self.cluster.search_query, 10, 10)("beer-search-index",
                                                                          search.TermQuery(
                                                                              "north"),
                                                                          search.SearchOptions(sort=["_score"]))  # type: SearchResult

        rows = x.rows()
        score = rows[0].score
        for row in rows[1:]:
            self.assertGreaterEqual(row.score, score)
            score = row.score
        # score - descending
        x = self.try_n_times_decorator(self.cluster.search_query, 10, 10)("beer-search-index",
                                                                          search.TermQuery(
                                                                              "north"),
                                                                          search.SearchOptions(sort=["-_score"]))  # type: SearchResult

        rows = x.rows()
        score = rows[0].score
        for row in rows[1:]:
            self.assertGreaterEqual(score, row.score)
            score = row.score

    def test_cluster_sort_score(self  # type: SearchTest
                                ):
        if self.is_mock:
            raise SkipTest("F.T.S. not supported by mock")
        # score - ascending
        x = self.try_n_times_decorator(self.cluster.search_query, 10, 10)("beer-search-index",
                                                                          search.TermQuery(
                                                                              "north"),
                                                                          search.SearchOptions(sort=[search.SortScore()]))  # type: SearchResult

        rows = x.rows()
        score = rows[0].score
        for row in rows[1:]:
            self.assertGreaterEqual(row.score, score)
            score = row.score
        # score - descending
        x = self.try_n_times_decorator(self.cluster.search_query, 10, 10)("beer-search-index",
                                                                          search.TermQuery(
                                                                              "north"),
                                                                          search.SearchOptions(sort=[search.SortScore(desc=True)]))  # type: SearchResult

        rows = x.rows()
        score = rows[0].score
        for row in rows[1:]:
            self.assertGreaterEqual(score, row.score)
            score = row.score

    def test_cluster_sort_id(self  # type: SearchTest
                             ):
        if self.is_mock:
            raise SkipTest("F.T.S. not supported by mock")
        # id - ascending
        x = self.try_n_times_decorator(self.cluster.search_query, 10, 10)("beer-search-index",
                                                                          search.TermQuery(
                                                                              "north"),
                                                                          search.SearchOptions(sort=[search.SortID()]))  # type: SearchResult

        rows = x.rows()
        id = rows[0].id
        for row in rows[1:]:
            self.assertGreaterEqual(row.id, id)
            id = row.id
        # id - descending
        x = self.try_n_times_decorator(self.cluster.search_query, 10, 10)("beer-search-index",
                                                                          search.TermQuery(
                                                                              "north"),
                                                                          search.SearchOptions(sort=[search.SortID(desc=True)]))  # type: SearchResult

        rows = x.rows()
        id = rows[0].id
        for row in rows[1:]:
            self.assertGreaterEqual(id, row.id)
            id = row.id

    def test_cluster_sort_field(self  # type: SearchTest
                                ):
        if self.is_mock:
            raise SkipTest("F.T.S. not supported by mock")
        sort_field = "abv"
        # field - ascending
        x = self.try_n_times_decorator(self.cluster.search_query, 10, 10)("beer-search-index",
                                                                          search.TermQuery(
                                                                              "north"),
                                                                          search.SearchOptions(sort=[search.SortField(
                                                                              field=sort_field, type="number", mode="min", missing="last")]),
                                                                          fields=[sort_field])  # type: SearchResult

        rows = x.rows()
        self.assertGreaterEqual(10, len(rows))
        abv = rows[0].fields[sort_field]
        for row in rows[1:]:
            self.assertGreaterEqual(row.fields[sort_field], abv)
            abv = row.fields[sort_field]
        # field - descending
        x = self.try_n_times_decorator(self.cluster.search_query, 10, 10)("beer-search-index",
                                                                          search.TermQuery(
                                                                              "north"),
                                                                          search.SearchOptions(sort=[search.SortField(
                                                                              field=sort_field, type="number", missing="last", desc=True)]),
                                                                          fields=[sort_field])  # type: SearchResult

        rows = x.rows()
        self.assertGreaterEqual(10, len(rows))
        abv = rows[0].fields[sort_field]
        for row in rows[1:]:
            self.assertGreaterEqual(abv, row.fields[sort_field])
            abv = row.fields[sort_field]

    def test_cluster_sort_geo(self  # type: SearchTest
                              ):
        if self.is_mock:
            raise SkipTest("F.T.S. not supported by mock")
        # TODO:  better confirmation on results?
        sort_field = "geo"
        # geo - ascending
        x = self.try_n_times_decorator(self.cluster.search_query, 10, 10)("beer-search-index",
                                                                          search.TermQuery(
                                                                              "north"),
                                                                          search.SearchOptions(sort=[search.SortGeoDistance(
                                                                              field=sort_field, location=(37.7749, 122.4194), unit="meters")]),
                                                                          fields=[sort_field])  # type: SearchResult

        rows = x.rows()
        self.assertGreaterEqual(10, len(rows))
        # geo - descending
        x = self.try_n_times_decorator(self.cluster.search_query, 10, 10)("beer-search-index",
                                                                          search.TermQuery(
                                                                              "north"),
                                                                          search.SearchOptions(sort=[search.SortGeoDistance(
                                                                              field=sort_field, location=(37.7749, 122.4194), unit="meters", desc=True)]),
                                                                          fields=[sort_field])  # type: SearchResult

        rows = x.rows()
        self.assertGreaterEqual(10, len(rows))

    def test_cluster_sort_field_multi(self  # type: SearchTest
                                      ):
        if self.is_mock:
            raise SkipTest("F.T.S. not supported by mock")
        sort_fields = [
            search.SortField(field="abv", type="number",
                             mode="min", missing="last"),
            search.SortField(field="updated", type="number",
                             mode="min", missing="last"),
            search.SortScore(),
        ]
        sort_field_names = ["abv", "updated"]

        x = self.try_n_times_decorator(self.cluster.search_query, 10, 10)("beer-search-index",
                                                                          search.TermQuery(
                                                                              "north"),
                                                                          search.SearchOptions(
                                                                              sort=sort_fields),
                                                                          fields=sort_field_names)  # type: SearchResult

        rows = x.rows()
        self.assertGreaterEqual(10, len(rows))
        sort_fields = [
            search.SortField(field="abv", type="number",
                             mode="min", missing="last", desc=True),
            search.SortField(field="updated", type="number",
                             mode="min", missing="last"),
            search.SortScore(desc=True),
        ]

        x = self.try_n_times_decorator(self.cluster.search_query, 10, 10)("beer-search-index",
                                                                          search.TermQuery(
                                                                              "north"),
                                                                          search.SearchOptions(
                                                                              sort=sort_fields),
                                                                          fields=sort_field_names)  # type: SearchResult

        rows = x.rows()
        self.assertGreaterEqual(10, len(rows))

        x = self.try_n_times_decorator(self.cluster.search_query, 10, 10)("beer-search-index",
                                                                          search.TermQuery(
                                                                              "north"),
                                                                          search.SearchOptions(sort=["abv", "udpated", "-_score"]))  # type: SearchResult

        rows = x.rows()
        self.assertGreaterEqual(10, len(rows))

    def test_search_raw_query(self):
        initial = datetime.datetime.now()
        query_args = {"match": "north south",
                      "fuzziness": 2, "operator": "and"}
        x = self.try_n_times_decorator(self.cluster.search_query, 10, 10)("beer-search-index",
                                                                          search.RawQuery(
                                                                              query_args),
                                                                          search.SearchOptions(limit=10))  # type: SearchResult
        SearchResultTest._check_search_result(self, initial, 1, x)

    def test_search_no_include_locations(self  # type: SearchTest
                                         ):
        if self.is_mock:
            raise SkipTest("F.T.S. not supported by mock")

        x = self.try_n_times_decorator(self.cluster.search_query, 10, 10)("beer-search-index",
                                                                          search.TermQuery(
                                                                              "north"),
                                                                          search.SearchOptions(limit=10))  # type: SearchResult

        rows = x.rows()
        locations = rows[0].locations
        all_locations = locations.get_all()
        self.assertEqual(0, len(all_locations))
        self.assertIsInstance(locations, search.SearchRowLocations)

        x = self.try_n_times_decorator(self.cluster.search_query, 10, 10)("beer-search-index",
                                                                          search.TermQuery(
                                                                              "north"),
                                                                          search.SearchOptions(include_locations=False, limit=10))  # type: SearchResult

        rows = x.rows()
        locations = rows[0].locations
        all_locations = locations.get_all()
        self.assertEqual(0, len(all_locations))
        self.assertIsInstance(locations, search.SearchRowLocations)

    def test_search_include_locations(self  # type: SearchTest
                                      ):
        if self.is_mock:
            raise SkipTest("F.T.S. not supported by mock")

        x = self.try_n_times_decorator(self.cluster.search_query, 10, 10)("beer-search-index",
                                                                          search.TermQuery(
                                                                              "north"),
                                                                          search.SearchOptions(include_locations=True, limit=10))  # type: SearchResult

        rows = x.rows()
        locations = rows[0].locations
        all_locations = locations.get_all()
        self.assertNotEqual(0, len(all_locations))
        res = list(map(lambda l: isinstance(
            l, search.SearchRowLocation), all_locations))
        self.assertTrue(all(res))
        self.assertIsInstance(locations, search.SearchRowLocations)

    def test_search_match_operator(self  # type: SearchTest
                                   ):
        if self.is_mock:
            raise SkipTest("F.T.S. not supported by mock")

        random_query_term = "".join(random.choice(string.ascii_letters)
                            for _ in range(10))

        # (operator, query, expect_rows)
        cases = [(search.MatchOperator.AND, "north south", True), (search.MatchOperator.AND, "north {}".format(random_query_term), False),
                 (search.MatchOperator.OR, "north south", True), (search.MatchOperator.OR, "north {}".format(random_query_term), True)]

        for (operator, query, expect_rows) in cases:
            x = self.try_n_times_decorator(self.cluster.search_query, 10, 10)("beer-search-index",
                                                                              search.MatchQuery(
                                                                                  query, match_operator=operator),
                                                                              search.SearchOptions(limit=10))  # type: SearchResult

            rows = x.rows()

            if expect_rows:
                self.assertNotEqual(0, len(rows))
            else:
                self.assertEqual(0, len(rows))

    def test_search_match_operator_fail(self  # type: SearchTest
                                        ):
        if self.is_mock:
            raise SkipTest("F.T.S. not supported by mock")

        with self.assertRaises(ValueError):
            self.try_n_times_decorator(self.cluster.search_query, 10, 10)("beer-search-index",
                                                                          search.MatchQuery(
                                                                              "north south", match_operator="NOT"),
                                                                          search.SearchOptions(limit=10))  # type: SearchResult


class SearchStringsTest(CouchbaseTestCase):
    def test_fuzzy(self):
        q = search.TermQuery('someterm', field='field', boost=1.5,
                             prefix_length=23, fuzziness=12)
        p = search.SearchOptions(explain=True)

        exp_json = {
            'query': {
                'term': 'someterm',
                'boost': 1.5,
                'fuzziness': 12,
                'prefix_length': 23,
                'field': 'field'
            },
            'indexName': 'someIndex',
            'explain': True
        }

        self.assertEqual(exp_json, p._gen_search_params('someIndex', q).body)

    def test_match_phrase(self):
        exp_json = {
            'query': {
                'match_phrase': 'salty beers',
                'analyzer': 'analyzer',
                'boost': 1.5,
                'field': 'field'
            },
            'size': 10,
            'indexName': 'ix'
        }

        p = search.SearchOptions(limit=10)
        q = search.MatchPhraseQuery('salty beers', boost=1.5, analyzer='analyzer',
                                    field='field')
        self.assertEqual(exp_json, p._gen_search_params('ix', q).body)

    def test_match_query(self):
        exp_json = {
            'query': {
                'match': 'salty beers',
                'analyzer': 'analyzer',
                'boost': 1.5,
                'field': 'field',
                'fuzziness': 1234,
                'prefix_length': 4,
                'operator': 'or'
            },
            'size': 10,
            'indexName': 'ix'
        }

        q = search.MatchQuery('salty beers', boost=1.5, analyzer='analyzer',
                              field='field', fuzziness=1234, prefix_length=4, match_operator=MatchOperator.OR)
        p = search.SearchOptions(limit=10)
        self.assertEqual(exp_json, p._gen_search_params('ix', q).body)

        exp_json["query"]["operator"] = "and"

        q = search.MatchQuery('salty beers', boost=1.5, analyzer='analyzer',
                              field='field', fuzziness=1234, prefix_length=4, match_operator=MatchOperator.AND)
        p = search.SearchOptions(limit=10)
        self.assertEqual(exp_json, p._gen_search_params('ix', q).body)

    def test_string_query(self):
        exp_json = {
            'query': {
                'query': 'q*ry',
                'boost': 2.0,
            },
            'explain': True,
            'size': 10,
            'indexName': 'ix'
        }
        q = search.QueryStringQuery('q*ry', boost=2.0)
        p = search.SearchOptions(limit=10, explain=True)
        self.assertEqual(exp_json, p._gen_search_params('ix', q).body)

    def test_params(self):
        self.assertEqual({}, SearchOptions().as_encodable('ix'))
        self.assertEqual({'size': 10}, SearchOptions(
            limit=10).as_encodable('ix'))
        self.assertEqual({'from': 100},
                         SearchOptions(skip=100).as_encodable('ix'))

        self.assertEqual({'explain': True},
                         SearchOptions(explain=True).as_encodable('ix'))

        self.assertEqual({'highlight': {'style': 'html'}},
                         SearchOptions(highlight_style=search.HighlightStyle.Html).as_encodable('ix'))

        self.assertEqual({'highlight': {'style': 'ansi',
                                        'fields': ['foo', 'bar', 'baz']}},
                         SearchOptions(highlight_style=search.HighlightStyle.Ansi,
                                       highlight_fields=['foo', 'bar', 'baz'])
                         .as_encodable('ix'))

        self.assertEqual({'fields': ['foo', 'bar', 'baz']},
                         SearchOptions(fields=['foo', 'bar', 'baz']
                                       ).as_encodable('ix'))

        self.assertEqual({'sort': ['f1', 'f2', '-_score']},
                         SearchOptions(sort=['f1', 'f2', '-_score']
                                       ).as_encodable('ix'))

        self.assertEqual({'sort': ['f1', 'f2', '-_score']},
                         SearchOptions(sort=[
                             'f1', 'f2', '-_score']).as_encodable('ix'))

        self.assertEqual({'includeLocations': True},
                         SearchOptions(include_locations=True).as_encodable('ix'))

        p = SearchOptions(facets={
            'term': search.TermFacet('somefield', limit=10),
            'dr': search.DateFacet('datefield').add_range('name', 'start', 'end'),
            'nr': search.NumericFacet('numfield').add_range('name2', 0.0, 99.99)
        })
        exp = {
            'facets': {
                'term': {
                    'field': 'somefield',
                    'size': 10
                },
                'dr': {
                    'field': 'datefield',
                    'date_ranges': [{
                        'name': 'name',
                        'start': 'start',
                        'end': 'end'
                    }]
                },
                'nr': {
                    'field': 'numfield',
                    'numeric_ranges': [{
                        'name': 'name2',
                        'min': 0.0,
                        'max': 99.99
                    }]
                },
            }
        }
        self.assertEqual(exp, p.as_encodable('ix'))
        self.assertEqual({'ctl': {'consistency': {'level': ''}}},
                         SearchOptions(scan_consistency=search.SearchScanConsistency.NOT_BOUNDED.value).as_encodable('ix'))

    def test_facets(self):
        s = SearchOptions()
        f = search.NumericFacet('numfield')
        p = s._gen_params()
        self.assertRaises(ValueError, p.facets.__setitem__, 'facetName', f)
        self.assertRaises(TypeError, f.add_range, 'range1')

        p.facets['facetName'] = f.add_range('range1', min=123, max=321)
        self.assertTrue('facetName' in p.facets)

        f = search.DateFacet('datefield')
        f.add_range('r1', start='2012', end='2013')
        f.add_range('r2', start='2014')
        f.add_range('r3', end='2015')
        exp = {
            'field': 'datefield',
            'date_ranges': [
                {'name': 'r1', 'start': '2012', 'end': '2013'},
                {'name': 'r2', 'start': '2014'},
                {'name': 'r3', 'end': '2015'}
            ]
        }
        self.assertEqual(exp, f.encodable)

        f = search.TermFacet('termfield')
        self.assertEqual({'field': 'termfield'}, f.encodable)
        f.limit = 10
        self.assertEqual({'field': 'termfield', 'size': 10}, f.encodable)

    def test_raw_query(self):
        qq = search.RawQuery({'foo': 'bar'})
        self.assertEqual({'foo': 'bar'}, qq.encodable)

    def test_wildcard_query(self):
        qq = search.WildcardQuery('f*o', field='wc')
        self.assertEqual({'wildcard': 'f*o', 'field': 'wc'}, qq.encodable)

    def test_docid_query(self):
        qq = search.DocIdQuery([])
        self.assertRaises(search.NoChildrenException, getattr, qq, 'encodable')
        qq.ids = ['foo', 'bar', 'baz']
        self.assertEqual({'ids': ['foo', 'bar', 'baz']}, qq.encodable)

    def test_boolean_query(self):
        prefix_q = search.PrefixQuery('someterm', boost=2)
        bool_q = search.BooleanQuery(
            must=prefix_q, must_not=prefix_q, should=prefix_q)
        exp = {'prefix': 'someterm', 'boost': 2.0}
        self.assertEqual({'conjuncts': [exp]},
                         bool_q.must.encodable)
        self.assertEqual({'min': 1, 'disjuncts': [exp]},
                         bool_q.should.encodable)
        self.assertEqual({'min': 1, 'disjuncts': [exp]},
                         bool_q.must_not.encodable)

        # Test multiple criteria in must and must_not
        pq_1 = search.PrefixQuery('someterm', boost=2)
        pq_2 = search.PrefixQuery('otherterm')
        bool_q = search.BooleanQuery(must=[pq_1, pq_2])
        exp = {
            'conjuncts': [
                {'prefix': 'someterm', 'boost': 2.0},
                {'prefix': 'otherterm'}
            ]
        }
        self.assertEqual({'must': exp}, bool_q.encodable)

    def test_daterange_query(self):
        self.assertRaises(TypeError, search.DateRangeQuery)
        dr = search.DateRangeQuery(end='theEnd')
        self.assertEqual({'end': 'theEnd'}, dr.encodable)
        dr = search.DateRangeQuery(start='theStart')
        self.assertEqual({'start': 'theStart'}, dr.encodable)
        dr = search.DateRangeQuery(start='theStart', end='theEnd')
        self.assertEqual({'start': 'theStart', 'end': 'theEnd'}, dr.encodable)
        dr = search.DateRangeQuery('', '')  # Empty strings should be ok
        self.assertEqual({'start': '', 'end': ''}, dr.encodable)

    def test_numrange_query(self):
        self.assertRaises(TypeError, search.NumericRangeQuery)
        nr = search.NumericRangeQuery(0, 0)  # Should be OK
        self.assertEqual({'min': 0, 'max': 0}, nr.encodable)
        nr = search.NumericRangeQuery(0.1, 0.9)
        self.assertEqual({'min': 0.1, 'max': 0.9}, nr.encodable)
        nr = search.NumericRangeQuery(max=0.9)
        self.assertEqual({'max': 0.9}, nr.encodable)
        nr = search.NumericRangeQuery(min=0.1)
        self.assertEqual({'min': 0.1}, nr.encodable)

    def test_disjunction_query(self):
        dq = search.DisjunctionQuery()
        self.assertEqual(1, dq.min)
        self.assertRaises(search.NoChildrenException, getattr, dq, 'encodable')

        dq.disjuncts.append(search.PrefixQuery('somePrefix'))
        self.assertEqual({'min': 1, 'disjuncts': [{'prefix': 'somePrefix'}]},
                         dq.encodable)
        self.assertRaises(ValueError, setattr, dq, 'min', 0)
        dq.min = 2
        self.assertRaises(search.NoChildrenException, getattr, dq, 'encodable')

    def test_conjunction_query(self):
        cq = search.ConjunctionQuery()
        self.assertRaises(search.NoChildrenException, getattr, cq, 'encodable')
        cq.conjuncts.append(search.PrefixQuery('somePrefix'))
        self.assertEqual({'conjuncts': [{'prefix': 'somePrefix'}]},
                         cq.encodable)

    def test_match_all_none_queries(self):
        self.assertEqual({'match_all': None}, search.MatchAllQuery().encodable)
        self.assertEqual({'match_none': None},
                         search.MatchNoneQuery().encodable)

    def test_phrase_query(self):
        pq = search.PhraseQuery('salty', 'beers')
        self.assertEqual({'terms': ['salty', 'beers']}, pq.encodable)

        pq = search.PhraseQuery()
        self.assertRaises(search.NoChildrenException, getattr, pq, 'encodable')
        pq.terms.append('salty')
        self.assertEqual({'terms': ['salty']}, pq.encodable)

    def test_prefix_query(self):
        pq = search.PrefixQuery('someterm', boost=1.5)
        self.assertEqual({'prefix': 'someterm', 'boost': 1.5}, pq.encodable)

    def test_regexp_query(self):
        pq = search.RegexQuery('some?regex')
        self.assertEqual({'regexp': 'some?regex'}, pq.encodable)

    def test_booleanfield_query(self):
        bq = search.BooleanFieldQuery(True)
        self.assertEqual({'bool': True}, bq.encodable)

    def test_consistency(self):
        uuid = str('10000')
        vb = 42
        seq = 101
        ixname = 'ix'

        mutinfo = (vb, uuid, seq, 'dummy-bucket-name')
        ms = MutationState()
        ms._add_scanvec(mutinfo)

        params = search.SearchOptions(consistent_with=ms)
        got = params._gen_search_params('ix', search.MatchNoneQuery()).body
        exp = {
            'indexName': ixname,
            'query': {
                'match_none': None
            },
            'ctl': {
                'consistency': {
                    'level': 'at_plus',
                    'vectors': {
                        ixname: {
                            '{0}/{1}'.format(vb, uuid): seq
                        }
                    }
                }
            }
        }
        self.assertEqual(exp, got)

    def test_advanced_sort(self):
        self.assertEqual({'by': 'score'}, search.SortScore().as_encodable())
        # test legacy 'descending' support
        self.assertEqual({'by': 'score', 'desc': False},
                         search.SortScore(descending=False).as_encodable())
        # official RFC format
        self.assertEqual({'by': 'score', 'desc': False},
                         search.SortScore(desc=False).as_encodable())
        self.assertEqual({'by': 'id'}, search.SortID().as_encodable())

        self.assertEqual({'by': 'field', 'field': 'foo'},
                         search.SortField('foo').as_encodable())
        self.assertEqual({'by': 'field', 'field': 'foo', 'type': 'int'},
                         search.SortField('foo', type='int').as_encodable())


class SearchCollectionTests(CollectionTestCase):

    def setUp(self):
        super(SearchCollectionTests, self).setUp(bucket='beer-sample')

        if self.is_mock:
            raise SkipTest("Search not available on Mock")

        # SkipTest if collections not supported
        try:
            self.bucket.collections().get_all_scopes()
        except NotSupportedException:
            raise SkipTest('Cluster does not support collections')

        self.cm = self.bucket.collections()
        self.create_beer_sample_collections()
        self.sm = self.cluster.search_indexes()

        with open(os.path.join(search_testcases, "beer-search-coll-index-params.json")) as params_file:
            input = params_file.read()
            params_json = json.loads(input)
            try:
                self.sm.get_index('beer-search-coll-index')
                # total of 3 minutes
                self._check_indexed_docs(retries=18, delay=10)
            except Exception:
                self.sm.upsert_index(
                    SearchIndex(name="beer-search-coll-index",
                                idx_type="fulltext-index",
                                source_name="beer-sample",
                                source_type="couchbase",
                                params=params_json)
                )
                # make sure the index loads, for some reason over time
                # loading the index becomes SLOW, hence the 30 second sleep
                self._check_indexed_docs()

    def _check_indexed_docs(self, retries=20, delay=30, num_docs=3000, idx="beer-search-coll-index"):
        for _ in range(retries):
            indexed_docs = self.try_n_times(
                10, 10, self.sm.get_indexed_documents_count, idx)
            if indexed_docs >= num_docs:
                break
            print('Found {} indexed docs, waiting a bit...'.format(
                indexed_docs))
            time.sleep(delay)

    @classmethod
    def setUpClass(cls) -> None:
        super(SearchCollectionTests, cls).setUpClass(True)

    @classmethod
    def tearDownClass(cls) -> None:
        if cls._beer_sample_collections:
            im = cls._cluster_resource.cluster.search_indexes()
            im.drop_index("beer-search-coll-index")
        super(SearchCollectionTests, cls).tearDownClass()

    def test_cluster_query_collections(self):
        initial = datetime.datetime.now()
        scope = self.bucket.scope(self.beer_sample_collections.scope)
        x = self.try_n_times_decorator(scope.search_query, 10, 10)("beer-search-coll-index",
                                                                   search.TermQuery(
                                                                       "north"),
                                                                   search.SearchOptions(limit=10,
                                                                                        collections=['breweries']))  # type: SearchResult

        rows = x.rows()
        collections = list(map(lambda r: r.fields['_$c'], rows))
        self.assertTrue(all([c for c in collections if c == 'breweries']))
        SearchResultTest._check_search_result(self, initial, 1, x)

    def test_scope_query(self):
        initial = datetime.datetime.now()
        scope = self.bucket.scope(self.beer_sample_collections.scope)
        x = self.try_n_times_decorator(scope.search_query, 10, 10)("beer-search-coll-index",
                                                                   search.TermQuery(
                                                                       "north"),
                                                                   search.SearchOptions(limit=10))  # type: SearchResult
        rows = x.rows()
        collections = list(map(lambda r: r.fields['_$c'], rows))
        self.assertTrue(
            all([c for c in collections if c in ["beers", "breweries"]]))
        SearchResultTest._check_search_result(self, initial, 1, x)

        initial = datetime.datetime.now()
        x = self.try_n_times_decorator(scope.search_query, 10, 10)("beer-search-coll-index",
                                                                   search.TermQuery(
                                                                       "north"),
                                                                   search.SearchOptions(limit=10,
                                                                                        collections=['breweries']))  # type: SearchResult

        rows = x.rows()
        collections = list(map(lambda r: r.fields['_$c'], rows))
        self.assertTrue(all([c for c in collections if c == 'breweries']))
        SearchResultTest._check_search_result(self, initial, 1, x)

    def test_scope_search_fields(self):
        scope = self.bucket.scope(self.beer_sample_collections.scope)
        test_fields = ['category', 'name']
        initial = datetime.datetime.now()
        # verify fields works w/in kwargs
        x = self.try_n_times_decorator(scope.search_query, 10, 10)("beer-search-coll-index",
                                                                   search.TermQuery(
                                                                       "north"),
                                                                   fields=test_fields,
                                                                   collections=['beers'])  # type: SearchResult

        rows = x.rows()
        collections = list(map(lambda r: r.fields['_$c'], rows))
        self.assertTrue(all([c for c in collections if c == 'beers']))
        first_entry = rows[0]
        self.assertNotEqual(first_entry.fields, {})
        # add the collection key to returned fields
        test_fields.append('_$c')
        res = list(map(lambda f: f in test_fields, first_entry.fields.keys()))
        self.assertTrue(all(res))
        SearchResultTest._check_search_result(self, initial, 1, x)

    def test_cluster_search_highlight(self):

        scope = self.bucket.scope(self.beer_sample_collections.scope)
        initial = datetime.datetime.now()
        # verify locations/fragments works w/in SearchOptions
        x = self.try_n_times_decorator(scope.search_query, 10, 10)("beer-search-coll-index",
                                                                   search.TermQuery(
                                                                       "north"),
                                                                   search.SearchOptions(highlight_style=search.HighlightStyle.Html,
                                                                                        limit=10,
                                                                                        collections=['beers']))  # type: SearchResult

        rows = x.rows()
        collections = list(map(lambda r: r.fields['_$c'], rows))
        self.assertTrue(all([c for c in collections if c == 'beers']))
        self.assertGreaterEqual(10, len(rows))
        locations = rows[0].locations
        fragments = rows[0].fragments
        self.assertIsInstance(fragments, dict)
        res = list(map(lambda l: isinstance(
            l, search.SearchRowLocation), locations.get_all()))
        self.assertTrue(all(res))
        self.assertIsInstance(locations, search.SearchRowLocations)
        SearchResultTest._check_search_result(self, initial, 1, x)

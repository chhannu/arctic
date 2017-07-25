from datetime import datetime as dt
import pandas as pd
from pandas.util.testing import assert_frame_equal
import pytest

from arctic.exceptions import NoDataFoundException

symbol1 = 'symbol1'
symbol2 = 'symbol2'
start_time1 = dt(2001, 1, 1)
start_time2 = dt(2001, 4, 1)
metadata1 = {'key1': 'value1'}
metadata2 = {'key2': 'value2'}
dataframe1 = pd.DataFrame({'metadata': [metadata1]}, [start_time1])
dataframe2 = pd.DataFrame({'metadata': [metadata1, metadata2]}, [start_time1, start_time2])


def test_has_symbol(ms_lib):
    assert not ms_lib.has_symbol(symbol1)
    ms_lib.write_metadata(symbol1, metadata1)
    assert ms_lib.has_symbol(symbol1)


def test_list_symbols(ms_lib):
    ms_lib.write_metadata(symbol1, metadata1)
    assert symbol1 in ms_lib.list_symbols()


def test_read_metadata(ms_lib):
    assert ms_lib.read_metadata(symbol1) == None

    ms_lib.write_metadata(symbol1, metadata1, start_time1)
    assert ms_lib.read_metadata(symbol1) == metadata1
    assert_frame_equal(ms_lib.read_metadata(symbol1, history=True), dataframe1)


def test_write_metadata(ms_lib):
    ms_lib.write_metadata(symbol1, None)
    assert not ms_lib.has_symbol(symbol1)

    ms_lib.write_metadata(symbol1, metadata1, start_time1)
    assert ms_lib.read_metadata(symbol1) == metadata1

    ms_lib.write_metadata(symbol1, metadata1, start_time2)
    assert_frame_equal(ms_lib.read_metadata(symbol1, history=True), dataframe1)

    ms_lib.write_metadata(symbol1, metadata2, start_time2)
    assert_frame_equal(ms_lib.read_metadata(symbol1, history=True), dataframe2)


def test_write_metadata_history(ms_lib):
    collection = {symbol1: ([metadata1], [start_time1]), symbol2: ([metadata1, metadata2], [start_time1, start_time2])}
    ms_lib.write_metadata_history(collection)

    assert_frame_equal(ms_lib.read_metadata(symbol1, history=True), dataframe1)
    assert_frame_equal(ms_lib.read_metadata(symbol2, history=True), dataframe2)


def test_delete_last_metadata(ms_lib):
    ms_lib.write_metadata_history({symbol1: ([metadata1, metadata2], [start_time1, start_time2])})
    ms_lib.delete_last_metadata(symbol1)
    assert_frame_equal(ms_lib.read_metadata(symbol1, history=True), dataframe1)


def test_delete_metadata(ms_lib):
    ms_lib.write_metadata_history({symbol1: ([metadata1, metadata2], [start_time1, start_time2])})
    ms_lib.delete_metadata(symbol1)

    assert not ms_lib.has_symbol(symbol1)

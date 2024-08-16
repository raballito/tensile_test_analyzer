# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 11:18:19 2024

@author: quentin.raball
"""

import pytest
import pandas as pd
from Extractor.TestBench import TestBench  # Remplace `your_module_name` par le nom du module contenant ta classe TestBench

def test_identify_test_bench_shimadzu(mocker):
    tb = TestBench('./Data/Exemple_MS_Shimadzu_Flex_L20_D2.csv')
    tb.test_bench = TestBench.identify_test_bench('./Data/Exemple_MS_Shimadzu_Flex_L20_D2.csv')
    result = tb.identify_file('./Data/Exemple_MS_Shimadzu_Flex_L20_D2.csv')
    
    assert tb.test_bench == 'Shimadzu'
    assert tb.separator == ','
    assert tb.header_index == 2
    assert tb.force_channel == 2
    assert tb.stroke_channel == 3
    assert tb.time_channel == 1
    assert tb.force_unit == 1
    assert tb.repeat_every == 3

def test_identify_file_WB400kN(mocker):
    tb = TestBench('./Data/Exemple_WB400kN_Tract_L100_D2.csv')
    tb.test_bench = TestBench.identify_test_bench('./Data/Exemple_WB400kN_Tract_L100_D2.csv')
    result = tb.identify_file('./Data/Exemple_WB400kN_Tract_L100_D2.csv')
    
    assert tb.separator == ','
    assert tb.header_index == 1
    assert tb.force_channel == 3
    assert tb.stroke_channel == 2
    assert tb.time_channel == 1
    assert tb.force_unit == 1000 #Unités du canal force en kN
    assert tb.repeat_every == 3

def test_identify_file_WB400kN_2(mocker):
    tb = TestBench('./Data/Exemple_WB400kN_2_Tract_L100_D10.csv')
    tb.test_bench = tb.identify_test_bench('./Data/Exemple_WB400kN_2_Tract_L100_D10.csv')
    result = tb.identify_file('./Data/Exemple_WB400kN_2_Tract_L100_D10.csv')
    assert tb.test_bench == 'WB400kN_2'
    assert tb.separator == ','
    assert tb.header_index == 1
    assert tb.force_channel == 3
    assert tb.stroke_channel == 2
    assert tb.time_channel == 1
    assert tb.force_unit == 1 #Unités du canal force en N
    assert tb.repeat_every == 3

def test_identify_file_WB100kN(mocker):
    tb = TestBench('./Data/Exemple_WB100kN_Tract_L100_D2.csv')
    tb.test_bench = tb.identify_test_bench('./Data/Exemple_WB100kN_Tract_L100_D2.csv')
    result = tb.identify_file('./Data/Exemple_WB100kN_Tract_L100_D2.csv')
    assert tb.test_bench == 'WB100kN'
    assert tb.separator == ';'
    assert tb.header_index == 1
    assert tb.force_channel == 3
    assert tb.time_channel == 1
    assert tb.stroke_channel == 10
    assert tb.force_unit == 1000 #Unité canal force en kN
    assert tb.repeat_every == 10

def test_identify_test_bench_unknown(mocker):
    # Mock de pandas.read_csv
    mock_read_csv = mocker.patch('pandas.read_csv')
    mock_read_csv.return_value = pd.DataFrame([
        ['UnknownHeader1', 'UnknownHeader2', 'UnknownHeader3'],
        ['Data1', 'Data2', 'Data3']
    ])
    
    # Mock de open pour éviter FileNotFoundError
    mock_open = mocker.patch('builtins.open', mocker.mock_open(read_data="header,data"))
    
    test_bench = TestBench.identify_test_bench('dummy_file.csv')
    assert test_bench == 'Unknown'




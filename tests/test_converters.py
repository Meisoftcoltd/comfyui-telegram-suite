import pytest
from nodes.converters import AnyToINT, AnyToFLOAT, AnyToBOOLEAN, AnyToSTRING

def test_any_to_int():
    converter = AnyToINT()
    assert converter.convert(None) == (0,)
    assert converter.convert("") == (0,)
    assert converter.convert("   ") == (0,)
    assert converter.convert('"10"') == (10,)
    assert converter.convert("'20'") == (20,)
    assert converter.convert('  "30"  ') == (30,)
    assert converter.convert("10.5") == (10,)
    assert converter.convert('"10.8"') == (10,)
    assert converter.convert(100) == (100,)
    assert converter.convert(100.7) == (100,)
    assert converter.convert("abc") == (0,)
    assert converter.convert("123abc") == (0,)

def test_any_to_float():
    converter = AnyToFLOAT()
    assert converter.convert(None) == (0.0,)
    assert converter.convert("") == (0.0,)
    assert converter.convert("10.5") == (10.5,)
    assert converter.convert('"10.8"') == (10.8,)
    assert converter.convert(100) == (100.0,)

def test_any_to_boolean():
    converter = AnyToBOOLEAN()
    assert converter.convert(None) == (False,)
    assert converter.convert("") == (False,)
    assert converter.convert("true") == (True,)
    assert converter.convert("TRUE") == (True,)
    assert converter.convert("1") == (True,)
    assert converter.convert("yes") == (True,)
    assert converter.convert("false") == (False,)
    assert converter.convert("0") == (False,)

def test_any_to_string():
    converter = AnyToSTRING()
    assert converter.convert(123) == ("123",)
    assert converter.convert("hello") == ("hello",)
    assert converter.convert('"quoted"') == ("quoted",)

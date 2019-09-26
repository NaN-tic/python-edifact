import unittest
from .test_characters import CharactersTest
from .test_controlcharacters import TestControlCharacters
from .test_huge_message import HugeMessageTest
from .test_input_output import InputOutputTest
from .test_message import MessageTest
from .test_parser import ParserTest
from .test_segment import SegmentTest
from .test_serializer import SerializerTest
from .test_token import TokenTest
from .test_tokenizer import TokenizerTest


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(
            CharactersTest))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(
            TestControlCharacters))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(
            InputOutputTest))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(
            MessageTest))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(
            ParserTest))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(
            SegmentTest))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(
            SerializerTest))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(
            TokenTest))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(
            TokenizerTest))
    return suite

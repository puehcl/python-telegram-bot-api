import unittest

import telegram.botapi.util as util

class TestIsCallable(unittest.TestCase):

    def callable_test_method(self):
        pass

    def test_iscallable_method_should_be_callable(self):
        self.assertTrue(util.iscallable(self.callable_test_method))

    def test_iscallable_string_should_not_be_callable(self):
        self.assertFalse(util.iscallable("teststring"))


class TestJsonObject(unittest.TestCase):

    def setUp(self):
        self.json_string = "{   \"intattr\": 5, \"strattr\": \"teststr\", \
                                \"listattr\": [ \
                                    {\"listitem1\": 1}, \
                                    {\"listitem2\": \"foo\"} \
                                ], \
                                \"subobj\": { \
                                    \"subobj_intattr\": 4, \
                                    \"subobj_strattr\": \"substr\", \
                                    \"subobj_listattr\": [ \
                                        {\"sublistitem1\": \"subliststr\"}\
                                    ]}}"
        self.jobj = util.fromjson(self.json_string)

    def test_fromjson(self):
        obj = util.fromjson(self.json_string)


    def test_access_should_work(self):
        self.assertTrue(self.jobj.intattr)
        self.assertTrue(self.jobj.subobj.subobj_strattr)
        self.assertTrue(self.jobj.subobj.subobj_listattr[0].sublistitem1)

    def test_access_should_not_work(self):
        self.assertFalse(self.jobj.absentattr)
        self.assertFalse(self.jobj.subobj.absentattr)

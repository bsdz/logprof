import logging
import unittest
from time import sleep

from logprof import logprof


class LogProfTestCase(unittest.TestCase):
    def test_basic(self):
        logger = logging.getLogger("basic")

        @logprof("bar", logger=logger)
        def function():
            pass

        with self.assertLogs("basic", level="INFO") as cm:
            function()
        self.assertEqual(cm.output[0], "INFO:basic:>>> 'bar' started..")

    def test_class_method(self):
        logger = logging.getLogger("class_methods")

        class Foo:
            @logprof("class func", logger=logger)
            def bar(self):
                pass

        with self.assertLogs("class_methods", level="INFO") as cm:
            Foo().bar()
        self.assertEqual(cm.output[0], "INFO:class_methods:>>> 'class func' started..")

    def test_time(self):
        logger = logging.getLogger("time")

        @logprof("bar", tf="breakdown", logger=logger)
        def function():
            sleep(1)

        with self.assertLogs("time", level="INFO") as cm:
            function()
        self.assertEqual(cm.output[0], "INFO:time:>>> 'bar' started..")
        self.assertRegex(
            cm.output[1],
            r"INFO:time:<<< 'bar' finished. Took \d+s \d+ms \d+us \d+ns",
        )

    def test_time_seconds(self):
        logger = logging.getLogger("time")

        @logprof("bar", tf="seconds", logger=logger)
        def function():
            sleep(1)

        with self.assertLogs("time", level="INFO") as cm:
            function()
        self.assertEqual(cm.output[0], "INFO:time:>>> 'bar' started..")
        self.assertRegex(
            cm.output[1],
            r"INFO:time:<<< 'bar' finished. Took \d+\.\d+s",
        )


if __name__ == "__main__":
    unittest.main()

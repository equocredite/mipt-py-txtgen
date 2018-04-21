import generate
import unittest
import os


class ParserTester(unittest.TestCase):
    def setUp(self):
        self.parser = generate.create_parser()

    def __assert_none(self, keys = set()):
        self.assertIsNotNone(self.args.model)
        self.assertIsNotNone(self.args.length)
        if "seed" in keys:
            self.assertIsNotNone(self.args.seed)
        else:
            self.assertIsNone(self.args.seed)
        if "output" in keys:
            self.assertIsNotNone(self.args.output)
        else:
            self.assertIsNone(self.args.output)

    def test_seed(self):
        self.args = self.parser.parse_args(["--model", "przekurwa",
                                            "--length", "100",
                                            "--seed", "grzegorz"])
        self.__assert_none({"seed"})
        self.assertEqual(self.args.seed, "grzegorz")

    def test_output(self):
        self.args = self.parser.parse_args(["--model", "przekurwa",
                                            "--length", "255",
                                            "--output", "grzegorz"])
        self.__assert_none({"output"})
        self.assertEqual(self.args.output, "grzegorz")

    def test_all(self):
        self.args = self.parser.parse_args(["--model", "lolkek.txt",
                                            "--seed", "sieg1488",
                                            "--length", "228",
                                            "--output", "output.txt"])
        self.__assert_none({"model", "seed", "output", "length"})
        self.assertEqual(self.args.model, "lolkek.txt")
        self.assertEqual(self.args.seed, "sieg1488")
        self.assertEqual(self.args.length, "228")
        self.assertEqual(self.args.output, "output.txt")


class ModelLoadTester(unittest.TestCase):
    def test(self):
        file = open("test.txt", "w")
        file.writelines("aba caba 3\ndaba caba 2")
        file.close()
        file = open("test.txt", "r")
        model = dict()
        generate.load_model(file, model)
        file.close()
        self.assertEqual(model["aba"]["caba"], 3)
        self.assertEqual(model["daba"]["caba"], 2)
        os.system("rm test.txt")


if __name__ == "__main__":
    unittest.main()
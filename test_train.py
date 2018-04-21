import train
import os
import unittest


class ParserTester(unittest.TestCase):
    def setUp(self):
        self.parser = train.create_parser()

    def __assert_none(self, keys = set()):
        self.assertIsNotNone(self.args.model)
        self.assertIsNotNone(self.args.lc)
        if "lc" not in keys:
            self.assertFalse(self.args.lc)
        if "input_dir" in keys:
            self.assertIsNotNone(self.args.input_dir)
        else:
            self.assertIsNone(self.args.input_dir)

    def test_lc(self):
        self.args = self.parser.parse_args(["--lc", "--model", "xyz"])
        self.__assert_none({"lc"})
        self.assertTrue(self.args.lc)
        self.args = self.parser.parse_args(["--model", "bionic_beaver"])
        self.__assert_none()

    def test_input_dir(self):
        self.args = self.parser.parse_args(["--input-dir", "abacaba",
                                            "--model", "model.txt"])
        self.__assert_none({"input_dir"})
        self.assertEqual(self.args.input_dir, "abacaba")

    def test_model(self):
        self.args = self.parser.parse_args(["--model", "dabacaba"])
        self.__assert_none({})
        self.assertEqual(self.args.model, "dabacaba")

    def test_all(self):
        self.args = self.parser.parse_args(["--model", "lolkek.txt",
                                            "--input-dir", "sieg1488",
                                            "--lc"])
        self.__assert_none({"input_dir", "model", "lc"})
        self.assertEqual(self.args.model, "lolkek.txt")
        self.assertEqual(self.args.input_dir, "sieg1488")
        self.assertTrue(self.args.lc)


class ModelTester(unittest.TestCase):
    def setUp(self):
        os.system("mkdir test_input")
        os.chdir("test_input")
        self.model = dict()

    def test_single_file(self):
        os.system("touch input")
        file = open("input", "w")
        file.writelines([
            "On the cushion velvet lining that the lamp-light gloated over\n",
            "But whose velvet-violet lining with the lamp-light gloating over"
        ])
        file.close()
        file = open("input", "r")
        train.process_file(file, True, self.model)
        self.assertEqual(self.model["the"]["cushion"], 1)
        self.assertEqual(self.model["the"]["lamp"], 2)
        self.assertEqual(self.model["lamp"]["light"], 2)
        self.assertEqual(self.model["over"]["but"], 1)
        file.close()

    def test_multiple_files(self):
        self.model.clear()
        os.system("touch input1 input2 input3")
        for file_name in os.listdir("../test_input"):
            file = open(file_name, "w")
            file.writelines("aba caba\ndaba")
            file.close()
            file = open(file_name, "r")
            train.process_file(file, True, self.model)
            file.close()
        self.assertEqual(self.model["aba"]["caba"], 3)
        self.assertEqual(self.model["caba"]["daba"], 3)

    def tearDown(self):
        os.system("rm *")
        os.chdir("..")
        os.system("rmdir test_input")


if __name__ == "__main__":
    unittest.main()

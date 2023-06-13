"""Módulo con tests unitarios de los scripts"""

import io
import os
import unittest
from scripts import *  # pylint: disable=W0614,W0401


class TestYourModule(unittest.TestCase):
    """_summary_
    """

    def test_remove_residual_chars(self):  # pylint: disable=C0116
        input_txt = "Hello\nWorld!"
        expected_output = "HelloWorld!"
        self.assertEqual(remove_residual_chars(input_txt), expected_output)

    def test_remove_special_characters(self):  # pylint: disable=C0116
        input_txt = "Hello\n\nWorld!\t\t"
        expected_output = "HelloWorld!"
        self.assertEqual(remove_special_characters(input_txt), expected_output)

    def test_get_size(self):  # pylint: disable=C0116
        input_obj = [1, 2, 3, 4, 5]
        self.assertEqual(get_size(input_obj), 244)

    def test_random_string(self):  # pylint: disable=C0116
        length = 10
        random_str = random_string(length)
        self.assertEqual(len(random_str), length)

    def test_get_id(self):  # pylint: disable=C0116
        uuid_str = get_id()
        self.assertTrue(isinstance(uuid_str, str))

    def test_write_json_file(self):  # pylint: disable=C0116
        data = {"key": "value"}
        path = "test.json"
        write_json_file(path, data)
        self.assertTrue(is_file_exist(path))
        read_data = read_json_file(path)
        self.assertEqual(data, read_data)
        os.remove(path)

    def test_read_json_file(self):  # pylint: disable=C0116
        data = {"key": "value"}
        path = "test.json"
        write_json_file(path, data)
        read_data = read_json_file(path)
        self.assertEqual(data, read_data)
        os.remove(path)

    def test_is_file_exist(self):  # pylint: disable=C0116
        path = "test_file.txt"
        self.assertFalse(is_file_exist(path))
        with open(path, "w") as file:
            pass
        self.assertTrue(is_file_exist(path))
        os.remove(path)

    def test_remove_bom_mark(self):  # pylint: disable=C0116
        path = "test_file.txt"
        content_with_bom = "\ufeffHello, World!"
        expected_content_without_bom = "Hello, World!"
        with open(path, "w", encoding="utf-8-sig") as file:
            file.write(content_with_bom)
        remove_bom_mark(path)
        with open(path, "r", encoding="utf-8-sig") as file:
            read_content = file.read()
        self.assertEqual(read_content, expected_content_without_bom)
        os.remove(path)

    def test_compress_and_decompress(self):  # pylint: disable=C0116
        files = {"hello.txt": b"hello.txt"}
        compressed_file = compress(files)
        self.assertTrue(isinstance(compressed_file, bytes))
        expected_output = {"hello.txt": b"hello.txt"}
        self.assertEqual(decompress(compressed_file), expected_output)

    def test_bytes_to_base64(self):  # pylint: disable=C0116
        data = b"Hello, World!"
        base64_str = bytes_to_base64(data)
        self.assertEqual(base64.b64decode(base64_str), data)

    def test_base64_to_bytes(self):  # pylint: disable=C0116
        base64_str = base64.b64encode(b"Hello, World!").decode("utf-8")
        data = base64_to_bytes(base64_str)
        self.assertEqual(base64.b64encode(data).decode("utf-8"), base64_str)

    def test_is_office_file(self):  # pylint: disable=C0116
        self.assertEqual(is_office_file("document.docx"), "docx")
        self.assertEqual(is_office_file("presentation.ppt"), "ppt")
        self.assertEqual(is_office_file("spreadsheet.xlsx"), "xlsx")
        self.assertIsNone(is_office_file("image.jpg"))

    def test_get_json_pretty(self):  # pylint: disable=C0116
        data = {"key": "value"}
        expected_output = '{\n    "key": "value"\n}'
        self.assertEqual(get_json_pretty(data), expected_output)

    def test_print_json(self):  # pylint: disable=C0116
        data = {"key": "value"}
        # Redirect stdout to capture print output
        with io.StringIO() as buffer:
            original_stdout = sys.stdout
            sys.stdout = buffer
            print_json(data)
            sys.stdout = original_stdout
            output = buffer.getvalue().strip()
            self.assertEqual(output, get_json_pretty(data))

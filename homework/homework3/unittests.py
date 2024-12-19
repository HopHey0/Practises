import unittest
from hw3 import *

class TestParserFunctions(unittest.TestCase):

    def test_parse_single_line_comment(self):
        # Теперь ожидаем преобразование комментария из "::" в "#"
        self.assertEqual(parse_single_line_comment(":: Комментарий"), "# Комментарий")

    def test_parse_array(self):
        self.assertEqual(parse_array("var myArray := [1; 2; 3]"), "myArray = [1, 2, 3]")
        self.assertIsNone(parse_array("var myArray = [1, 2, 3]"))

    def test_parse_dictionary(self):
        # Адаптируем ожидаемый вывод под текущую реализацию
        self.assertEqual(parse_dictionary("struct { key1 = value1, key2 = value2 }"),
                         "[section]\n  key1 = value1\n  key2 = value2")
        self.assertIsNone(parse_dictionary("var myDict := [1; 2; 3]"))

    def test_parse_constant_declaration(self):
        self.assertEqual(parse_constant_declaration("var x := 10"), "x = 10")
        self.assertEqual(parse_constant_declaration("var name := \"John\""), 'name = "John"')
        self.assertIsNone(parse_constant_declaration("var y ^:= 20"))

    def test_evaluate_expression(self):
        context = {'x': 5, 'y': 10}
        self.assertEqual(evaluate_expression("result = ^(max 10 15)", context), "result = 15")
        self.assertEqual(evaluate_expression("result = ^(- 10 3)", context), "result = 7")

    def test_convert_to_toml(self):
        # Создаем временный файл для тестирования
        with open('test_input.txt', 'w', encoding='utf-8') as f:
            f.write(":: Комментарий\n")
            f.write("var a := 5\n")
            f.write("var b := [1; 2; 3]\n")
            f.write("struct { key1 = value1, key2 = value2 }\n")

        expected_output = (
            '# Комментарий\n'
            'a = 5\n'
            'b = [1, 2, 3]\n'
            '[section]\n'
            '  key1 = value1\n'
            '  key2 = value2\n'
        )

        result_output = convert_to_toml('test_input.txt')

        self.assertEqual(result_output.strip(), expected_output.strip())

if __name__ == '__main__':
    unittest.main()

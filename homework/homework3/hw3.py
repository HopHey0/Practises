import sys
import re

def parse_single_line_comment(line):
    # Преобразуем однострочные комментарии с '::' в формат TOML (начиная с '#')
    if '::' in line:
        return "#" + line.strip().replace("::", "")  # Заменяем '::' на '#'
    return None  # Остальные строки без изменений

def parse_array(line):
    match = re.match(r'var\s+(\w+)\s*:=\s*\[(.*?)\]', line)
    if match:
        values = match.group(2).split(';')
        return f'{match.group(1)} = [{", ".join(value.strip() for value in values)}]'
    return None

def parse_dictionary(line):
    match = re.match(r'struct\s*{\s*(.*?)\s*}', line)
    if match:
        items = match.group(1).split(',')
        dict_items = {}
        for item in items:
            key_value = item.split('=')
            if len(key_value) == 2:
                key = key_value[0].strip()
                value = key_value[1].strip()
                dict_items[key] = value
        
        # Формируем словарь в формате TOML
        return '[section]\n' + '\n'.join(f'  {k} = {v}' for k, v in dict_items.items())
    return None

def parse_constant_declaration(line):
    match = ""
    if '^' not in line:
        match = re.match(r'var\s+(\w+)\s*:=\s*(.*)', line)
    if match:
        return f'{match.group(1)} = {match.group(2).strip()}'
    return None

def evaluate_expression(expression, context):
    expression = expression.replace(":", "").strip()
    def replace_key(match):
        key = match.group(0)  # Получаем найденный ключ
        return str(context[key])  # Возвращаем значение из контекста
    
    # Заменяем ключи на значения
    pattern = r'\b(' + '|'.join(re.escape(key) for key in context.keys()) + r')\b'
    modified_expression = re.sub(pattern, replace_key, expression)
    
    # Меняем местами операцию и число
    def swap_operation(match):
        operation = match.group(1)  # Операция (+, -, max)
        number = match.group(2)      # Число (10 или другое)
        if operation == 'max':
            return f"max({number}, "  # Начинаем с max( и добавляем запятую для следующего числа
        return f"{number} {operation}"  # Меняем местами для других операций

    # Регулярное выражение для поиска операций и чисел
    modified_expression = re.sub(r'(\+|-|max)\s+(\d+)', swap_operation, modified_expression)

    # Извлекаем имя переменной и само выражение без символов ^ и других лишних частей
    var_name = modified_expression.split('=')[0].strip()  # Извлекаем имя переменной
    expression_only = re.search(r'\((.*)\)', modified_expression)
    
    if expression_only:
        expression_to_eval = expression_only.group(1).replace(' ', '')  # Убираем пробелы

        # Если есть max, добавляем закрывающую скобку
        if 'max' in expression_to_eval:
            expression_to_eval += ')'  # Закрываем скобку для max

        # Вычисляем результат
        result = eval(expression_to_eval)

        # Формируем итоговую строку с именем переменной
        final_result = f"{var_name} = {result}"
        return final_result.replace("var","").strip()

    return None

def convert_to_toml(input_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    toml_output = []
    context = {}  # Контекст для хранения значений переменных
    
    for line in lines:
        # Если это комментарий (с '::'), то пропускаем его или преобразуем в TOML комментарий
        parsed_comment = parse_single_line_comment(line)
        if parsed_comment is not None:  # Если комментарий, добавляем его
            toml_output.append(parsed_comment)
            continue
        
        array_result = parse_array(line)
        if array_result:
            toml_output.append(array_result)
            continue
        
        dict_result = parse_dictionary(line)
        if dict_result:
            toml_output.append(dict_result)
            continue
        
        constant_decl_result = parse_constant_declaration(line)
        if constant_decl_result:
            var_name, value_str = constant_decl_result.split('=', 1)
            var_name = var_name.strip()
            value_str = value_str.strip().strip('"')  # Убираем кавычки из строковых значений
            
            # Пробуем преобразовать в число, если это возможно
            try:
                value_int = int(value_str) if value_str.isdigit() else value_str
                context[var_name] = value_int
                toml_output.append(f'{var_name} = {value_int}')
            except ValueError:
                context[var_name] = value_str
                toml_output.append(f'{var_name} = "{value_str}"')
            continue
        
        # Обработка выражений с вычислениями
        eval_result_prefix = None
        # Проверка на префиксные выражения с ^
        if '^' in line:
            eval_result_prefix = evaluate_expression(line, context)
            toml_output.append(eval_result_prefix)
        

    return '\n'.join(toml_output)

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Использование: python script.py <путь_к_файлу>")
        sys.exit(1)

    input_file_path = sys.argv[1]
    
    try:
        toml_output = convert_to_toml(input_file_path)
        print(toml_output)
    except Exception as e:
        print(f'Ошибка: {e}', file=sys.stderr)

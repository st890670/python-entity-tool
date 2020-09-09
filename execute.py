# connect
import psycopg2
from config import db_config, output_config
from string import Template
from util import convert_to_camel_naming, uppercase_first_word
import os

output_config = output_config()
table_name = output_config['table_name']
class_name = uppercase_first_word(convert_to_camel_naming(table_name))
package_path = output_config['package_path']
template_path = 'template\\entity_template.txt'
build_folder_path = 'build'
result_path = f'build\\{class_name}.java'


def execute():
    conn = None
    template_file_io = None
    result_file_io = None

    try:
        params = db_config()

        print('連接資料庫...')
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        print('取得欄位資訊...')
        columns = select(cur)

        filter_column_name = ['id', 'created_date', 'created_user',
                              'modified_date', 'modified_user', 'approval_user', 'approval_date']

        filtered_columns = filter(
            lambda tup: tup[0] not in filter_column_name, columns)

        converted_columns = list(
            map(lambda tup: {'name': tup[0], 'data_type': tup[1]}, filtered_columns))

        print('讀取模板...')
        template_file_io = open(template_path, mode='r')
        template = Template(template_file_io.read())

        type_dict = {'character varying': 'String',
                     'text': 'String',
                     'timestamp without time zone': 'Timestamp',
                     'integer': 'Long',
                     'boolean': 'Boolean'}

        column_result = ''
        for column_dict in converted_columns:
            column_name = column_dict.get('name')
            camel_name = convert_to_camel_naming(column_name)

            column_result += f'    @Column(name = \"{column_name}\")\n'
            column_result += f'    private {type_dict.get(column_dict.get("data_type"))} {camel_name};\n'
            column_result += '\n'
        
        result = template.substitute(
            {'package_path': package_path, 'table_name': table_name, 'class_name': class_name, 'column': column_result})

        if not os.path.exists(build_folder_path):
            os.mkdir(build_folder_path)

        result_file_io = open(result_path, mode='w')

        result_file_io.write(result)
        print('已產出檔案...')

    except (Exception, psycopg2.DatabaseError) as error:
        print(f'error: {error}')

    finally:
        if conn is not None:
            conn.close()
        if template_file_io is not None:
            template_file_io.close()
        if result_file_io is not None:
            result_file_io.close()


def select(cursor):
    cursor.execute(
        f"SELECT column_name, data_type FROM information_schema.columns WHERE table_schema = 'public' AND table_name = '{table_name}';")
    member_columns = cursor.fetchall()
    return member_columns


if __name__ == '__main__':
    execute()

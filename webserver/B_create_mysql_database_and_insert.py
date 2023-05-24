import pymysql
import mysql_operate
from mysql_config import MYSQL_DB
import pandas as pd
from tqdm import tqdm

def exec_sql_once(sql_str):
    db = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='123456',
        database='tis'
    )
    cursor = db.cursor()
    cursor.execute(sql_str)
    db.close()

def table_exist(table_name):
    sql = 'SHOW TABLES;'
    result = mysql_operate.db.select_db(sql);
    for row in result:
        if row[str('Tables_in_' + MYSQL_DB)] == table_name:
            return True
    return False

def main():
    table_name = "image_info"
    csv_path = r'webserver/test.csv'

    if table_exist(table_name):
        sql = 'drop table `' + table_name + '` ;'
        result = mysql_operate.db.execute_db(sql)
        print('Table `{}` already exist! Dropping table `{}`...\n{}'.format(table_name, table_name, result))

    create_table = (
        "CREATE TABLE `{}`  ("
        "`id` int(64) NOT NULL COMMENT 'ids', "
        "`path` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'image path', "
        "`label` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'image label, no used', "
        "PRIMARY KEY (`id`) USING BTREE"
        ") ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;"
    ).format(table_name)
    result = mysql_operate.db.execute_db(create_table)
    print('Creating table {}... \n'.format(table_name) + result)

    df = pd.read_csv(csv_path)
    print('Inserting image info into table `{}`...'.format(table_name))
    for row in tqdm(df.itertuples()):
        id = getattr(row, 'id')
        path = getattr(row, 'path')
        label = getattr(row, 'label')
        insert_row = (
            "INSERT INTO `tis`.`{}`(`id`, `path`, `label`) VALUES ("
            "'{}', '{}', '{}');".format(table_name, id, path, label)
        )
        result = mysql_operate.db.execute_db(insert_row)
        # print('id: {}\n  path: \t{}\n  label: \t{}'.format(id, path, label))
    print('Insert success!')

if __name__ == '__main__':
    main()
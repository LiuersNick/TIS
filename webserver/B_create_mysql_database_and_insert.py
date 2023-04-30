import pymysql
import mysql_operate
from mysql_config import MYSQL_DB
import pandas as pd


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
    csv_path = r'webserver/reverse_image_search.csv'

    if table_exist(table_name):
        sql = 'drop table `' + table_name + '` ;'
        result = mysql_operate.db.execute_db(sql)
        print('Table `{}` already exist! Dropping table `{}`...\n{}'.format(table_name, table_name, result))

    create_table = (
        "CREATE TABLE `image_info`  ("
        "`id` int(64) NOT NULL COMMENT 'ids', "
        "`path` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'image path', "
        "`label` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'image label, no used', "
        "PRIMARY KEY (`id`) USING BTREE"
        ") ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;"
    )
    result = mysql_operate.db.execute_db(create_table)
    print('Creating table {} \n'.format(table_name) + result)

    df = pd.read_csv(csv_path)
    for row in df.itertuples():
        id = getattr(row, 'id')
        path = getattr(row, 'path')
        label = getattr(row, 'label')
        insert_row = (
            "INSERT INTO `tis`.`image_info`(`id`, `path`, `label`) VALUES ("
            "'{}', '{}', '{}');".format(id, path, label)
        )
        result = mysql_operate.db.execute_db(insert_row)
        print('id: {}\n  path: \t{}\n  label: \t{}'.format(id, path, label))

if __name__ == '__main__':
    main()
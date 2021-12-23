import sqlite3
import random

TABLES = {
    'Ships': ['ship', 'weapon', 'hull', 'engine'],
    'Weapons': ['weapon', 'reload_speed', 'rotation_speed', 'diameter'],
    'Hulls': ['hull', 'armor', 'type', 'capacity'],
    'Engines': ['engine', 'power', 'type'],
}

ELEMENTS = {
    'Ships': 200,
    'Weapons': 20,
    'Hulls': 5,
    'Engines': 6,
}

TYPES = {
    'Ships': "TEXT",
    'Weapons': "INT",
    'Hulls': "INT",
    'Engines': "INT",
}


def create_table(database, table_name, attributes, type_values, type_pk='TEXT'):
    base = sqlite3.connect(database)
    sql_query = 'CREATE TABLE IF NOT EXISTS {}({} {} PRIMARY KEY, {})'.format(
                 table_name, attributes[0], type_pk, ', '.join([f'{value} {type_values}' for value in attributes[1:]]))
    base.execute(sql_query)
    base.commit()
    return


def fil_table(base_name, table_name, amount: int):
    base = sqlite3.connect(base_name)
    cur = base.cursor()
    for i in range(1, amount + 1):
        element_name = '-'.join([TABLES[table_name][0].capitalize(), str(i)])
        if table_name == 'Ships':
            values = []
            for attr, value in ELEMENTS.items():
                if attr == 'Ships':
                    continue
                values.append('-'.join([attr[:-1], str(random.randint(1, value))]))
        else:
            values = [str(random.randint(1, 20)) for _ in TABLES[table_name][1:]]

        sql_query = 'INSERT OR REPLACE INTO {} VALUES("{}", "{}");'.format(
                    table_name, element_name, '", "'.join(values))
        cur.execute(sql_query)
    base.commit()
    return


def create_tables(base_name, tables_dict, types_dict):
    for model, attr in tables_dict.items():
        create_table(attributes=attr, database=base_name, table_name=model, type_values=types_dict[model])
    return


def fil_base(base_name, number_of_elements):
    for element, value in number_of_elements.items():
        fil_table(base_name=base_name, table_name=element, amount=value)
    return


def main():
    create_tables(base_name='wg.db', tables_dict=TABLES, types_dict=TYPES)
    fil_base(base_name='wg.db', number_of_elements=ELEMENTS)


if __name__ == '__main__':
    main()


import creator
import random
import os
import pytest
import sqlite3


def change(basename):
    with sqlite3.connect(basename) as _base:
        _cur = _base.cursor()
        db = {
            1: {'table': 'Weapons', 'pk': 'weapon'},
            2: {'table': 'Hulls', 'pk': 'hull'},
            3: {'table': 'Engines', 'pk': 'engine'}
        }
        for ship in _cur.execute('SELECT * FROM Ships;').fetchall():
            chosen = random.choice(ship[1:])
            index = ship.index(chosen)
            new_ship_component = random.choice([i for tuple_ in _cur.execute(
                            f'SELECT {db[index]["pk"]} '
                            f'FROM {db[index]["table"]}').fetchall() for i in tuple_ if i != chosen])
            _cur.execute(f'UPDATE Ships SET {db[index]["pk"]} == "{new_ship_component}" WHERE ship == "{ship[0]}";')

            '''change parameters all components of the ship'''
            for i, component in enumerate(ship[1:], start=1):
                columns = creator.TABLES[db[i]["table"]][1:]
                element = random.choice(columns)
                old_component = _cur.execute(
                    f'SELECT {element} FROM {db[i]["table"]} WHERE {db[i]["pk"]} == "{component}";').fetchone()
                new_component = old_component
                while new_component == old_component:
                    new_component = random.randint(1, 20)
                _cur.execute(f'UPDATE {db[i]["table"]} '
                             f'SET {element} == "{new_component}" WHERE {db[i]["pk"]} == "{component}";')
        _base.commit()


@pytest.fixture(scope='session', autouse=True)
def setup():
    with sqlite3.connect('wg.db') as base, sqlite3.connect('wg_test.db') as _base:
        cur = base.cursor()
        _cur = _base.cursor()
        creator.create_tables(base_name='wg_test.db', tables_dict=creator.TABLES, types_dict=creator.TYPES)
        for table in creator.TABLES:
            for element in cur.execute(f'SELECT * FROM {table};').fetchall():
                sql_query = 'INSERT OR REPLACE INTO {} VALUES("{}");'.format(
                    table, '", "'.join(map(lambda x: str(x), element)))
                _cur.execute(sql_query)
        _base.commit()
        change(basename='wg_test.db')
        yield _base
    # os.remove('wg_test.db')   # all bases are closed, but it's didn't work! sorry, I'm not a wizard(

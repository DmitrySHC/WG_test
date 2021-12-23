import sqlite3
import pytest
import creator


def make_ship_list():
    with sqlite3.connect('wg.db') as base:
        cur = base.cursor()
        my_list = sorted([ship[0] for ship in cur.execute('SELECT ship FROM Ships').fetchall()], key=len)
        return my_list


@pytest.mark.parametrize('ship', make_ship_list())
def test_ship_engine(ship):
    with sqlite3.connect('wg.db') as base, sqlite3.connect('wg_test.db') as _base:
        cur = base.cursor()
        _cur = _base.cursor()
        old_engine = cur.execute('SELECT engine FROM Ships WHERE ship == ?', (ship,)).fetchone()[0]
        new_engine = _cur.execute('SELECT engine FROM Ships WHERE ship == ?', (ship,)).fetchone()[0]
        if old_engine != new_engine:
            print(f'\n{ship}, {new_engine} \n\t expected {old_engine}, was {new_engine}')   # instead hook
            assert False
        old_engine_param = cur.execute(f'SELECT * FROM Engines WHERE engine == "{old_engine}"').fetchone()
        new_engine_param = _cur.execute(f'SELECT * FROM Engines WHERE engine == "{new_engine}"').fetchone()
        error = f'\n{ship}, {new_engine}'
        count_errors = 0
        for param, old, new in zip(creator.TABLES['Engines'], old_engine_param, new_engine_param):
            if old != new:
                error += f'\n\t{param}: expected {old}, was {new}'  # instead hook too
                count_errors += 1
        if count_errors:
            print(error)
            assert False


@pytest.mark.parametrize('ship', make_ship_list())
def test_ship_weapon(ship):
    with sqlite3.connect('wg.db') as base, sqlite3.connect('wg_test.db') as _base:
        cur = base.cursor()
        _cur = _base.cursor()
        old_weapon = cur.execute('SELECT weapon FROM Ships WHERE ship == ?', (ship,)).fetchone()[0]
        new_weapon = _cur.execute('SELECT weapon FROM Ships WHERE ship == ?', (ship,)).fetchone()[0]
        if old_weapon != new_weapon:
            print(f'\n{ship}, {new_weapon} \n\t expected {old_weapon}, was {new_weapon}')
            assert False
        old_weapon_param = cur.execute(f'SELECT * FROM Weapons WHERE weapon == "{old_weapon}"').fetchone()
        new_weapon_param = _cur.execute(f'SELECT * FROM Weapons WHERE weapon == "{new_weapon}"').fetchone()
        error = f'\n{ship}, {new_weapon}'
        count_errors = 0
        for param, old, new in zip(creator.TABLES['Weapons'], old_weapon_param, new_weapon_param):
            if old != new:
                error += f'\n\t{param}: expected {old}, was {new}'
                count_errors += 1
        if count_errors:
            print(error)
            assert False


@pytest.mark.parametrize('ship', make_ship_list())
def test_ship_hull(ship):
    with sqlite3.connect('wg.db') as base, sqlite3.connect('wg_test.db') as _base:
        cur = base.cursor()
        _cur = _base.cursor()
        old_hull = cur.execute('SELECT hull FROM Ships WHERE ship == ?', (ship,)).fetchone()[0]
        new_hull = _cur.execute('SELECT hull FROM Ships WHERE ship == ?', (ship,)).fetchone()[0]
        if old_hull != new_hull:
            print(f'\n{ship}, {new_hull} \n\t expected {old_hull}, was {new_hull}')
            assert False
        old_hull_param = cur.execute(f'SELECT * FROM Hulls WHERE hull == "{old_hull}"').fetchone()
        new_hull_param = _cur.execute(f'SELECT * FROM Hulls WHERE hull == "{new_hull}"').fetchone()
        error = f'\n{ship}, {new_hull}'
        count_errors = 0
        for param, old, new in zip(creator.TABLES['Hulls'], old_hull_param, new_hull_param):
            if old != new:
                error += f'\n\t{param}: expected {old}, was {new}'
                count_errors += 1
        if count_errors:
            print(error)
            assert False

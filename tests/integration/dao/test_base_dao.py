import uuid

import pytest

from dao.base_dao import BaseDAO


class DAOofTest(BaseDAO):
    columns = 'id, name'
    table = 'dao'
    pkid = 'id'

    sql_create_table = "CREATE TABLE `daooftest` (" \
                       "`id` int(11) NOT NULL, " \
                       "`name` varchar(32) NOT NULL)"

    sql_truncate_table = "TRUNCATE TABLE `daooftest`"

    sql_drop_table = "DROP TABLE IF EXISTS `daooftest`"

    sql_insert_record = "INSERT INTO `daooftest` (`id`, `name`) VALUES (%s, %s)"


@pytest.fixture(autouse=True, scope='module')
def table_during_module_tests(pymsqlconnection):
    cursor = pymsqlconnection.cursor()
    cursor.execute(DAOofTest.sql_drop_table)
    cursor.execute(DAOofTest.sql_create_table)
    pymsqlconnection.commit()
    yield
    cursor.execute(DAOofTest.sql_drop_table)
    pymsqlconnection.commit()


@pytest.fixture(name='records', scope='class')
def records(pymsqlconnection):
    records = [{'id': 1, 'name': 'dummpy-name1'},
               {'id': 2, 'name': 'dummpy-name2'},
               {'id': 3, 'name': 'dummpy-namelist'},
               {'id': 4, 'name': 'dummpy-namelist'}]

    cursor = pymsqlconnection.cursor()
    cursor.execute(DAOofTest.sql_insert_record, (1, 'dummpy-name1'))
    cursor.execute(DAOofTest.sql_insert_record, (2, 'dummpy-name2'))
    cursor.execute(DAOofTest.sql_insert_record, (3, 'dummpy-namelist'))
    cursor.execute(DAOofTest.sql_insert_record, (4, 'dummpy-namelist'))
    pymsqlconnection.commit()
    return records


@pytest.mark.usefixtures('enter_request_context')
class TestBaseDAO:
    def test_get_by_id(self, records):
        record0 = DAOofTest.get_by_id(records[0]['id'])
        record1 = DAOofTest.get_by_id(records[1]['id'])
        record2 = DAOofTest.get_by_id(max(records[0]['id'], records[1]['id']) + 1)

        assert record0 == records[0]
        assert record1 == records[1]
        assert record2 is None

    def test_get_by_column(self, records):
        record0 = DAOofTest.get_by_column('name', records[0]['name'])
        record1 = DAOofTest.get_by_column('name', records[1]['name'])
        record2 = DAOofTest.get_by_column('name', str(uuid.uuid1()))

        assert record0 == records[0]
        assert record1 == records[1]
        assert record2 is None

    def test_get_list_by_column(self, records):
        records1 = DAOofTest.get_many_by_column('name', records[2]['name'])
        records2 = DAOofTest.get_many_by_column('name', records[3]['name'], orderby='id')
        records3 = DAOofTest.get_many_by_column('name', str(uuid.uuid1()))

        assert sorted(records1, key=lambda x: x['id']) == list(records2)
        assert len(records3) == 0

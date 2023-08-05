import random
import pandas as pd
import datetime
from dwopt import make_eng, Pg, Lt, Oc
from dwopt.set_up import _TEST_PG_URL, _TEST_LT_URL, _TEST_OC_URL
import sqlalchemy as alc
from sqlalchemy.dialects.oracle import NUMBER
from sqlalchemy.dialects.postgresql import BIGINT
import logging

_logger = logging.getLogger(__file__)


def make_test_df(n=10000):
    """Make a test dataframe with various data types and missing values.

    Details see :func:`dwopt.make_test_tbl`.

    Parameters
    ------------
    n: int
        Number of records.

    Returns
    --------
    pandas.DataFrame

    Examples
    ----------
    >>> from dwopt.testing import make_test_df
    >>> make_test_df(10000).iloc[0,:]
    id                                0
    score                      4.066531
    amt                             813
    cat                            test
    date                     2022-01-01
    time     2022-03-03 10:19:35.071235
    Name: 0, dtype: object
    """
    random.seed(0)
    df = pd.DataFrame(
        {
            "id": range(n),
            "score": [random.uniform(-1, 5) for i in range(n)],
            "amt": random.choices(range(1000), k=n),
            "cat": random.choices(["test", "train"], k=n),
            "date": [
                datetime.date.fromisoformat(i)
                for i in random.choices(["2022-01-01", "2022-02-02", "2022-03-03"], k=n)
            ],
            "time": [
                datetime.datetime.fromisoformat(i)
                for i in random.choices(
                    [
                        "2022-01-01 00:19:02.011135",
                        "2022-02-02 23:00:00.000000",
                        "2022-03-03 10:19:35.071235",
                    ],
                    k=n,
                )
            ],
        }
    )

    for col in ["score", "cat", "date", "time"]:
        df.loc[random.choices(range(n), k=int(n / 20)), col] = None

    return df


def _parse_sch_tbl_nme(sch_tbl_nme):
    return Pg._parse_sch_tbl_nme(Pg, sch_tbl_nme)


def _make_pg_tbl(df, eng, sch_tbl_nme):
    _, sch, tbl_nme = _parse_sch_tbl_nme(sch_tbl_nme)
    meta = alc.MetaData()
    test_tbl = alc.Table(
        tbl_nme,
        meta,
        alc.Column("id", BIGINT, primary_key=True),
        alc.Column("score", alc.Float(8)),
        alc.Column("amt", BIGINT),
        alc.Column("cat", alc.String(20)),
        alc.Column("date", alc.Date),
        alc.Column("time", alc.DateTime),
        schema=sch,
    )
    with eng.connect() as conn:
        test_tbl.drop(conn, checkfirst=True)
    meta.create_all(eng)
    with eng.connect() as conn:
        conn.execute(
            test_tbl.insert(),
            df.assign(
                time=lambda x: x.time.astype(object).where(~x.time.isna(), None)
            ).to_dict("records"),
        )


def _make_lt_tbl(df, eng, sch_tbl_nme):
    _, sch, tbl_nme = _parse_sch_tbl_nme(sch_tbl_nme)
    meta = alc.MetaData()
    test_tbl = alc.Table(
        tbl_nme,
        meta,
        alc.Column("id", alc.Integer, primary_key=True),
        alc.Column("score", alc.REAL),
        alc.Column("amt", alc.Integer),
        alc.Column("cat", alc.String),
        alc.Column("date", alc.String),
        alc.Column("time", alc.String),
        schema=sch,
    )
    with eng.connect() as conn:
        test_tbl.drop(conn, checkfirst=True)
    meta.create_all(eng)
    with eng.connect() as conn:
        conn.execute(
            test_tbl.insert(),
            df.assign(
                time=lambda x: x.time.astype(str).where(~x.time.isna(), None)
            ).to_dict("records"),
        )


def _make_oc_tbl(df, eng, sch_tbl_nme):
    _, sch, tbl_nme = _parse_sch_tbl_nme(sch_tbl_nme)
    meta = alc.MetaData()
    test_tbl = alc.Table(
        tbl_nme,
        meta,
        alc.Column("id", NUMBER, primary_key=True),
        alc.Column("score", alc.Float),
        alc.Column("amt", NUMBER),
        alc.Column("cat", alc.String(20)),
        alc.Column("date", alc.Date),
        alc.Column("time", alc.DateTime),
        schema=sch,
    )
    with eng.connect() as conn:
        test_tbl.drop(conn, checkfirst=True)
    meta.create_all(eng)
    with eng.connect() as conn:
        conn.execute(
            test_tbl.insert(),
            df.assign(
                time=lambda x: x.time.astype(object).where(~x.time.isna(), None)
            ).to_dict("records"),
        )


def make_test_tbl(db, sch_tbl_nme="test", n=10000):
    """Make or remake a test table on database.

    Uses Sqlalchemy toolkits for table drop, creation, insertion.

    Parameters
    ------------
    db: dwopt.dbo._Db, or str
        Dwopt database operator object. Or one of ``'pg'``, ``'lt'``, and ``'oc'``,
        indicating usage of pre-defined testing database engines.
    sch_tbl_nme: str
        Table name in form ``my_schema1.my_table1`` or ``my_table1``.
    n: int
        Number of records.

    Returns
    ----------
    (dwopt.dbo._Db, pandas.DataFrame):
        Tuple of database operator used, and the test dataframe.

    Notes
    ------

    **Table specifications**

    ====== ============== =========== ===================
    Column Data type      None values Example
    ====== ============== =========== ===================
    id     int64                      0
    score  float64        NaN         4.066531
    amt    int64                      867
    cat    str            None        train
    date   datetime.date  None        2022-03-03
    time   datetime64[ns] NaT         2022-02-02 23:00:00
    ====== ============== =========== ===================

    **Test database table specifications**

    ====== =========== ======= ============
    Column Postgre     Sqlite  Oracle
    ====== =========== ======= ============
    id     bigint      integer number
    score  float8      real    float
    amt    bigint      integer number
    cat    varchar(20) text    varchar2(20)
    date   date        text    date
    time   timestamp   text    timestamp
    ====== =========== ======= ============

    These datatypes are implemented via respective
    `Sqlalchemy datatypes <https://docs.sqlalchemy.org/en/14/core/type_basics.html>`_.

    The ``id`` column will be made primary key in the test database tables.

    *Datetime types*

    The ``time`` column's ``NaT`` objects are converted into None before insertion for
    Postgre and Oracle.
    The ``time`` column are converted into str and None before insertion for Sqlite.

    See :meth:`dwopt.dbo._Db.write` for discussion on
    datetime columns and reversibility of insert statements.

    **Pre-defined testing database engines**

    * ``pg``: ``postgresql://dwopt_tester:1234@localhost/dwopt_test``
    * ``lt``: ``sqlite://``
    * ``oc``: Not implemented.

    **Install testing databases**

    *Postgre*::

        psql -U postgres
        CREATE DATABASE dwopt_test;
        CREATE USER dwopt_tester WITH PASSWORD '1234';
        GRANT ALL PRIVILEGES ON DATABASE dwopt_test to dwopt_tester;

    *Oracle*

    * Install oracle db from the
      `oracle xe <https://www.oracle.com/database/technologies/xe-downloads.html>`_.
    * Schema: test_schema
    * Not implemented.

    Examples
    ----------
    Make test table through user provided database operator:

    >>> from dwopt import lt, make_test_tbl
    >>> _ = make_test_tbl(lt)
    >>> lt.qry('test').len()
    10000

    Use the function to make database operator linked to the pre-defined
    test databases, then make test table on it:

    >>> from dwopt import make_test_tbl
    >>> lt, df = make_test_tbl('lt', 'foo', 999)
    >>> lt.eng
    Engine(sqlite://)
    >>> lt.qry('foo').len()
    999
    >>> len(df)
    999
    """
    if isinstance(db, str):
        if db == "pg":
            db = Pg(make_eng(_TEST_PG_URL))
        elif db == "lt":
            db = Lt(make_eng(_TEST_LT_URL))
        elif db == "pg":
            db = Oc(make_eng(_TEST_OC_URL))
        else:
            raise ValueError("Invalid db str, use one of 'pg', 'lt', or 'oc'")
    df = make_test_df(n)
    if isinstance(db, Pg):
        _make_pg_tbl(df, db.eng, sch_tbl_nme)
    elif isinstance(db, Lt):
        _make_lt_tbl(df, db.eng, sch_tbl_nme)
    elif isinstance(db, Oc):
        _make_oc_tbl(df, db.eng, sch_tbl_nme)
    else:
        raise ValueError(
            "Invalid db, must be a database operator object, instances of "
            "(dwopt.Pg, dwopt.Lt, dwopt.Oc)"
        )
    return db, df

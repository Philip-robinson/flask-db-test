import sqlite3

con = sqlite3.connect("shares.db")

con.executescript(
    """
    DROP TABLE transactions;
    DROP TABLE prices;
    DROP TABLE shares;

    CREATE TABLE shares(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        name TEXT NOT NULL
    );
    CREATE TABLE transactions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        share_id INTEGER NOT NULL,
        created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        buy_sell varchar(4) NOT NULL,
        number INTEGER NOT NULL,
        cost NUMBER(10,2) NOT NULL,
        FOREIGN KEY(share_id) REFERENCES shars(id)
    );
    CREATE TABLE prices(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        share_id INTEGER NOT NULL,
        created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        price NUMBER(10,2),
        FOREIGN KEY(share_id) REFERENCES shars(id)
    );
    """)
curs = con.cursor()
curs.executemany("INSERT INTO shares(name) VALUES (?)",[
     ("Ashtead Group PLC (LSE:AHT)",),
     ("BHP Group PLC (LSE:BHP)",),
     ("BP PLC (LSE:BP.)",),
     ("Ferguson PLC (LSE:FERG)",),
     ("Hoist Finance AB (XSTO:HOFI)",),
     ("Royal Mail PLC (LSE:RMG)",),
     ("SThree PLC (LSE:STEM)",),
     ("BP PLC (LSE:BP.)",),
     ("Deutsche Post AG (XETRA:DPW)",),
     ("Ferguson PLC (LSE:FERG)",),
     ("Mondi PLC (LSE:MNDI)",),
     ("Smurfit Kappa Group PLC (LSE:SKG)",),
     ("SThree PLC (LSE:STEM)",),
     ("Telefonica Deutschland Holding AG (XETRA:O2D)",),
     ("Tesco PLC (LSE:TSCO)",)])

curs.executemany("INSERT INTO prices(share_id, price) VALUES (?, ?)", [
    (con.execute("select id from shares where name=?", ("Ashtead Group PLC (LSE:AHT)",)).fetchone()[0], "60.58"),
    (con.execute("select id from shares where name=?", ("BHP Group PLC (LSE:BHP)",)).fetchone()[0], "23.055"),
    (con.execute("select id from shares where name=?", ("BP PLC (LSE:BP.)",)).fetchone()[0], "3.6255"),
    (con.execute("select id from shares where name=?", ("Ferguson PLC (LSE:FERG)",)).fetchone()[0], "128.4"),
    (con.execute("select id from shares where name=?", ("Hoist Finance AB (XSTO:HOFI)",)).fetchone()[0], "31.5"),
    (con.execute("select id from shares where name=?", ("Royal Mail PLC (LSE:RMG)",)).fetchone()[0], "5.188"),
    (con.execute("select id from shares where name=?", ("SThree PLC (LSE:STEM)",)).fetchone()[0], "4.31"),
    (con.execute("select id from shares where name=?", ("BP PLC (LSE:BP.)",)).fetchone()[0], "3.6255"),
    (con.execute("select id from shares where name=?", ("Deutsche Post AG (XETRA:DPW)",)).fetchone()[0], "56.1"),
    (con.execute("select id from shares where name=?", ("Ferguson PLC (LSE:FERG)",)).fetchone()[0], "128.4"),
    (con.execute("select id from shares where name=?", ("Mondi PLC (LSE:MNDI)",)).fetchone()[0], "18.89"),
    (con.execute("select id from shares where name=?", ("Smurfit Kappa Group PLC (LSE:SKG)",)).fetchone()[0], "41.39"),
    (con.execute("select id from shares where name=?", ("SThree PLC (LSE:STEM)",)).fetchone()[0], "4.31"),
    (con.execute("select id from shares where name=?", ("Telefonica Deutschland Holding AG (XETRA:O2D)",)).fetchone()[0], "2.458")])

curs.executemany("insert into transactions(share_id, buy_sell, number, cost)values(?, 'BUY', ?, ?)", 
    [(con.execute("select id from shares where name=?", ("Ashtead Group PLC (LSE:AHT)",)).fetchone()[0], 168, 10049.27),
    (con.execute("select id from shares where name=?", ("BHP Group PLC (LSE:BHP)",)).fetchone()[0], 274, 6018.41),
    (con.execute("select id from shares where name=?", ("BP PLC (LSE:BP.)",)).fetchone()[0], 1476, 4899.20),
    (con.execute("select id from shares where name=?", ("Ferguson PLC (LSE:FERG)",)).fetchone()[0], 30, 3962.28),
    (con.execute("select id from shares where name=?", ("Hoist Finance AB (XSTO:HOFI)",)).fetchone()[0], 37, 97.89),
    (con.execute("select id from shares where name=?", ("Royal Mail PLC (LSE:RMG)",)).fetchone()[0], 912, 4288.43),
    (con.execute("select id from shares where name=?", ("SThree PLC (LSE:STEM)",)).fetchone()[0], 1079, 5025.67),
    (con.execute("select id from shares where name=?", ("BP PLC (LSE:BP.)",)).fetchone()[0], 6, 20.89),
    (con.execute("select id from shares where name=?", ("Deutsche Post AG (XETRA:DPW)",)).fetchone()[0], 4, 193.87),
    (con.execute("select id from shares where name=?", ("Ferguson PLC (LSE:FERG)",)).fetchone()[0], 1, 114.80),
    (con.execute("select id from shares where name=?", ("Mondi PLC (LSE:MNDI)",)).fetchone()[0], 440, 8043.52),
    (con.execute("select id from shares where name=?", ("Smurfit Kappa Group PLC (LSE:SKG)",)).fetchone()[0], 271, 10553.51),
    (con.execute("select id from shares where name=?", ("SThree PLC (LSE:STEM)",)).fetchone()[0], 2239, 10797.71),
    (con.execute("select id from shares where name=?", ("Telefonica Deutschland Holding AG (XETRA:O2D)",)).fetchone()[0], 19, 40.84),
    (con.execute("select id from shares where name=?", ("Tesco PLC (LSE:TSCO)",)).fetchone()[0], 1759, 5027.79)])

con.commit()
con.close()

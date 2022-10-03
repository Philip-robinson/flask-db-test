import sqlite3

def getCon():
    return sqlite3.connect("shares.db")

class Portfolio:

    def names(self):
        con = getCon()
        cur = con.cursor()
        res =  cur.execute("SELECT id, name FROM shares").fetchall()
        con.close()
        return [{"id": row[0], "name": row[1]} for row in res];

    def detail(self, id):
        con = getCon()
        cur = con.cursor()
        price, name, number, cost = cur.execute("""
                          SELECT p.price, s.name, sum(t.number), sum(cost)
                          FROM shares s
                          LEFT JOIN transactions t ON s.id = t.share_id
                          LEFT JOIN prices p ON p.share_id=s.id
                          WHERE s.id=? 
                          AND NOT EXISTS(
                              SELECT * 
                              FROM prices p2
                              WHERE p2.id > p.id
                              AND p2.share_id=p.share_id)
                          GROUP BY p.price
                          """, (id,)).fetchone()
        if number is None:
            number=0
        con.close()
        if cost is None:
            cost=0
        con.close()
        if price is None:
            price=0
        con.close()
        return{"price": price,
               "name": name,
               "number": number,
               "cost": cost,
               "value": price*number,
               "profit": price*number-cost
        }

        

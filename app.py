from flask import Flask, render_template, request, redirect, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "secret"

# DB作成
def init_db():
    conn = sqlite3.connect("drink.db")
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        weight REAL,
        total REAL
    )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/test")
def test():
    return "HELLO"

@app.route("/", methods=["GET","POST"])
def start():
    if request.method == "POST":
        name = request.form["name"]
        weight = request.form["weight"]

        conn = sqlite3.connect("drink.db")
        c = conn.cursor()
        c.execute("INSERT INTO players (name, weight, total) VALUES (?, ?, 0)",
                  (name, weight))
        conn.commit()
        player_id = c.lastrowid
        conn.close()

        session["player_id"] = player_id
        return redirect("/game")

    return render_template("start.html")


@app.route("/game")
def game():
    conn = sqlite3.connect("drink.db")
    c = conn.cursor()
    c.execute("SELECT * FROM players ORDER BY total DESC")
    players = c.fetchall()
    conn.close()

    return render_template("game.html", players=players)


@app.route("/add/<int:amount>")
def add(amount):
    player_id = session.get("player_id")

    conn = sqlite3.connect("drink.db")
    c = conn.cursor()
    c.execute("UPDATE players SET total = total + ? WHERE id = ?",
              (amount, player_id))
    conn.commit()
    conn.close()

    return redirect("/game")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

DATABASE = "database.db"


def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    connection = get_db_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            severity TEXT NOT NULL,
            status TEXT NOT NULL,
            description TEXT,
            source TEXT,
            assigned_to TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


@app.route("/")
def index():
    connection = get_db_connection()

    incidents = connection.execute("""
        SELECT *
        FROM incidents
        ORDER BY id DESC
    """).fetchall()

    stats = {
        "total": connection.execute(
            "SELECT COUNT(*) FROM incidents"
        ).fetchone()[0],

        "open": connection.execute(
            "SELECT COUNT(*) FROM incidents WHERE status != 'Closed'"
        ).fetchone()[0],

        "critical": connection.execute(
            "SELECT COUNT(*) FROM incidents WHERE severity = 'Critical'"
        ).fetchone()[0],

        "closed": connection.execute(
            "SELECT COUNT(*) FROM incidents WHERE status = 'Closed'"
        ).fetchone()[0]
    }

    connection.close()

    return render_template(
        "index.html",
        incidents=incidents,
        stats=stats
    )


@app.route("/new", methods=["GET", "POST"])
def new_incident():

    if request.method == "POST":

        title = request.form["title"]
        category = request.form["category"]
        severity = request.form["severity"]
        description = request.form["description"]
        source = request.form["source"]
        assigned_to = request.form["assigned_to"]

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        connection = get_db_connection()

        connection.execute("""
            INSERT INTO incidents (
                title,
                category,
                severity,
                status,
                description,
                source,
                assigned_to,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            title,
            category,
            severity,
            "New",
            description,
            source,
            assigned_to,
            current_time,
            current_time
        ))

        connection.commit()
        connection.close()

        return redirect(url_for("index"))

    return render_template("new_incident.html")


@app.route("/incident/<int:incident_id>")
def incident(incident_id):

    connection = get_db_connection()

    incident = connection.execute(
        "SELECT * FROM incidents WHERE id = ?",
        (incident_id,)
    ).fetchone()

    connection.close()

    if incident is None:
        return "Incident not found", 404

    return render_template(
        "incident.html",
        incident=incident
    )


@app.route("/incident/<int:incident_id>/status", methods=["POST"])
def update_status(incident_id):

    status = request.form["status"]

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    connection = get_db_connection()

    connection.execute("""
        UPDATE incidents
        SET status = ?, updated_at = ?
        WHERE id = ?
    """, (
        status,
        current_time,
        incident_id
    ))

    connection.commit()
    connection.close()

    return redirect(
        url_for("incident", incident_id=incident_id)
    )


@app.route("/incident/<int:incident_id>/delete", methods=["POST"])
def delete_incident(incident_id):

    connection = get_db_connection()

    connection.execute(
        "DELETE FROM incidents WHERE id = ?",
        (incident_id,)
    )

    connection.commit()
    connection.close()

    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
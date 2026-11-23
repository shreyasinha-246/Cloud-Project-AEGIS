import sqlite3
from datetime import datetime

DB_NAME = "aegis.db"

def connect_db():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            cpu REAL,
            ram REAL,
            disk REAL,
            network_sent REAL,
            network_received REAL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            message TEXT
        )
    """)

    cursor.execute("PRAGMA table_info(metrics)")
    columns = [row[1] for row in cursor.fetchall()]

    if "network_sent" not in columns:
        cursor.execute("ALTER TABLE metrics ADD COLUMN network_sent REAL")

    if "network_received" not in columns:
        cursor.execute("ALTER TABLE metrics ADD COLUMN network_received REAL")

    conn.commit()
    conn.close()


def save_data(metrics, alerts):
    conn = connect_db()
    cursor = conn.cursor()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO metrics
        (timestamp, cpu, ram, disk, network_sent, network_received)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        timestamp,
        metrics["cpu"],
        metrics["ram"],
        metrics["disk"],
        metrics["network_sent"],
        metrics["network_received"]
    ))

    for alert in alerts:
        if alert != "SYSTEM STATUS: NORMAL":
            cursor.execute("""
                INSERT INTO alerts (timestamp, message)
                VALUES (?, ?)
            """, (timestamp, alert))

    conn.commit()
    conn.close()


def get_recent_metrics(limit=10):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT timestamp, cpu, ram, disk,
               network_sent, network_received
        FROM metrics ORDER BY id DESC LIMIT ?
    """, (limit,))

    records = cursor.fetchall()
    conn.close()
    return records


def get_recent_alerts(limit=10):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT timestamp, message
        FROM alerts ORDER BY id DESC LIMIT ?
    """, (limit,))

    records = cursor.fetchall()
    conn.close()
    return records
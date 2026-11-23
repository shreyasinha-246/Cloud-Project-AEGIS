import tkinter as tk
from tkinter import ttk

from monitor import get_metrics
from detector import detect_issues
from database import save_data, get_recent_metrics, get_recent_alerts


def start_dashboard():

    root = tk.Tk()
    root.title("AEGIS - Intelligent System Monitoring")
    root.geometry("1100x800")
    root.configure(bg="#101820")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview",
                    background="#243447",
                    foreground="white",
                    fieldbackground="#243447",
                    rowheight=28)
    style.configure("Treeview.Heading",
                    background="#34495e",
                    foreground="white",
                    font=("Arial", 10, "bold"))

    tk.Label(root, text="AEGIS",
             font=("Arial", 28, "bold"),
             bg="#101820", fg="white").pack(pady=(15, 0))

    tk.Label(root, text="INTELLIGENT SYSTEM MONITORING",
             font=("Arial", 11),
             bg="#101820", fg="lightgray").pack()

    status = tk.Label(root, text="CONNECTING...",
                      font=("Arial", 15, "bold"),
                      bg="#101820", fg="lightgreen")
    status.pack(pady=15)

    cards = tk.Frame(root, bg="#101820")
    cards.pack(fill="x", padx=20)

    resources = {}

    for name in ["CPU", "RAM", "DISK"]:
        card = tk.Frame(cards, bg="#243447", padx=15, pady=15)
        card.pack(side="left", expand=True, fill="x", padx=8)

        tk.Label(card, text=name + " USAGE",
                 font=("Arial", 12, "bold"),
                 bg="#243447", fg="white").pack()

        value = tk.Label(card, text="0%",
                         font=("Arial", 22, "bold"),
                         bg="#243447", fg="white")
        value.pack(pady=8)

        bar = ttk.Progressbar(card, maximum=100, length=180)
        bar.pack(fill="x")

        resources[name] = (value, bar)

    network_frame = tk.Frame(root, bg="#243447", padx=15, pady=12)
    network_frame.pack(fill="x", padx=28, pady=15)

    network_label = tk.Label(
        network_frame,
        text="NETWORK DATA: Waiting...",
        font=("Arial", 12, "bold"),
        bg="#243447", fg="white"
    )
    network_label.pack()

    tk.Label(root, text="MONITORING HISTORY",
             font=("Arial", 14, "bold"),
             bg="#101820", fg="white").pack(pady=8)

    history = ttk.Treeview(
        root,
        columns=("time", "cpu", "ram", "disk", "sent", "received"),
        show="headings", height=7
    )

    headings = [
        ("time", "Timestamp"),
        ("cpu", "CPU (%)"),
        ("ram", "RAM (%)"),
        ("disk", "Disk (%)"),
        ("sent", "Sent (MB)"),
        ("received", "Received (MB)")
    ]

    for col, heading in headings:
        history.heading(col, text=heading)
        history.column(col, width=145, anchor="center")

    history.pack(fill="x", padx=25)

    tk.Label(root, text="ALERT HISTORY",
             font=("Arial", 14, "bold"),
             bg="#101820", fg="white").pack(pady=15)

    alert_table = ttk.Treeview(
        root,
        columns=("time", "message"),
        show="headings", height=5
    )

    alert_table.heading("time", text="Timestamp")
    alert_table.heading("message", text="Alert Message")
    alert_table.column("time", width=250, anchor="center")
    alert_table.column("message", width=650, anchor="w")

    alert_table.pack(fill="x", padx=25)

    def update_dashboard():

        try:
            metrics = get_metrics()
            alerts = detect_issues(metrics)

            save_data(metrics, alerts)

            for name, key in [
                ("CPU", "cpu"),
                ("RAM", "ram"),
                ("DISK", "disk")
            ]:
                value, bar = resources[name]
                value.config(text=f"{metrics[key]:.1f}%")
                bar["value"] = metrics[key]

            if alerts[0] == "SYSTEM STATUS: NORMAL":
                status.config(text="SYSTEM STATUS: NORMAL",
                              fg="lightgreen")
            else:
                status.config(text="SYSTEM STATUS: WARNING",
                              fg="orange")

            network_label.config(
                text=f"NETWORK DATA | Sent: {metrics['network_sent']} MB"
                     f" | Received: {metrics['network_received']} MB"
            )

            for item in history.get_children():
                history.delete(item)

            for record in get_recent_metrics(10):
                history.insert("", "end", values=(
                    record[0], record[1], record[2],
                    record[3], record[4], record[5]
                ))

            for item in alert_table.get_children():
                alert_table.delete(item)

            for record in get_recent_alerts(10):
                alert_table.insert("", "end", values=record)

        except Exception as error:
            status.config(text="MONITORING ERROR", fg="red")
            print("Error:", error)

        root.after(3000, update_dashboard)

    root.after(500, update_dashboard)
    root.mainloop()


if __name__ == "__main__":
    start_dashboard()
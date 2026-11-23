from config import CPU_THRESHOLD, RAM_THRESHOLD, DISK_THRESHOLD

def detect_issues(metrics):

    alerts = []

    if metrics["cpu"] > CPU_THRESHOLD:
        alerts.append("WARNING: High CPU Usage!")

    if metrics["ram"] > RAM_THRESHOLD:
        alerts.append("WARNING: High RAM Usage!")

    if metrics["disk"] > DISK_THRESHOLD:
        alerts.append("WARNING: High Disk Usage!")

    if not alerts:
        alerts.append("SYSTEM STATUS: NORMAL")

    return alerts
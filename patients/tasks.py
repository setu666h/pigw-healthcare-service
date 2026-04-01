import threading
import time


def send_welcome_email(patient_name):
    """
    Simulate sending a welcome email in background
    """
    time.sleep(2)  # simulate delay
    print(f"Welcome email sent to {patient_name}")


def run_async_email(patient_name):
    """
    Run email task in background thread
    """
    thread = threading.Thread(target=send_welcome_email, args=(patient_name,))
    thread.start()
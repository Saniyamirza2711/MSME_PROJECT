from logger import log_info, log_error

log_info("This is a test info log.")
log_error("This is a test error log.")

with open("logs/error.log", "r") as f:
    print("\nLog File Contents:\n")
    print(f.read())  # ✅ Print contents of error.log

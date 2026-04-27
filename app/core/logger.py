def log(widget, msg):
    try:
        widget.insert("end", msg + "\n")
        widget.see("end")
    except Exception:
        print(msg)
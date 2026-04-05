import datetime

def get_realtime_info():
    now = datetime.datetime.now()
    return f"""
Current Date & Time Info:
Day: {now.strftime("%A")}
Date: {now.strftime("%d %B %Y")}
Time: {now.strftime("%H:%M:%S")}
"""

def clean_text(text):
    return "\n".join([line for line in text.split("\n") if line.strip()])
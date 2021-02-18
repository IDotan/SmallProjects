import base64

with open("icon.ico", "rb") as open_icon:
    b64str = base64.b64encode(open_icon.read())
write_data = "img=%s" % b64str
with open("icon.py", "w") as f:
    f.write(write_data)

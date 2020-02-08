from os.path import dirname, join, abspath

close = join(dirname(abspath(__file__)), "close.txt")
with open(close, "w", encoding="utf-8") as f:
    f.write("1")

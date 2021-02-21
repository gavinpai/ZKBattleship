import threading
def a():
    print("hello")
def b():
    input()
thread = threading.Thread(target = input)
thread.start()
a()

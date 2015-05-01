from zmq import Context, PUSH

def set_data(h, var, val):
    c = Context()
    s = c.socket(PUSH)
    s.connect('tcp://cerf:1337')
    s.send_json([h, {var: val}])

def moro(var, val):
    set_data(2, var, val)
def ame(var, val):
    set_data(3, var, val)
def yuki(var, val):
    set_data(4, var, val)

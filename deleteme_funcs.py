GLOBAL_SETTING = False

def myfunc(a, b=2):
    print('a is', a)
    print('b is', b)
    if GLOBAL_SETTING:
        print('global setting is on')

def myfunc2(a, c=3):
    print('a2 is', a)
    print('c is', c)
    if GLOBAL_SETTING:
        print('global setting is on')

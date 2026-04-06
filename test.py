def check(**kwarg):
    print(kwarg.get("a"))
    print(kwarg.keys())
    for key in iter(kwarg.keys()):
        print(key)
check(a = '1',  b=2)

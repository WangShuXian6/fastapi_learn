def fence(func):
    def wrapper():
        print("++++++++++")
        func()
        print("++++++++++")

    return wrapper


@fence
def log():
    print("Decorated")


# log()


def custom_fence(symbol: str = "+"):
    def add_fence(func):
        def wrapper():
            print(symbol * 10)
            func()
            print(symbol * 10)

        return wrapper

    return add_fence


@custom_fence("-")
def log2():
    print("Decorated")


log2()

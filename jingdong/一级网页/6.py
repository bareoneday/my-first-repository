import time

import timeout_decorator


@timeout_decorator.timeout(6)
def justtest():
    time.sleep(5)

    return 5


aaa = justtest()

print (aaa)
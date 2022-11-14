from my_class import Handler


def main():

    path = "notReadNotWrite.txt"
    handler = Handler()
    first = handler.register(path, True, False)
    sen = handler.register(path, False, True)
    third = handler.register(path, True, False)
    fourth = handler.register(path, True, True)
    fifth = handler.register(path, False, False)
    handler.unregister(first)
    handler.unregister(sen)
    handler.unregister(third)
    handler.unregister(fourth)
    handler.unregister(fifth)




if __name__ == '__main__':
    main()

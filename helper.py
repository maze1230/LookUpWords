import lookup as lu


def input_lint():  # Split numbers into list
    return map(int, input().split(','))


def choose_from_list(list_, num=20):  # num -> max number of the item to show
    if len(list_) == 0:
        raise LookupError()
    ret = []
    for idx, item in enumerate(list_):
        if idx >= num:
            break
        print(str(idx) + ": " + str(item))
    print("Choose numbers(separate by ,) : ", end='')
    x = input_lint()
    for i in x:
        ret.append(list_[i])
    return ret


def synonym_api_init():
    try:
        with open("./.synonym_key", mode='x') as f:
            id_ = input("Synonym API ID(OxFordDictionary): ")
            key = input("Synonym API Key                 : ")
            f.writelines(id_ + "\n")
            f.writelines(key + "\n")
    except FileExistsError:
        with open("./.synonym_key") as f:
            line = f.readlines()
            line = [x[:-1] for x in line]
            (id_, key) = (line[0], line[1])
    lu.synonym_API_id = id_
    lu.synonym_API_key = key


def first(item):
    return item[0]

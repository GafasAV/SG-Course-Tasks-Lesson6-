import re
import logging


__author__ = "Andrew Gafiychuk"


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("[+]App started...")

    # True list. RE result must be all word from list
    true_list = ['afoot', 'catfoot', 'dogfoot', 'fanfoot', 'foody',
                 'foolery', 'foolish', 'fooster', 'footage',
                 'foothot', 'footle', 'footpad', 'footway',
                 'hotfoot', 'jawfoot', 'mafoo', 'nonfood',
                 'padfoot', 'prefool', 'sfoot', 'unfool'
                 ]

    # False list. RE result must be 0 word from list
    false_list = ['Atlas', 'Aymoro', 'Iberic', 'Mahran', 'Ormazd',
                  'Silipan', 'altered', 'chandoo', 'crenel',
                  'crooked', 'fardo', 'folksy', 'forest', 'hebamic',
                  'idgah', 'manlike', 'marly', 'palazzo', 'sixfold',
                  'tarrock', 'unfold'
                  ]

    res_list = []
    for el in true_list + false_list:
        res = re.findall(r'(^.*foo.*$)', el)
        res_list.extend(res)

    print(res_list)
    if len(res_list) == len(true_list):
        print(True)

    logging.debug("[+]App done success!")

import re
import logging


__author__ = "Andrew Gafiychuk"


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("[+]App started...")

    # True list. RE result all word from this list
    true_list = ['fu', 'tofu', 'snafu']

    # False list. RE result 0 word from this list
    false_list = ['futz', 'fusillade', 'functional',
                  'discombobulated']

    res_list = []
    for el in true_list + false_list:
        res = re.findall(r'(^.*fu\b)', el)
        res_list.extend(res)

    print(res_list)
    if len(res_list) == len(true_list):
        print(True)

    logging.debug("[+]App done success!")

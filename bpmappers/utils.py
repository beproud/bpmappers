from collections import OrderedDict


def sort_dict_with_keys(target_dict, keys):
    """Sorting target_dict with keys list.

    :return: OrderedDict
    """
    def _key_func(k):
        if k in keys:
            return keys.index(k)
        return -1
    key_order = sorted(target_dict.keys(), key=_key_func)
    ordered = OrderedDict()
    for key in key_order:
        ordered[key] = target_dict[key]
    return ordered

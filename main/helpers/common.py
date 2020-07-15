def without_keys(d, *keys):
     return dict(filter(lambda key_value: key_value[0] not in keys, d.items()))


def only_keys(d, *keys):
     return dict(filter(lambda key_value: key_value[0] in keys, d.items()))


def without_items(l, items= []):
     return list(filter(lambda item: not (item in items), l))
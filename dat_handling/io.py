def load_list_from_txt(fn='./data/categories.csv'):
    """Read a list from a text file.

    :fn: filename to read from.
    :returns: array of values

    """
    with open(fn) as f:
        return [l.replace('\n', '') for l in f]


def inlist(lst, matcher):
    result = [x for x in lst if matcher(x)]
    return len(result) > 0

def take(n, generator):
    i = 0
    result = []
    while i < n:
        result.append(next(generator))
        i = i + 1
    return result

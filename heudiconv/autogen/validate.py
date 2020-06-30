def validate_grouping(seqinfos, threshold=90):
    """
    Performs quick sanity checks to ensure SeqInfos are similar enough

    Returns
    -------
    None

    Raises
    ------
    RuntimeError
        Significant differences found within SeqInfo fields

    """

    field = 'protocol_name'
    if not multi_fuzz_ratio([getattr(s, field) for s in seqinfos], threshold):
        field = 'series_description'
        if not multi_fuzz_ratio([getattr(s, field) for s in seqinfos], threshold):
            raise RuntimeError("Grouped sequences do not have similar enough descriptions")

    sz = {s.dim3 for s in seqinfos}
    st = {s.dim4 for s in seqinfos}
    if len(sz) > 1 or len(st) > 1:
        raise RuntimeError("Grouped sequences have different shapes")
    return field


def get_key_grouping(seqinfos, validate=True):
    """
    Generate heuristic rule for one or more grouped SeqInfos.

    Performs quick sanity checks to ensure SeqInfos are similar enough.

    """
    criteria = {}

    name_field = None
    if validate:
        name_field = validate_grouping(seqinfos)

    if name_field is not None:
        # add name field
        if len(seqinfos) == 1:
            criteria[name_field] = getattr(seqinfos[0], name_field)
        else:
            prev = None
            for i in range(len(seqinfos) - 1):
                curr = largest_substring(
                    getattr(seqinfos[i], name_field),
                    getattr(seqinfos[i+1], name_field)
                )
                if prev is not None and prev != curr:
                    prev = None
                    break
                prev = curr

            if prev is not None:
                criteria[name_field] = prev

    dim3 = {s.dim3 for s in seqinfos}
    if len(dim3) == 1:
        criteria['dim3'] = int(dim3.pop())
    dim4 = {s.dim4 for s in seqinfos}
    if len(dim4) == 1:
        criteria['dim4'] = int(dim4.pop())

    if not criteria:
        raise Exception(f"Could not generate any groupings for SeqInfos:\n{seqinfos}")
    return criteria


def largest_substring(a, b, mtol=None):
    from difflib import SequenceMatcher

    matches = SequenceMatcher(None, a, b).get_matching_blocks()
    l = max(matches, key=lambda m: m.size)

    if mtol is not None:
        assert (l.size / max(len(a), len(b))) > mtol, \
            "Size of match to string ratio is too low"

    ma = a[l.a:l.a + l.size]
    mb = b[l.b:l.b + l.size]
    assert ma == mb
    return ma

def multi_fuzz_ratio(items, threshold):
    """
    Given items of 2 or more elements, ensure all sequential
    ratios are within a given threshold

    """
    from fuzzywuzzy import fuzz
    if len(items) > 1:
        for i in range(len(items), 1):
            if fuzz.ratio(items[i-1], items[i]) < threshold:
                return False
    return True

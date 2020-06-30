def autogenerate_heuristic(seqinfos, session=None, validate=True, out_file=None):
    from ..utils import SeqInfo
    from .validate import get_key_grouping

    keys, outpaths, groupings = [], [], []
    for key, vals in seqinfos.items():
        seqinfos = [SeqInfo(*v) for v in vals]
        keys.append(key.replace('-', '_'))
        outpaths.append(gen_bids_path(key, len(seqinfos), session))
        groupings.append(get_key_grouping(seqinfos, validate))

    return write_heuristic(keys, outpaths, groupings, out_file=out_file)


def gen_bids_path(key, num_seqs, session=None):
    """
    Parameters
    ----------
    key : :obj:`str`
        Scan descriptor for seq grouping (provided by user)
    num_seqs : :obj:`int`
        Number of grouped sequences
    session : :obj:`bool`
        Multi-session scan (adds ``ses`` entity to outpath)

    Returns
    -------
    outpath : :obj:`str`
        Output BIDS path
    """

    entities = key.split('_')
    # the first entity will always tell us what type of scan
    modality, suffix = entities.pop(0).split('-')

    if session is True:
        # TO CONSIDER: Windows support
        outpath = f'{{bids_subject_session_dir}}/{modality}/{{bids_subject_session_prefix}}'
    else:
        outpath = f'sub-{{subject}}/{modality}/sub-{{subject}}'

    for ent in entities:  # additional bids information to insert
        outpath += f'_{ent}'
    if num_seqs > 1:
        outpath += '_run-{item:1d}'

    outpath += f'_{suffix}'
    return outpath


def create_key(template, outtype=("nii.gz",), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return template, outtype, annotation_classes


def write_heuristic(keys, paths, groupings, out_file=None):
    """
    Creates a heuristic file with ``create_key`` and ``infotodict`` methods

    Parameters
    ----------
    keys : list of `str`s
        Unique id for each scan grouping
    paths : list of `str`s
        Target path for each key
    groupings : list of `dict`s
        Criteria for series to be grouped into key
    out_file : `str` or None
        Output file path

    Returns
    -------
    out_file : `str`
        Autogenerated heuristic

    """
    from pathlib import Path
    import inspect

    def ind(s, ln=1):
        "Helper method for indentation"
        return " " * 4 * ln + s

    lines = ['"This heuristic was automatically generated"\n']
    lines += inspect.getsource(create_key).splitlines()
    lines += ['\n', 'def infotodict(seqinfos):',]


    lines.append(ind("# Output paths"))
    for k, p in zip(keys, paths):
        lines.append(ind(f'{k} = create_key("{p}")'))

    lines.append(ind("# Info dictionary"))
    lines.append(ind("info = {"))
    for k in keys:
        lines.append(ind(f"{k}: [],", 2))
    lines.append(ind("}"))

    lines.append(ind("# Scan grouping"))
    lines.append(ind("for s in seqinfo:"))
    for k, group in zip(keys, groupings):
        lines.append(
            ind(_gen_conditional('if' if k == keys[0] else 'elif', group), 2)
        )
        lines.append(
            ind(f'info[{k}].append(s.series_id)', 3)
        )
    lines.append(ind("return seqinfo"))

    if out_file is None:
        out_file = Path('heuristic-auto.py')

    Path(out_file).write_text('\n'.join(lines))
    return str(out_file)


def _gen_conditional(cond, grouping):
    for k, v in grouping.items():
        if k in ('protocol_name', 'series_description'):
            cond += f' "{v}" in s.{k} and'
        else:
            cond += f' s.{k} == {v} and'

    return cond[:-4] + ':'

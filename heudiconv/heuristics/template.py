import os


def create_key(template, outtype=('nii.gz',), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return template, outtype, annotation_classes


def infotodict(seqinfo):
    """Heuristic evaluator for determining which runs belong where

    allowed template fields - follow python string module:

    item: index within category
    subject: participant id
    seqitem: run number during scanning
    subindex: sub index within group

    Each namedtuple in the `seqinfo` list contains the following fields:

    * total_files_till_now
    * example_dcm_file
    * series_id
    * dcm_dir_name
    * unspecified2
    * unspecified3
    * dim1
    * dim2
    * dim3
    * dim4
    * TR
    * TE
    * protocol_name
    * is_motion_corrected
    * is_derived
    * patient_id
    * study_description
    * referring_physician_name
    * series_description
    * image_type
    * accession_number
    * patient_age
    * patient_sex
    * date
    """

    # Define keys

    # Define info

    for s in seqinfo:
        # Define rules
        pass
    return info

BIAS_FIELDS = [

    "name",
    "gender",
    "age",
    "dob",
    "date_of_birth",
    "religion",
    "nationality",
    "marital_status",
    "photo",
    "profile_picture"
]


def remove_bias_fields(resume):

    cleaned = dict(resume)

    for field in BIAS_FIELDS:

        if field in cleaned:

            del cleaned[field]

    return cleaned
from math import fabs


def paginate_queryset(qs, **kwargs):
    max_limit = 10
    count = len(qs)
    limit = kwargs.get("limit", 0)
    # new = kwargs.get("new")

    if not limit:
        raise Exception("limit is required")
    ret = int(limit)

    limit = min(ret, max_limit)

    offset = int(kwargs.get("offset", 0))

    if limit is None:
        return None

    # if offset and new:
    #     date_offset = qs.get(id=offset).date
    #     qs = qs.filter(date__gte=date_offset)
    #     max_qs = len(qs)
    #     if max_qs < 2:
    #         return []
    #     return qs[0:max_qs - 1]
    #
    # if offset:
    #     date_offset = qs.get(id=offset).date
    #     qs = qs.filter(date__lte=date_offset)
    #     return qs[1: fabs(limit) + 1]

    if count == 0 or offset < 0:
        return []
    return qs[offset:offset + limit]


def paginate(qs, **kwargs):
    limit = kwargs.get("limit", None)
    offset = kwargs.get("offset", None)
    # new = kwargs.get("new", False)
    if limit is not None and offset is not None:
        qs = paginate_queryset(qs,
                               limit=limit,
                               offset=offset)
    return qs

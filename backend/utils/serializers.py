from datetime import datetime
from bson import ObjectId


def _serialize_value(v):
    # Convert ObjectId to str, datetimes to ISO, recurse into lists/dicts
    if isinstance(v, ObjectId):
        return str(v)
    if isinstance(v, datetime):
        return v.isoformat()
    if isinstance(v, dict):
        return serialize_doc(v)
    if isinstance(v, list):
        return [_serialize_value(x) for x in v]
    return v


def serialize_doc(doc, exclude_fields=None):
    """Return a new dict with `_id` converted to `id` (string), datetimes
    and ObjectIds stringified and optionally exclude sensitive fields.
    Works recursively for nested dicts/lists.
    """
    if doc is None:
        return None

    exclude_fields = set(exclude_fields or [])

    out = {}
    # If the input is not a dict (e.g., Cursor item converted), try to cast
    try:
        items = list(doc.items())
    except Exception:
        # Fallback for objects that behave like dicts
        if isinstance(doc, dict):
            items = doc.items()
        else:
            return _serialize_value(doc)

    for k, v in items:
        if k in exclude_fields:
            continue
        if k == '_id':
            out['id'] = _serialize_value(v)
            continue
        out[k] = _serialize_value(v)

    return out


def serialize_list(docs, exclude_fields=None):
    return [serialize_doc(d, exclude_fields=exclude_fields) for d in docs]

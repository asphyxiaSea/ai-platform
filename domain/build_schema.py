from pydantic import BaseModel, Field, create_model
from typing import Optional
from typing import Literal, List
import json
import hashlib
import json
import hashlib

_SCHEMA_CACHE: dict[str, type[BaseModel]] = {}

TYPE_MAP = {
    "string": str,
    "number": float,
    "integer": int,
    "boolean": bool,
}

def canonicalize_field(f: dict) -> dict:
    return {
        "name": f["name"],
        "type": f["type"],
        "required": bool(f.get("required", False)),
        "items": f.get("items"),
        "enum": tuple(f["enum"]) if "enum" in f else None,
    }

def canonicalize_fields(fields: list[dict]) -> list[dict]:
    canonical = [canonicalize_field(f) for f in fields]
    return sorted(canonical, key=lambda x: x["name"])

def resolve_type(f: dict):
    t = f["type"]

    # 1️⃣ enum → Literal
    if t == "enum":
        values = f.get("enum")
        if not values:
            raise ValueError("enum field must define enum values")

        first_type = type(values[0])
        if not all(isinstance(v, first_type) for v in values):
            raise ValueError("enum values must be same type")

        return Literal[tuple(values)]

    # 2️⃣ array
    if t == "array":
        item_type = TYPE_MAP.get(f.get("items", "string"), str)
        return List[item_type]

    # 3️⃣ primitive
    return TYPE_MAP.get(t, str)


def schema_identity(
    schema_name: str,
    fields: list[dict],
) -> str:
    payload = {
        "schema_name": schema_name,
        "fields": canonicalize_fields(fields),
    }
    raw = json.dumps(payload, sort_keys=True, ensure_ascii=False)
    return hashlib.md5(raw.encode()).hexdigest()


def build_pydantic_schema(
    schema_name: str,
    fields: list[dict],
) -> type[BaseModel]:

    sid = schema_identity(schema_name, fields)
    model_name = f"{schema_name}_{sid[:8]}"

    if sid in _SCHEMA_CACHE:
        return _SCHEMA_CACHE[sid]

    model_fields = {}

    for f in fields:
        py_type = resolve_type(f)

        if f.get("required", False):
            model_fields[f["name"]] = (
                py_type,
                Field(..., description=f.get("description", ""))
            )
        else:
            model_fields[f["name"]] = (
                Optional[py_type],
                Field(None, description=f.get("description", ""))
            )

    model = create_model(model_name, **model_fields)

    _SCHEMA_CACHE[sid] = model
    return model

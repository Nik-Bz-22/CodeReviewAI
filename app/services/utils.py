from typing import TypeAlias
import hashlib
import json
import re

AVAILABLE_TYPE_TO_HASH:TypeAlias=str|tuple[str]|dict[str,str]

def str_to_sha256(input_data:str) -> str:
    data = input_data.encode()
    hash_object = hashlib.sha256(data)
    sha256_hash = hash_object.hexdigest()
    return sha256_hash

def dict_to_sha256(input_data:dict) -> str:
    json_data = json.dumps(input_data, sort_keys=True)
    sha256_hash = hashlib.sha256(json_data.encode()).hexdigest()
    return sha256_hash

def tuple_to_sha256(input_data:tuple) -> str:
    tuple_bytes = str(input_data).encode('utf-8')
    sha256_hash = hashlib.sha256(tuple_bytes).hexdigest()
    return sha256_hash

def hash_to_sha256(input_data:AVAILABLE_TYPE_TO_HASH) -> str:
    if isinstance(input_data, dict):
        return dict_to_sha256(input_data)
    elif isinstance(input_data, tuple):
        return tuple_to_sha256(input_data)
    elif isinstance(input_data, str):
        return str_to_sha256(input_data)
    else:
        raise TypeError("Invalid data type to be hashed")


def get_unique_review_key(all_data:dict[str, str], prompt:str)->str:
    hashed_repo_content = hash_to_sha256(all_data)
    hashed_prompt = hash_to_sha256(prompt)
    unique_review_key = f"{hashed_prompt}:{hashed_repo_content}"
    return unique_review_key


def extract_json_from_string(s: str) -> str:
    if '{' not in s or '}' not in s:
        raise ValueError("JSON object not found in the string.")

    pattern = r'\{[^{}]*\}'
    match = re.search(pattern, s)

    if match:
        return match.group().replace("\n", "")
    else:
        raise ValueError("JSON object not found in the string.")

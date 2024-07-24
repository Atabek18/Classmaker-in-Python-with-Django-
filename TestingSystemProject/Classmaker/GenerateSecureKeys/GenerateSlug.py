import re
import unicodedata
from django.utils.text import slugify
import uuid
import hashlib
import time
import random
import string


def generate_slugs(text):
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    hash_value = slugify(str(uuid.uuid4()).split('-')[-1])
    return f"{slugify(text)}-{hash_value}"


def generate_secure_slug(input_data=''):
    salt = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))
    timestamp = str(int(time.time()))
    data_with_salt = f"{input_data}{salt}{timestamp}"
    hash_object = hashlib.sha512(data_with_salt.encode())
    hash_value = hash_object.hexdigest()
    upper_case_index = random.randint(0, len(hash_value) - 10)
    hash_value = hash_value[:upper_case_index] + hash_value[upper_case_index:].upper()
    char_list = list(hash_value[:120])
    random.shuffle(char_list)
    shuffled_string = ''.join(char_list)
    part_length = 20
    parts = [shuffled_string[i:i+part_length] for i in range(0, len(shuffled_string), part_length)]
    chosen_part = random.choice(parts)
    return chosen_part

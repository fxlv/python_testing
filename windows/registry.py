from _winreg import *


def get_num_keys(key_name, sub_key):
    key = OpenKey(key_name, sub_key)
    num_keys, num_values, last_modified = QueryInfoKey(key)
    return num_keys

def get_num_values(key_name, sub_key):
    key = OpenKey(key_name, sub_key)
    num_keys, num_values, last_modified = QueryInfoKey(key)
    return num_values

def get_keys(key_name, sub_key):
    keys_list = []
    key = OpenKey(key_name, sub_key)
    num_keys = get_num_keys(key_name, sub_key)
    if num_keys > 0:
        for i in range(num_keys):
            keys_list.append(EnumKey(key, i))
    return keys_list


def get_values(key_name, sub_key):
    values_list = []
    key = OpenKey(key_name, sub_key)
    num_values = get_num_values(key_name, sub_key)
    if num_values > 0:
        for i in range(num_values):
            values_list.append(EnumValue(key, i))
    return values_list

registry_path = "SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList"
print get_keys(HKEY_LOCAL_MACHINE, registry_path)
print get_values(HKEY_LOCAL_MACHINE, registry_path)



import glob
import os

from src.script import utils


def remove_gpg_ext(list_files):
    result = {}
    for key, value in list_files.items():
        new_key = replace_last(key, ".gpg", "")
        result[new_key] = value
    return result


def build_md5_files_map_virtual_remove_gpg_ext(list_files, folder_src):
    list_files = build_md5_files_map_virtual(list_files, folder_src)
    return remove_gpg_ext(list_files)


def calculate_state(folder_path):
    list_files = glob.glob(folder_path + "/**", recursive=True)
    return build_md5_files_map_virtual(list_files, folder_path)


def calculate_state_without_gpg_ext(folder_path):
    list_files = glob.glob(folder_path + "/**", recursive=True)
    return build_md5_files_map_virtual_remove_gpg_ext(list_files, folder_path)


def build_md5_files_map_virtual(list_files, folder_src):
    folder_src = folder_src.replace("*", "")
    result = {}
    for file in list_files:
        file_rel = os.path.relpath(file, folder_src)
        file_rel = "/" + file_rel.replace("\\", "/")  # windows-specific
        if file_rel == "/.":
            continue
        if os.path.isfile(file):
            filemd5 = utils.md5(file)
            result[file_rel] = filemd5
        if os.path.isdir(file):
            file_rel = file_rel + "/"
            md5_from_dir_path = utils.md5_from_string(file_rel)
            result[file_rel] = md5_from_dir_path
    return result


def find_diff_by_key(dict1, dict2):
    return {k: dict1[k] for k in set(dict1) - set(dict2)}


def find_modified_files(dict1, dict2):
    same_names = find_intersection_by_keys(dict1, dict2)

    result = {}
    for key, value in same_names.items():
        if dict1[key] != dict2[key]:
            result.update({key: value})

    return result


def find_not_modified_files(dict1, dict2):
    same_names = find_intersection_by_keys(dict1, dict2)

    result = {}
    for key, value in same_names.items():
        if dict1[key] == dict2[key]:
            result.update({key: value})

    return result


def find_intersection_by_keys(dict1, dict2):
    return {k: dict1[k] for k in set(dict1).intersection(set(dict2))}


def find_added_elements_by_key(dict1, dict2):
    return find_diff_by_key(dict1, dict2)


def find_removed_elements_by_key(dict1, dict2):
    return find_diff_by_key(dict2, dict1)


def replace_last(source_string, replace_what, replace_with):
    head, _sep, tail = source_string.rpartition(replace_what)
    return head + replace_with + tail


def save_state(state_file, current_local_state):
    utils.dict_to_json(state_file, current_local_state)

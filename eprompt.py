import os
import re
import platform
import getpass

import utils as __utils


def get_yn(prompt, default=None, allow_empty=False):
    if default is None and allow_empty:
        default = ''

    inp = None
    while inp not in ['y', 'n']:
        inp = str(input(f"{prompt} [y/n]: ")).strip().lower()
        if not inp and default is not None:
            inp = default
            break

    return inp


def get_value(prompt, allowed_types=[str], default=None, allow_empty=False):
    if default is None and allow_empty:
        default = ''

    while True:
        inp = str(input(f"{prompt}: ")).strip()
        if not inp and default is not None:
            return default

        inp_type = __utils.interpret_type(inp)
        if inp_type in allowed_types:
            return inp_type(inp)
        elif inp and str in allowed_types:
            return inp


def get_values(prompt, delimeter=',', allowed_types=[str], default=None, allow_empty=False):
    if default is None and allow_empty:
        default = ''

    inp = items = None
    while not (inp and items):
        inp = str(input(f"{prompt}: ")).strip()
        if not inp and default is not None:
            return default

        items = [item.strip() for item in inp.split(delimeter) if item.strip()]
        items = __utils.auto_cast(items, allowed_types)
    return items


def match_value(prompt, target, max_attempts=-1):
    target = str(target)
    attempts = 0
    inp = None
    while inp != target and attempts != max_attempts:
        inp = str(input(f"{prompt}: "))
        attempts += 1
    return attempts != max_attempts


def match_values(prompt, targets, max_attempts=-1, delimeter=','):
    targets = [str(v) for v in targets]
    attempts = 0
    inps = []
    while sorted(inps) != sorted(targets) and attempts != max_attempts:
        inps = str(input(f"{prompt}: ")).split(delimeter)
        inps = [v.strip() for v in inps if v]
        attempts += 1
    return attempts != max_attempts


def get_bool(prompt, default=None, allow_empty=False):
    if default is None and allow_empty:
        default = ''

    while True:
        inp = str(input(f"{prompt}: ")).strip()
        if not inp and default is not None:
            return default
        try:
            inp = bool(inp)
            return inp
        except ValueError:
            pass


def get_number(prompt, default=None, allow_empty=False):
    if default is None and allow_empty:
        default = ''

    while True:
        inp = str(input(f"{prompt}: ")).strip()
        if not inp and default is not None:
            return default
        cast = float if '.' in inp else int
        try:
            inp = cast(inp)
            return inp
        except ValueError:
            pass


def get_int(prompt, default=None, allow_empty=False):
    if default is None and allow_empty:
        default = ''

    while True:
        inp = str(input(f"{prompt}: ")).strip()
        if not inp and default is not None:
            return default
        try:
            inp = int(inp)
            return inp
        except ValueError:
            pass


def get_float(prompt, default=None, allow_empty=False):
    if default is None and allow_empty:
        default = ''

    while True:
        inp = str(input(f"{prompt}: ")).strip()
        if not inp and default is not None:
            return default
        try:
            inp = float(inp)
            return inp
        except ValueError:
            pass


def get_char(prompt, default=None, allow_empty=False):
    if default is None and allow_empty:
        default = ''

    inp = ''
    while not __utils.ischar(inp):
        inp = str(input(f"{prompt}: "))
        if not inp and default is not None:
            return default
    return inp


def get_str(prompt, default=None, allow_empty=False):
    if default is None and allow_empty:
        default = ''

    inp = ''
    while not inp:
        inp = str(input(f"{prompt}: "))
        if not inp and default is not None:
            return default
    return inp


def get_alpha(prompt, default=None, allow_empty=False):
    if default is None and allow_empty:
        default = ''

    inp = ''
    while not inp.isalpha():
        inp = str(input(f"{prompt}: ")).strip()
        if not inp and default is not None:
            return default
    return inp


def get_alphanumeric(prompt, default=None, allow_empty=False):
    if default is None and allow_empty:
        default = ''

    inp = ''
    while not inp.isalnum():
        inp = str(input(f"{prompt}: ")).strip()
        if not inp and default is not None:
            return default
    return inp


def get_line(prompt, default=None, allow_empty=False):
    if default is None and allow_empty:
        default = ''

    inp = None
    while not inp:
        inp = str(input(f"{prompt}: ")).strip()
        if not inp and default is not None:
            return default
    return inp


def get_lines(prompt, allow_empty=True):
    print(f"{prompt}: ")
    lines = []
    while True:
        try:
            l = input()
            l = str(l).strip()
            lines.append(l)
        except EOFError:
            if not allow_empty:
                lines = list(filter(None, lines))
            return lines


def get_selection(menu_options, header="menu", prompt="enter selection", default=None, allow_empty=False):
    if default is None and allow_empty:
        default = ''

    if header:
        print(header)
    for key, value in menu_options.items():
        print(f"\t[{key}]: {value}")
    print()

    key = None
    while key not in menu_options.keys():
        key = str(input(f"{prompt}> ")).strip()
        if not key and default is not None:
            if default in menu_options.keys():
                return default, menu_options[default]
            else:
                return default, None
    return key, menu_options[key]


def get_email(prompt, default=None, allow_empty=False):
    if default is None and allow_empty:
        default = ''

    email = None
    while not email:
        inp = str(input(f"{prompt}: ")).strip()
        if not inp and default is not None:
            return default
        email = re.match(r"^[^@]+@[^@]+\.[^@]+$", inp)
    return email.group()


def get_pwd(prompt, default=None, allow_empty=False):
    if default is None and allow_empty:
        default = ''

    pwd = None
    while not pwd:
        pwd = getpass.getpass(prompt=f"{prompt}: ")
        if not pwd and default is not None:
            return default
    return pwd


def match_pwd(prompt, target, max_attempts=-1):
    target = str(target)
    attempts = 0
    pwd = None
    while pwd != target and attempts != max_attempts:
        pwd = getpass.getpass(prompt=f"{prompt}: ")
        attempts += 1
    return attempts != max_attempts


def get_regex(prompt, r, flags, default=None, allow_empty=False):
    if default is None and allow_empty:
        default = ''

    match = None
    while not match:
        inp = str(input(f"{prompt}: "))
        if not inp and default is not None:
            return default
        match = re.match(r, inp, flags=flags)
    return match


def wait_for_key_press(key, prompt="press \'{}\' to continue..."):
    prompt = prompt.format(key)
    inp = None
    while inp != key:
        inp = str(input(f"{prompt}: "))


def wait_for_some_key_press(keys, prompt="press \'{}\' to continue..."):
    prompt = prompt.format(keys)
    inp = None
    while inp not in keys:
        inp = str(input(f"{prompt}: "))


def wait_for_any_key_press(prompt="press any key to continue..."):
    if platform.system() == "Windows":
        print(prompt)
        os.system("pause")
    else:
        os.system(f"read -s -n 1 -p \"{prompt}\"")


def wait_for_enter(prompt="press ENTER to continue..."):
    input(prompt)
#!/usr/bin/python

DOCUMENTATION = '''
---
module: to_toml, from_toml
version_added: "2.8"
short_description: Converts Python data to TOML and TOML to Python data.
author:
    - "Samy Coenen (contact@samycoenen.be)"
'''

import datetime
import sys
from collections import OrderedDict
#pip3 install python-toml

def to_toml(data):
    ''' Convert the value to TOML '''
    return dumps(data)

def from_toml(data):
    ''' Convert TOML to Python data '''
    return loads(data)

class FilterModule(object):
    ''' Ansible TOML jinja2 filters '''

    def filters(self):
        return {
            # toml
            'to_toml': to_toml,
            'from_toml': from_toml
        }

def loads(s, *args, **kwargs):
    if not isinstance(s, basestring):
        raise TypeError("It's not a string.")

    try:
        s = s.decode('utf-8')
    except AttributeError:
        pass

    s = _clear_r_n_t(s)

    return _loads(s)


def load(file, *args, **kwargs):
    return loads(_read(file, *args, **kwargs))


def dumps(s, *args, **kwargs):
    if not isinstance(s, dict):
        raise TypeError("It's not a dict.")

    return un_utf_8(_json_transition_str(s))


def dump(file, s, *args, **kwargs):
    _write(file, dumps(s))


def _clear_r_n_t(v):
    return v.replace('\r', '').replace('\t', '').split('\n')


def _clear_empty_l_r(v):
    return v.rstrip(' ').lstrip(' ')


def _clear_empty(v):
    return v.replace(' ', '')


def _is_empty(v):
    return v[0] if v else v


def _get_key(v):
    key = _re('\[\[(.*?)\]\]', v)
    if key:
        return key, True

    return _re('\[(.*?)\]', v), False


def _loads(s):
    items, nd, it, fg = ordict(), ordict(), [], False
    key_status = False

    for v in s:
        if not v or _is_empty(_clear_empty(v)) == '#':
            continue

        if '[' == _is_empty(_clear_empty(v)) and ']' in v:
            key, key_status = _get_key(v)
            nd = ordict()
        else:
            _it = v.split('=')
            _it[0] = _clear_empty(_is_empty(_it))

            """
                arr_arr = [
                    'zbc',
                    'sdf',
                ]
            """
            try:
                if '[' not in _it[0] and _it[0][-1] == ']':
                    it.append(_it[0])
                    fg = False
                elif _it[1].replace(' ', '')[0] == '[' and ']' not in _it[1]:
                    it.append(_it[0])
                    fg = True
            except Exception as e:
                pass

            if fg:
                it.append(_it[1] if len(_it) > 1 else _it[0])
            elif not fg and it:
                _it = [it[0], ''.join(it[1:])]
                it = []

            nd.update(_str_transition_json(_it))

        ite = items

        try:
            # [1][:-1] = []
            for k in key[:-1]:
                try:
                    ite = ite[k]
                except Exception as e:
                    ite[k] = ordict()
                    ite = ite[k]

            if isinstance(ite, list):
                ite = ite[-1]

            try:
                ite[key[-1]]
                if key_status:
                    ite[key[-1]].append(nd)
            except Exception as e:
                ite[key[-1]] = [nd] if key_status else nd
            finally:
                key_status = False

        except Exception as e:
            ite.update(nd)
            pass

    return items


def _str_transition_json(v):
    item = ordict()
    if not isinstance(v, (list, tuple)):
        raise TypeError("It's not a list/tuple.")

    if (len(v) == 2):
            item[v[0]] = _str_transition_obj(_clear_empty_l_r(v[1]))
    elif (len(v) > 2):
        item[v[0]] = _str_transition_obj(_clear_empty_l_r('='.join(v[1:])))

    return item


def _str_transition_obj(v):
    if not isinstance(v, basestring):
        raise TypeError("It's not a string")

    if v.lower() == 'true':
        return True
    elif v.lower() == 'false':
        return False

    try:
        if _re('\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z', v):
            return str_to_datetime(v)
    except Exception as e:
        raise e

    try:
        _veal = eval(v.replace(',', ', '))
        if isinstance(_veal, basestring):
            return escape(_veal)
        return _veal
    except SyntaxError as e:
        pass

    return v


def _json_transition_str(s, _k='', index=0):
    _s = ''
    for k, v in s.items():
        _k = _k.rstrip('.') + '.' if _k else ''
        if isinstance(v, dict):
            _s += '\n' + '\t' * index + '[{}]\n'.format(_k + k)
            _s += _json_transition_str(v, _k + k, index=index + 1)

        elif isinstance(v, list) and isinstance(v[0], dict):
            for _v in v:
                _s += '\n' + '\t' * index + '[[{}]]\n'.format(_k + k)
                _s += _json_transition_str(_v, _k + k, index=index + 1)

        elif not isinstance(v, dict):
            _s += '\t' * index + _key_equal_value(k, v)
        else:
            _s += '\n'
    return _s


def _key_equal_value(k, v):
    if isinstance(v, datetime.datetime):
        v = datetime_to_str(v)
    elif isinstance(v, bool):
        v = str(v).lower()
    elif not isinstance(v, basestring):
        v = str(v)
    else:
        v = '"' + str(v) + '"'
    return k + ' = ' + _utf_8(v) + '\n'

def _read(file, *args, **kwargs):
    if PY3:
        with open(file, encoding='utf-8', *args, **kwargs) as fp:
            v = fp.read()
    else:
        with open(file, *args, **kwargs) as fp:
            v = fp.read()
    return v


def _write(file, text, model='w', *args, **kwargs):
    if PY3:
        with open(file, model, encoding='utf-8', *args, **kwargs) as fp:
            fp.write(text)
    else:
        with open(file, model, *args, **kwargs) as fp:
            fp.write(text)


def _re(reg, text):
    reg = re.findall(re.compile(reg), text)
    reg = reg[0].split('.') if reg else []
    return reg


def escape(v):
    if not isinstance(v, basestring):
        return v

    return v.replace(
        '\\', '\\\\').replace(
        '\b', '\\b').replace(
        '\t', '\\t').replace(
        '\f', '\\f').replace(
        '\r', '\\r').replace(
        '\"', '\\"').replace(
        '\/', '\\/').replace(
        '\n', '\\n')


def escape_u(v):
    if not isinstance(v, basestring):
        return v

    # v = escape(v)
    v = v.encode('unicode-escape').decode()

    if PY2:
        return v.replace('\\x', '\\u00')
    return v


def unescape_u(v):
    if not isinstance(v, basestring):
        return v
    v = unescape(v)

    return v.encode().decode('unicode-escape')


def _utf_8(v):
    if PY2:
        return v.decode('utf-8')
    return v


def un_utf_8(v):
    if PY2:
        return v.encode('utf-8')
    return v


def str_to_datetime(dtstr, strftime='%Y-%m-%dT%H:%M:%SZ'):
    if not isinstance(dtstr, basestring):
        raise TypeError("It's not a string.")

    return datetime.datetime.strptime(dtstr, strftime)


def datetime_to_str(dttime, strftime='%Y-%m-%dT%H:%M:%SZ'):
    if not isinstance(dttime, datetime.datetime):
        raise TypeError("It's not a datetime.")

    return dttime.strftime(strftime)

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

PY35 = sys.version_info[:2] == (3, 5)
PY36 = sys.version_info[:2] == (3, 6)

if PY3:
    basestring = str,
    integer_types = int,
    unicode = str
    unichr = chr
    _range = range
else:
    integer_types = (int, long)
    _range = xrange


def ordict():
    return {} if PY36 else OrderedDict()

if __name__ == '__main__':
    pass
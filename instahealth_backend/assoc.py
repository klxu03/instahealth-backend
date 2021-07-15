from flask import current_app

_assoc_dict = None

def get_assoc_dict():
    global _assoc_dict
    if _assoc_dict is None:
        assoc_dict = {}
        with current_app.open_resource("assoc.txt") as file:
            for line in file.read().decode("utf-8").splitlines():
                tag, _, rest = line.partition(" ")
                for word in line.split(", "):
                    if word not in assoc_dict:
                        assoc_dict[word] = set()
                    assoc_dict[word].add(tag)
        _assoc_dict = assoc_dict
    return _assoc_dict

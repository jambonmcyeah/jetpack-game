# Ugly module to generate docstrings to save me the pain, works surprisingly well
# Please don't judge the code as this is not part of the game
import re
import types
import inspect
import importlib
import pygame


def gen_docstrings(module):
    docstring = ""

    for name, value in inspect.getmembers(module):
        if inspect.isclass(value):
            string = " ".join(map(str.lower, re.sub('(?!^)([A-Z][a-z]+)', r' \1', name).split()))
            if "sprite" not in string and issubclass(value, pygame.sprite.Sprite):
                string += " sprite"
            docstring += "A class representing %s" % string + "s"
            if not (len(value.__bases__) == 1 and value.__bases__[0] == object):
                docstring += ", inherits from " + ", ".join(map(lambda x: x.__name__, value.__bases__)) + "\n"
            for member_name, member in value.__dict__.items():
                if type(member) == property:
                    docstring += "Getter for the %s attribute of this %s" % (
                    member_name.replace("_" + name + "__", ""), name) + "\n"
                    if member.fset is not None:
                        docstring += "Setter for the %s attribute of this %s" % (
                        member_name.replace("_" + name + "__", ""), name) + "\n"
                if member_name == "__init__":
                    docstring += "Initializer for the %s class" % name + "\n"
                elif isinstance(member, types.FunctionType):
                    docstring += "%s method for this %s" % (member_name.replace("_" + name + "__", ""), name) + "\n"

            docstring += "\n"

    return docstring


module = importlib.import_module(input())

print(gen_docstrings(module))

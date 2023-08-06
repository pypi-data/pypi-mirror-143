"""
These elements are used by the translator to construct the model from the
interpreted results. It is technically possible to use these functions to
build a model from scratch. But - it would be rather error prone.

This is code to assemble a pysd model once all of the elements have
been translated from their native language into python compatible syntax.
There should be nothing here that has to know about either vensim or
xmile specific syntax.
"""

import re
import os.path
import textwrap
import warnings
from io import open
import black
import json

from . import utils

from pysd._version import __version__


class Imports():
    """
    Class to save the imported modules information for intelligent import
    """
    _numpy, _xarray, _subs = False, False, False
    _functions, _statefuls, _external, _data, _utils =\
        set(), set(), set(), set(), set()
    _external_libs = {"numpy": "np", "xarray": "xr"}
    _internal_libs = [
        "functions", "statefuls", "external", "data", "utils"]

    @classmethod
    def add(cls, module, function=None):
        """
        Add a function from module.

        Parameters
        ----------
        module: str
          module name.

        function: str or None
          function name. If None module will be set to true.

        """
        if function:
            getattr(cls, f"_{module}").add(function)
        else:
            setattr(cls, f"_{module}", True)

    @classmethod
    def get_header(cls, outfile):
        """
        Returns the importing information to print in the model file

        Parameters
        ----------
        outfile: str
            Name of the outfile to print in the header.

        Returns
        -------
        text: str
            Header of the translated model file.

        """
        text =\
            f'"""\nPython model \'{outfile}\'\nTranslated using PySD\n"""\n\n'

        text += "from pathlib import Path\n"

        for module, shortname in cls._external_libs.items():
            if getattr(cls, f"_{module}"):
                text += f"import {module} as {shortname}\n"

        text += "\n"

        for module in cls._internal_libs:
            if getattr(cls, f"_{module}"):
                text += "from pysd.py_backend.%(module)s import %(methods)s\n"\
                        % {
                            "module": module,
                            "methods": ", ".join(getattr(cls, f"_{module}"))}

        if cls._subs:
            text += "from pysd import subs\n"

        cls.reset()

        return text

    @classmethod
    def reset(cls):
        """
        Reset the imported modules
        """
        cls._numpy, cls._xarray, cls._subs = False, False, False
        cls._functions, cls._statefuls, cls._external, cls._data,\
            cls._utils = set(), set(), set(), set(), set()


# Variable to save identifiers of external objects
build_names = set()


def build_modular_model(elements, subscript_dict, namespace, dependencies,
                        main_filename, elements_per_view):

    """
    This is equivalent to the build function, but is used when the
    split_views parameter is set to True in the read_vensim function.
    The main python model file will be named as the original model file,
    and stored in the same folder. The modules will be stored in a separate
    folder named modules + original_model_name. Three extra json files will
    be generated, containing the namespace, subscripts_dict and the module
    names plus the variables included in each module, respectively.

    Setting split_views=True is recommended for large models with many
    different views.

    Parameters
    ----------
    elements: list
        Each element is a dictionary, with the various components needed
        to assemble a model component in python syntax. This will contain
        multiple entries for elements that have multiple definitions in
        the original file, and which need to be combined.

    subscript_dict: dict
        A dictionary containing the names of subscript families (dimensions)
        as keys, and a list of the possible positions within that dimension
        for each value.

    namespace: dict
        Translation from original model element names (keys) to python safe
        function identifiers (values).

    main_filename: str
        The name of the file to write the main module of the model to.

    elements_per_view: dict
        Contains the names of the modules and submodules as keys and the
        variables in each specific module inside a list as values.

    """
    root_dir = os.path.dirname(main_filename)
    model_name = os.path.basename(main_filename).split(".")[0]
    modules_dir = os.path.join(root_dir, "modules_" + model_name)
    # create modules directory if it does not exist
    os.makedirs(modules_dir, exist_ok=True)

    def process_views_tree(view_name,
                           view_content,
                           working_directory,
                           processed_elements):
        """
        Creates a directory tree based on the elements_per_view dictionary.
        If it's the final view, it creates a file, if not, it creates a folder.
        """
        if isinstance(view_content, list):  # will become a module
            subview_elems = []
            for element in elements:
                if element.get("py_name") in view_content or \
                   element.get("parent_name") in view_content:
                    subview_elems.append(element)

            _build_separate_module(subview_elems, subscript_dict,
                                   view_name, working_directory)
            processed_elements += subview_elems

        else:  # the current view has subviews
            working_directory = os.path.join(working_directory, view_name)
            os.makedirs(working_directory, exist_ok=True)

            for subview_name, subview_content in view_content.items():
                process_views_tree(subview_name,
                                   subview_content,
                                   working_directory,
                                   processed_elements)

    processed_elements = []
    for view_name, view_content in elements_per_view.items():
        process_views_tree(view_name,
                           view_content,
                           modules_dir,
                           processed_elements)

    # the unprocessed will go in the main file
    unprocessed_elements = [
        element for element in elements if element not in processed_elements
    ]

    # building main file using the build function
    _build_main_module(unprocessed_elements, subscript_dict, main_filename)

    # create json file for the modules and corresponding model elements
    with open(os.path.join(modules_dir, "_modules.json"), "w") as outfile:
        json.dump(elements_per_view, outfile, indent=4, sort_keys=True)

    # create single namespace in a separate json file
    with open(
        os.path.join(root_dir, "_namespace_" + model_name + ".json"), "w"
    ) as outfile:
        json.dump(namespace, outfile, indent=4, sort_keys=True)

    # create single subscript_dict in a separate json file
    with open(
        os.path.join(root_dir, "_subscripts_" + model_name + ".json"), "w"
    ) as outfile:
        json.dump(subscript_dict, outfile, indent=4, sort_keys=True)

    # create single subscript_dict in a separate json file
    with open(
        os.path.join(root_dir, "_dependencies_" + model_name + ".json"), "w"
    ) as outfile:
        json.dump(dependencies, outfile, indent=4, sort_keys=True)


def _build_main_module(elements, subscript_dict, file_name):
    """
    Constructs and writes the python representation of the main model
    module, when the split_views=True in the read_vensim function.

    Parameters
    ----------
    elements: list
        Elements belonging to the main module. Ideally, there should only be
        the initial_time, final_time, saveper and time_step, functions, though
        there might be others in some situations. Each element is a
        dictionary, with the various components needed to assemble a model
        component in python syntax. This will contain multiple entries for
        elements that have multiple definitions in the original file, and
        which need to be combined.

    subscript_dict: dict
        A dictionary containing the names of subscript families (dimensions)
        as keys, and a list of the possible positions within that dimension
        for each value.

    file_name: str
        Path of the file where the main module will be stored.

    Returns
    -------
    None or text: None or str
        If file_name="return" it will return the content of the output file
        instead of saving it. It is used for testing.

    """
    # separating between control variables and rest of variables
    control_vars, funcs = _build_variables(elements, subscript_dict)

    Imports.add("utils", "load_model_data")
    Imports.add("utils", "load_modules")

    # import of needed functions and packages
    text = Imports.get_header(os.path.basename(file_name))

    # import namespace from json file
    text += textwrap.dedent("""
    __pysd_version__ = '%(version)s'

    __data = {
        'scope': None,
        'time': lambda: 0
    }

    _root = Path(__file__).parent

    _namespace, _subscript_dict, _dependencies, _modules = load_model_data(
        _root, "%(outfile)s")
    """ % {
        "outfile": os.path.basename(file_name).split(".")[0],
        "version": __version__
    })

    text += _get_control_vars(control_vars)

    text += textwrap.dedent("""
        # load modules from modules_%(outfile)s directory
        exec(load_modules("modules_%(outfile)s", _modules, _root, []))

        """ % {
            "outfile": os.path.basename(file_name).split(".")[0],
        })

    text += funcs
    text = black.format_file_contents(text, fast=True, mode=black.FileMode())

    # Needed for various sessions
    build_names.clear()

    with open(file_name, "w", encoding="UTF-8") as out:
        out.write(text)


def _build_separate_module(elements, subscript_dict, module_name, module_dir):
    """
    Constructs and writes the python representation of a specific model
    module, when the split_views=True in the read_vensim function

    Parameters
    ----------
    elements: list
        Elements belonging to the module module_name. Each element is a
        dictionary, with the various components needed to assemble a model
        component in python syntax. This will contain multiple entries for
        elements that have multiple definitions in the original file, and
        which need to be combined.

    subscript_dict: dict
        A dictionary containing the names of subscript families (dimensions)
        as keys, and a list of the possible positions within that dimension
        for each value.

    module_name: str
        Name of the module

    module_dir: str
        Path of the directory where module files will be stored.

    Returns
    -------
    None

    """
    text = textwrap.dedent('''
    """
    Module %(module_name)s
    Translated using PySD version %(version)s
    """
    ''' % {
        "module_name": module_name,
        "version": __version__,
    })
    funcs = _generate_functions(elements, subscript_dict)
    text += funcs
    text = black.format_file_contents(text, fast=True, mode=black.FileMode())

    outfile_name = os.path.join(module_dir, module_name + ".py")

    with open(outfile_name, "w", encoding="UTF-8") as out:
        out.write(text)


def build(elements, subscript_dict, namespace, dependencies, outfile_name):
    """
    Constructs and writes the python representation of the model, when the
    the split_modules is set to False in the read_vensim function. The entire
    model is put in a single python file.

    Parameters
    ----------
    elements: list
        Each element is a dictionary, with the various components needed to
        assemble a model component in python syntax. This will contain
        multiple entries for elements that have multiple definitions in the
        original file, and which need to be combined.

    subscript_dict: dict
        A dictionary containing the names of subscript families (dimensions)
        as keys, and a list of the possible positions within that dimension
        for each value.

    namespace: dict
        Translation from original model element names (keys) to python safe
        function identifiers (values).

    dependencies: dict
        Dependencies dictionary. Variables as keys and set of called values or
        objects, objects as keys and a dictionary of dependencies for
        initialization and dependencies for run.

    outfile_name: str
        The name of the file to write the model to.

    Returns
    -------
    None or text: None or str
        If outfile_name="return" it will return the content of the output file
        instead of saving it. It is used for testing.

    """
    # separating between control variables and rest of variables
    control_vars, funcs = _build_variables(elements, subscript_dict)

    text = Imports.get_header(os.path.basename(outfile_name))

    text += textwrap.dedent("""
    __pysd_version__ = '%(version)s'

    __data = {
        'scope': None,
        'time': lambda: 0
    }

    _root = Path(__file__).parent

    _subscript_dict = %(subscript_dict)s

    _namespace = %(namespace)s

    _dependencies = %(dependencies)s
    """ % {
        "subscript_dict": repr(subscript_dict),
        "namespace": repr(namespace),
        "dependencies": repr(dependencies),
        "version": __version__,
    })

    text += _get_control_vars(control_vars) + funcs
    text = black.format_file_contents(text, fast=True, mode=black.FileMode())

    # Needed for various sessions
    build_names.clear()

    # this is used for testing
    if outfile_name == "return":
        return text

    with open(outfile_name, "w", encoding="UTF-8") as out:
        out.write(text)


def _generate_functions(elements, subscript_dict):
    """
    Builds all model elements as functions in string format.
    NOTE: this function calls the build_element function, which updates the
    import_modules.
    Therefore, it needs to be executed before the_generate_automatic_imports
    function.

    Parameters
    ----------
    elements: dict
        Each element is a dictionary, with the various components needed to
        assemble a model component in python syntax. This will contain
        multiple entries for elements that have multiple definitions in the
        original file, and which need to be combined.

    subscript_dict: dict
        A dictionary containing the names of subscript families (dimensions)
        as keys, and a list of the possible positions within that dimension
        for each value.

    Returns
    -------
    funcs: str
        String containing all formated model functions

    """
    functions = [build_element(element, subscript_dict) for element in
                 elements]

    funcs = "%(functions)s" % {"functions": "\n".join(functions)}
    funcs = funcs.replace("\t", "    ")

    return funcs


def _get_control_vars(control_vars):
    """
    Create the section of control variables

    Parameters
    ----------
    control_vars: str
        Functions to define control variables.

    Returns
    -------
    text: str
        Control variables section and header of model variables section.

    """
    text = textwrap.dedent("""
    ##########################################################################
    #                            CONTROL VARIABLES                           #
    ##########################################################################
    %(control_vars_dict)s
    def _init_outer_references(data):
        for key in data:
            __data[key] = data[key]


    def time():
        return __data['time']()

    """ % {"control_vars_dict": control_vars[0]})

    text += control_vars[1]

    text += textwrap.dedent("""
    ##########################################################################
    #                             MODEL VARIABLES                            #
    ##########################################################################
    """)

    return text


def _build_variables(elements, subscript_dict):
    """
    Build model variables (functions) and separate then in control variables
    and regular variables.

    Parameters
    ----------
    elements: list
        Model elements.

    subscript_dict:

    Returns
    -------
    control_vars, regular_vars: tuple, str
        control_vars is a tuple of length 2. First element is the dictionary
        of original control vars. Second is the string to add the control
        variables' functions. regular_vars is the string to add the regular
        variables' functions.

    """
    # returns of the control variables
    control_vars_dict = {
        "initial_time": ["__data['time'].initial_time()"],
        "final_time": ["__data['time'].final_time()"],
        "time_step": ["__data['time'].time_step()"],
        "saveper": ["__data['time'].saveper()"]
    }
    regular_vars = []
    control_vars = []

    for element in elements:
        if element["py_name"] in control_vars_dict:
            # change the return expression in the element and update the dict
            # with the original expression
            control_vars_dict[element["py_name"]], element["py_expr"] =\
                element["py_expr"][0], control_vars_dict[element["py_name"]]
            control_vars.append(element)
        else:
            regular_vars.append(element)

    if len(control_vars) == 0:
        # macro objects, no control variables
        control_vars_dict = ""
    else:
        control_vars_dict = """
    _control_vars = {
        "initial_time": lambda: %(initial_time)s,
        "final_time": lambda: %(final_time)s,
        "time_step": lambda: %(time_step)s,
        "saveper": lambda: %(saveper)s
    }
    """ % control_vars_dict

    return (control_vars_dict,
            _generate_functions(control_vars, subscript_dict)),\
        _generate_functions(regular_vars, subscript_dict)


def build_element(element, subscript_dict):
    """
    Returns a string that has processed a single element dictionary.

    Parameters
    ----------
    element: dict
        A dictionary containing at least the elements:
        - kind: ['constant', 'setup', 'component', 'lookup']
            Different types of elements will be built differently
        - py_expr: str
            An expression that has been converted already into python syntax
        - subs: list of lists
            Each sublist contains coordinates for initialization of a
            particular part of a subscripted function, the list of
            subscripts vensim attaches to an equation

    subscript_dict: dict
        A dictionary containing the names of subscript families (dimensions)
        as keys, and a list of the possible positions within that dimension
        for each value.

    Returns
    -------
    func: str
        The function to write in the model file.

    """
    # check the elements with ADD in their name
    # as these wones are directly added to the
    # external objecets via .add method
    py_expr_no_ADD = ["ADD" not in py_expr for py_expr in element["py_expr"]]

    if element["kind"] == "dependencies":
        # element only used to update dependencies
        return ""
    elif sum(py_expr_no_ADD) > 1 and element["kind"] not in [
        "stateful",
        "external",
        "external_add",
    ]:
        py_expr_i = []
        # need to append true to the end as the next element is checked
        py_expr_no_ADD.append(True)
        for i, (py_expr, subs_i) in enumerate(zip(element["py_expr"],
                                                  element["subs"])):
            if not (py_expr.startswith("xr.") or py_expr.startswith("_ext_")):
                # rearrange if it doesn't come from external or xarray
                coords = utils.make_coord_dict(
                    subs_i,
                    subscript_dict,
                    terse=False)
                coords = {
                    new_dim: coords[dim]
                    for new_dim, dim in zip(element["merge_subs"], coords)
                }
                dims = list(coords)
                Imports.add("utils", "rearrange")
                py_expr_i.append("rearrange(%s, %s, %s)" % (
                    py_expr, dims, coords))
            elif py_expr_no_ADD[i]:
                # element comes from external or xarray
                py_expr_i.append(py_expr)
        Imports.add("utils", "xrmerge")
        py_expr = "xrmerge(%s)" % (
            ",\n".join(py_expr_i))
    else:
        py_expr = element["py_expr"][0]

    contents = "return %s" % py_expr

    element["subs_dec"] = ""
    element["subs_doc"] = "None"

    if element["merge_subs"]:
        # We add the list of the subs to the __doc__ of the function
        # this will give more information to the user and make possible
        # to rewrite subscripted values with model.run(params=X) or
        # model.run(initial_condition=(n,x))
        element["subs_doc"] = "%s" % element["merge_subs"]
        if element["kind"] in ["component", "setup", "constant",
                               "component_ext_data", "data"]:
            # the decorator is not always necessary as the objects
            # defined as xarrays in the model will have the right
            # dimensions always, we should try to reduce to the
            # maximum when we use it
            # re arrange the python object
            element["subs_dec"] =\
                "@subs(%s, _subscript_dict)" % element["merge_subs"]
            Imports.add("subs")

    indent = 8
    element.update(
        {
            "ulines": "-" * len(element["real_name"]),
            "contents": contents.replace("\n", "\n" + " " * indent),
        }
    )
    # indent lines 2 onward

    # convert newline indicator and add expected level of indentation
    element["doc"] = element["doc"].replace("\\", "\n").replace("\n", "\n    ")

    if element["kind"] in ["stateful", "external", "tab_data"]:
        func = """
    %(py_name)s = %(py_expr)s
            """ % {
            "py_name": element["py_name"],
            "py_expr": element["py_expr"][0],
        }

    elif element["kind"] == "external_add":
        # external expressions to be added with .add method
        # remove the ADD from the end
        py_name = element["py_name"].split("ADD")[0]
        func = """
    %(py_name)s%(py_expr)s
            """ % {
            "py_name": py_name,
            "py_expr": element["py_expr"][0],
        }

    else:
        sep = "\n" + " " * 10
        if len(element["eqn"]) == 1:
            # Original equation in the same line
            element["eqn"] = element["eqn"][0]
        elif len(element["eqn"]) > 5:
            # First and last original equations separated by vertical dots
            element["eqn"] = (
                sep + element["eqn"][0] + (sep + "  .") * 3 + sep
                    + element["eqn"][-1]
            )
        else:
            # From 2 to 5 equations in different lines
            element["eqn"] = sep + sep.join(element["eqn"])

        func = (
            '''
    %(subs_dec)s
    def %(py_name)s(%(arguments)s):
        """
        Real Name: %(real_name)s
        Original Eqn: %(eqn)s
        Units: %(unit)s
        Limits: %(lims)s
        Type: %(kind)s
        Subs: %(subs_doc)s

        %(doc)s
        """
        %(contents)s
        '''
            % element
        )

    return textwrap.dedent(func)


def merge_partial_elements(element_list):
    """
    Merges model elements which collectively all define the model component,
    mostly for multidimensional subscripts

    Parameters
    ----------
    element_list: list
        List of all the elements.

    Returns
    -------
    list:
        List of merged elements.

    """
    outs = dict()  # output data structure

    for element in element_list:
        name = element["py_name"]
        if name not in outs:
            # Use 'expr' for Vensim models, and 'eqn' for Xmile
            # (This makes the Vensim equation prettier.)
            eqn = element["expr"] if "expr" in element else element["eqn"]
            parent_name = element["parent_name"] if "parent_name" in element\
                else None
            outs[name] = {
                "py_name": element["py_name"],
                "real_name": element["real_name"],
                "doc": element["doc"],
                "py_expr": [element["py_expr"]],  # in a list
                "unit": element["unit"],
                "subs": [element["subs"]],
                "merge_subs": element["merge_subs"]
                if "merge_subs" in element else None,
                "dependencies": element["dependencies"]
                if "dependencies" in element else None,
                "lims": element["lims"],
                "eqn": [eqn.replace(r"\ ", "")],
                "parent_name": parent_name,
                "kind": element["kind"],
                "arguments": element["arguments"],
            }

        else:
            eqn = element["expr"] if "expr" in element else element["eqn"]

            outs[name]["doc"] = outs[name]["doc"] or element["doc"]
            outs[name]["unit"] = outs[name]["unit"] or element["unit"]
            outs[name]["lims"] = outs[name]["lims"] or element["lims"]
            outs[name]["eqn"] += [eqn.replace(r"\ ", "")]
            outs[name]["py_expr"] += [element["py_expr"]]
            outs[name]["subs"] += [element["subs"]]
            if outs[name]["dependencies"] is not None:
                if name.startswith("_"):
                    # stateful object merge initial and step
                    for target in outs[name]["dependencies"]:
                        _merge_dependencies(
                            outs[name]["dependencies"][target],
                            element["dependencies"][target])
                else:
                    # regular element
                    _merge_dependencies(
                        outs[name]["dependencies"],
                        element["dependencies"])
            outs[name]["arguments"] = element["arguments"]

    return list(outs.values())


def _merge_dependencies(current, new):
    """
    Merge two dependencies dicts of an element.

    Parameters
    ----------
    current: dict
        Current dependencies of the element. It will be mutated.

    new: dict
        New dependencies to add.

    Returns
    -------
    None

    """
    current_set, new_set = set(current), set(new)
    for dep in current_set.intersection(new_set):
        if dep.startswith("__"):
            # if it is special (__lookup__, __external__) continue
            continue
        # if dependency is in both sum the number of calls
        current[dep] += new[dep]
    for dep in new_set.difference(current_set):
        # if dependency is only in new copy it
        current[dep] = new[dep]


def build_active_initial_deps(identifier, arguments, deps):
    """
    Creates new model element dictionaries for the model elements associated
    with a stock.

    Parameters
    ----------
    identifier: str
        The python-safe name of the stock.

    expression: str
        Formula which forms the regular value for active initial.

    initial: str
        Formula which forms the initial value for active initial.

    deps: dict
        The dictionary with all the denpendencies in the expression.

    Returns
    -------
    reference: str
        A reference to the gost variable that defines the dependencies.

    new_structure: list
        List of additional model element dictionaries.

    """
    deps = build_dependencies(
        deps,
        {
            "initial": [arguments[1]],
            "step": [arguments[0]]
        })

    py_name = "_active_initial_%s" % identifier

    # describe the stateful object
    new_structure = [{
        "py_name": py_name,
        "parent_name": "",
        "real_name": "",
        "doc": "",
        "py_expr": "",
        "unit": "",
        "lims": "",
        "eqn": "",
        "subs": "",
        "merge_subs": None,
        "dependencies": deps,
        "kind": "dependencies",
        "arguments": "",
    }]

    return py_name, new_structure


def add_stock(identifier, expression, initial_condition, subs, merge_subs,
              deps):
    """
    Creates new model element dictionaries for the model elements associated
    with a stock.

    Parameters
    ----------
    identifier: str
        The python-safe name of the stock.

    expression: str
        The formula which forms the derivative of the stock.

    initial_condition: str
        Formula which forms the initial condition for the stock.

    subs: list of strings
        List of strings of subscript indices that correspond to the
        list of expressions, and collectively define the shape of the output.

    merge_subs: list of strings
        List of the final subscript range of the python array after
        merging with other objects.

    deps: dict
        The dictionary with all the denpendencies in the expression.

    Returns
    -------
    reference: str
        a string to use in place of the 'INTEG...' pieces in the element
        expression string, a reference to the stateful object.

    new_structure: list
        List of additional model element dictionaries. When there are
        subscripts, constructs an external 'init' and 'ddt' function so
        that these can be appropriately aggregated.

    """
    Imports.add("statefuls", "Integ")

    deps = build_dependencies(
        deps,
        {
            "initial": [initial_condition],
            "step": [expression]
        })

    new_structure = []
    py_name = "_integ_%s" % identifier

    if len(subs) == 0:
        stateful_py_expr = "Integ(lambda: %s, lambda: %s, '%s')" % (
            expression,
            initial_condition,
            py_name,
        )
    else:
        stateful_py_expr = "Integ(_integ_input_%s, _integ_init_%s, '%s')" % (
            identifier,
            identifier,
            py_name,
        )

        # following elements not specified in the model file, but must exist
        # create the stock initialization element
        new_structure.append({
            "py_name": "_integ_init_%s" % identifier,
            "parent_name": identifier,
            "real_name": "Implicit",
            "kind": "setup",
            "py_expr": initial_condition,
            "subs": subs,
            "merge_subs": merge_subs,
            "doc": "Provides initial conditions for %s function"
                    % identifier,
            "unit": "See docs for %s" % identifier,
            "lims": "None",
            "eqn": "None",
            "arguments": "",
        })

        new_structure.append({
            "py_name": "_integ_input_%s" % identifier,
            "parent_name": identifier,
            "real_name": "Implicit",
            "kind": "component",
            "doc": "Provides derivative for %s function" % identifier,
            "subs": subs,
            "merge_subs": merge_subs,
            "unit": "See docs for %s" % identifier,
            "lims": "None",
            "eqn": "None",
            "py_expr": expression,
            "arguments": "",
        })

    # describe the stateful object
    new_structure.append({
        "py_name": py_name,
        "parent_name": identifier,
        "real_name": "Representation of  %s" % identifier,
        "doc": "Integrates Expression %s" % expression,
        "py_expr": stateful_py_expr,
        "unit": "None",
        "lims": "None",
        "eqn": "None",
        "subs": "",
        "merge_subs": None,
        "dependencies": deps,
        "kind": "stateful",
        "arguments": "",
    })

    return "%s()" % py_name, new_structure


def add_delay(identifier, delay_input, delay_time, initial_value, order,
              subs, merge_subs, deps):
    """
    Creates code to instantiate a stateful 'Delay' object,
    and provides reference to that object's output.

    The name of the stateful object is based upon the passed in parameters,
    so if there are multiple places where identical delay functions are
    referenced, the translated python file will only maintain one stateful
    object, and reference it multiple times.

    Parameters
    ----------
    identifier: str
        The python-safe name of the delay.

    delay_input: str
        Reference to the model component that is the input to the delay.

    delay_time: str
        Can be a number (in string format) or a reference to another model
        element which will calculate the delay. This is calculated throughout
        the simulation at runtime.

    initial_value: str
        This is used to initialize the stocks that are present in the delay.
        We initialize the stocks with equal values so that the outflow in
        the first timestep is equal to this value.

    order: str
        The number of stocks in the delay pipeline. As we construct the
        delays at build time, this must be an integer and cannot be calculated
        from other model components. Anything else will yield a ValueError.

    subs: list of strings
        List of strings of subscript indices that correspond to the
        list of expressions, and collectively define the shape of the output.

    merge_subs: list of strings
        List of the final subscript range of the python array after
        merging with other objects.

    deps: dict
        The dictionary with all the denpendencies in the expression.

    Returns
    -------
    reference: str
        Reference to the delay object `__call__` method, which will return
        the output of the delay process.

    new_structure: list
        List of element construction dictionaries for the builder to assemble.

    """
    Imports.add("statefuls", "Delay")

    deps = build_dependencies(
        deps,
        {
            "initial": [initial_value, order, delay_time],
            "step": [delay_time, delay_input]
        })

    new_structure = []
    py_name = "_delay_%s" % identifier

    if len(subs) == 0:
        stateful_py_expr = (
            "Delay(lambda: %s, lambda: %s,"
            "lambda: %s, lambda: %s, time_step, '%s')"
            % (delay_input, delay_time, initial_value, order, py_name)
        )

    else:
        stateful_py_expr = (
            "Delay(_delay_input_%s, lambda: %s, _delay_init_%s,"
            "lambda: %s, time_step, '%s')"
            % (identifier, delay_time, identifier, order, py_name)
        )

        # following elements not specified in the model file, but must exist
        # create the delay initialization element
        new_structure.append({
            "py_name": "_delay_init_%s" % identifier,
            "parent_name": identifier,
            "real_name": "Implicit",
            "kind": "setup",  # not specified in the model file, but must exist
            "py_expr": initial_value,
            "subs": subs,
            "merge_subs": merge_subs,
            "doc": "Provides initial conditions for %s function" \
                    % identifier,
            "unit": "See docs for %s" % identifier,
            "lims": "None",
            "eqn": "None",
            "arguments": "",
        })

        new_structure.append({
            "py_name": "_delay_input_%s" % identifier,
            "parent_name": identifier,
            "real_name": "Implicit",
            "kind": "component",
            "doc": "Provides input for %s function" % identifier,
            "subs": subs,
            "merge_subs": merge_subs,
            "unit": "See docs for %s" % identifier,
            "lims": "None",
            "eqn": "None",
            "py_expr": delay_input,
            "arguments": "",
        })

    # describe the stateful object
    new_structure.append({
        "py_name": py_name,
        "parent_name": identifier,
        "real_name": "Delay of %s" % delay_input,
        "doc": "Delay time: %s \n Delay initial value %s \n Delay order %s"
        % (delay_time, initial_value, order),
        "py_expr": stateful_py_expr,
        "unit": "None",
        "lims": "None",
        "eqn": "None",
        "subs": "",
        "merge_subs": None,
        "dependencies": deps,
        "kind": "stateful",
        "arguments": "",
    })

    return "%s()" % py_name, new_structure


def add_delay_f(identifier, delay_input, delay_time, initial_value, deps):
    """
    Creates code to instantiate a stateful 'DelayFixed' object,
    and provides reference to that object's output.

    The name of the stateful object is based upon the passed in parameters,
    so if there are multiple places where identical delay functions are
    referenced, the translated python file will only maintain one stateful
    object, and reference it multiple times.

    Parameters
    ----------
    identifier: str
        The python-safe name of the delay.

    delay_input: str
        Reference to the model component that is the input to the delay.

    delay_time: str
        Can be a number (in string format) or a reference to another model
        element which will calculate the delay. This is calculated throughout
        the simulation at runtime.

    initial_value: str
        This is used to initialize the stocks that are present in the delay.
        We initialize the stocks with equal values so that the outflow in
        the first timestep is equal to this value.

    deps: dict
        The dictionary with all the denpendencies in the expression.

    Returns
    -------
    reference: str
        Reference to the delay object `__call__` method, which will return
        the output of the delay process.

    new_structure: list
        List of element construction dictionaries for the builder to assemble.

    """
    Imports.add("statefuls", "DelayFixed")

    deps = build_dependencies(
        deps,
        {
            "initial": [initial_value, delay_time],
            "step": [delay_input]
        })

    py_name = "_delayfixed_%s" % identifier

    stateful_py_expr = (
        "DelayFixed(lambda: %s, lambda: %s,"
        "lambda: %s, time_step, '%s')"
        % (delay_input, delay_time, initial_value, py_name)
    )

    # describe the stateful object
    stateful = {
        "py_name": py_name,
        "parent_name": identifier,
        "real_name": "Delay fixed  of %s" % delay_input,
        "doc": "DelayFixed time: %s \n Delay initial value %s"
        % (delay_time, initial_value),
        "py_expr": stateful_py_expr,
        "unit": "None",
        "lims": "None",
        "eqn": "None",
        "subs": "",
        "merge_subs": None,
        "dependencies": deps,
        "kind": "stateful",
        "arguments": "",
    }

    return "%s()" % py_name, [stateful]


def add_n_delay(identifier, delay_input, delay_time, initial_value, order,
                subs, merge_subs, deps):
    """
    Creates code to instantiate a stateful 'DelayN' object,
    and provides reference to that object's output.

    The name of the stateful object is based upon the passed in parameters,
    so if there are multiple places where identical delay functions are
    referenced, the translated python file will only maintain one stateful
    object, and reference it multiple times.

    Parameters
    ----------
    identifier: str
        The python-safe name of the delay.

    delay_input: str
        Reference to the model component that is the input to the delay.

    delay_time: str
        Can be a number (in string format) or a reference to another model
        element which will calculate the delay. This is calculated throughout
        the simulation at runtime.

    initial_value: str
        This is used to initialize the stocks that are present in the delay.
        We initialize the stocks with equal values so that the outflow in
        the first timestep is equal to this value.

    order: str
        The number of stocks in the delay pipeline. As we construct the
        delays at build time, this must be an integer and cannot be calculated
        from other model components. Anything else will yield a ValueError.

    subs: list of strings
        List of strings of subscript indices that correspond to the
        list of expressions, and collectively define the shape of the output.

    merge_subs: list of strings
        List of the final subscript range of the python array after
        merging with other objects.

    deps: dict
        The dictionary with all the denpendencies in the expression.

    Returns
    -------
    reference: str
        Reference to the delay object `__call__` method, which will return
        the output of the delay process.

    new_structure: list
        List of element construction dictionaries for the builder to assemble.

    """
    Imports.add("statefuls", "DelayN")

    deps = build_dependencies(
        deps,
        {
            "initial": [initial_value, order, delay_time],
            "step": [delay_time, delay_input]
        })

    new_structure = []
    py_name = "_delayn_%s" % identifier

    if len(subs) == 0:
        stateful_py_expr = (
            "DelayN(lambda: %s, lambda: %s,"
            "lambda: %s, lambda: %s, time_step, '%s')"
            % (delay_input, delay_time, initial_value, order, py_name)
        )

    else:
        stateful_py_expr = (
            "DelayN(_delayn_input_%s, lambda: %s,"
            " _delayn_init_%s, lambda: %s, time_step, '%s')"
            % (identifier, delay_time, identifier, order, py_name)
        )

        # following elements not specified in the model file, but must exist
        # create the delay initialization element
        new_structure.append({
            "py_name": "_delayn_init_%s" % identifier,
            "parent_name": identifier,
            "real_name": "Implicit",
            "kind": "setup",  # not specified in the model file, but must exist
            "py_expr": initial_value,
            "subs": subs,
            "merge_subs": merge_subs,
            "doc": "Provides initial conditions for %s function" \
                    % identifier,
            "unit": "See docs for %s" % identifier,
            "lims": "None",
            "eqn": "None",
            "arguments": "",
        })

        new_structure.append({
            "py_name": "_delayn_input_%s" % identifier,
            "parent_name": identifier,
            "real_name": "Implicit",
            "kind": "component",
            "doc": "Provides input for %s function" % identifier,
            "subs": subs,
            "merge_subs": merge_subs,
            "unit": "See docs for %s" % identifier,
            "lims": "None",
            "eqn": "None",
            "py_expr": delay_input,
            "arguments": "",
        })

    # describe the stateful object
    new_structure.append({
        "py_name": py_name,
        "parent_name": identifier,
        "real_name": "DelayN of %s" % delay_input,
        "doc": "DelayN time: %s \n DelayN initial value %s \n DelayN order\
                %s"
        % (delay_time, initial_value, order),
        "py_expr": stateful_py_expr,
        "unit": "None",
        "lims": "None",
        "eqn": "None",
        "subs": "",
        "merge_subs": None,
        "dependencies": deps,
        "kind": "stateful",
        "arguments": "",
    })

    return "%s()" % py_name, new_structure


def add_forecast(identifier, forecast_input, average_time, horizon,
                 subs, merge_subs, deps):
    """
    Constructs Forecast object.

    Parameters
    ----------
    identifier: str
        The python-safe name of the forecast.

    forecast_input: str
        Input of the forecast.

    average_time: str
        Average time of the forecast.

    horizon: str
        Horizon for the forecast.

    subs: list of strings
        List of strings of subscript indices that correspond to the
        list of expressions, and collectively define the shape of the output.

    merge_subs: list of strings
        List of the final subscript range of the python array after
        merging with other objects.

    deps: dict
        The dictionary with all the denpendencies in the expression.

    Returns
    -------
    reference: str
        Reference to the forecast object `__call__` method, which will return
        the output of the forecast process.

    new_structure: list
        List of element construction dictionaries for the builder to assemble.

    """
    Imports.add("statefuls", "Forecast")

    deps = build_dependencies(
        deps,
        {
            "initial": [forecast_input],
            "step": [forecast_input, average_time, horizon]
        })

    new_structure = []
    py_name = "_forecast_%s" % identifier

    if len(subs) == 0:
        stateful_py_expr = "Forecast(lambda: %s, lambda: %s,"\
                           " lambda: %s, '%s')" % (
                               forecast_input, average_time,
                               horizon, py_name)

    else:
        # only need to re-dimension init as xarray will take care of other
        stateful_py_expr = "Forecast(_forecast_input_%s, lambda: %s,"\
                           " lambda: %s, '%s')" % (
                               identifier, average_time,
                               horizon, py_name)

        # following elements not specified in the model file, but must exist
        # create the delay initialization element
        new_structure.append({
            "py_name": "_forecast_input_%s" % identifier,
            "parent_name": identifier,
            "real_name": "Implicit",
            "kind": "setup",  # not specified in the model file, but must exist
            "py_expr": forecast_input,
            "subs": subs,
            "merge_subs": merge_subs,
            "doc": "Provides input for %s function"
                    % identifier,
            "unit": "See docs for %s" % identifier,
            "lims": "None",
            "eqn": "None",
            "arguments": "",
        })

    new_structure.append({
        "py_name": py_name,
        "parent_name": identifier,
        "real_name": "Forecast of %s" % forecast_input,
        "doc": "Forecast average time: %s \n Horizon %s"
        % (average_time, horizon),
        "py_expr": stateful_py_expr,
        "unit": "None",
        "lims": "None",
        "eqn": "None",
        "subs": "",
        "merge_subs": None,
        "dependencies": deps,
        "kind": "stateful",
        "arguments": "",
    })

    return "%s()" % py_name, new_structure


def add_sample_if_true(identifier, condition, actual_value, initial_value,
                       subs, merge_subs, deps):
    """
    Creates code to instantiate a stateful 'SampleIfTrue' object,
    and provides reference to that object's output.

    Parameters
    ----------
    identifier: str
        The python-safe name of the sample if true.

    condition: str
        Reference to another model element that is the condition to the
        'sample if true' function.

    actual_value: str
        Can be a number (in string format) or a reference to another model
        element which is calculated throughout the simulation at runtime.

    initial_value: str
        This is used to initialize the state of the sample if true function.

    subs: list of strings
        List of strings of subscript indices that correspond to the
        list of expressions, and collectively define the shape of the output.

    merge_subs: list of strings
        List of the final subscript range of the python array after
        merging with other objects.

    deps: dict
        The dictionary with all the denpendencies in the expression.

    Returns
    -------
    reference: str
        Reference to the sample if true object `__call__` method,
        which will return the output of the sample if true process.

    new_structure: list
        List of element construction dictionaries for the builder to assemble.

    """
    Imports.add("statefuls", "SampleIfTrue")

    deps = build_dependencies(
        deps,
        {
            "initial": [initial_value],
            "step": [actual_value, condition]
        })

    new_structure = []
    py_name = "_sample_if_true_%s" % identifier

    if len(subs) == 0:
        stateful_py_expr = "SampleIfTrue(lambda: %s, lambda: %s,"\
                           "lambda: %s, '%s')" % (
                               condition, actual_value, initial_value, py_name)

    else:
        stateful_py_expr = "SampleIfTrue(lambda: %s, lambda: %s,"\
                           "_sample_if_true_init_%s, '%s')" % (
                               condition, actual_value, identifier, py_name)

        # following elements not specified in the model file, but must exist
        # create the delay initialization element
        new_structure.append({
            "py_name": "_sample_if_true_init_%s" % identifier,
            "parent_name": identifier,
            "real_name": "Implicit",
            "kind": "setup",  # not specified in the model file, but must exist
            "py_expr": initial_value,
            "subs": subs,
            "merge_subs": merge_subs,
            "doc": "Provides initial conditions for %s function" % identifier,
            "unit": "See docs for %s" % identifier,
            "lims": "None",
            "eqn": "None",
            "arguments": ""
        })
    # describe the stateful object
    new_structure.append({
        "py_name": py_name,
        "parent_name": identifier,
        "real_name": "Sample if true of %s" % identifier,
        "doc": "Initial value: %s \n  Input: %s \n Condition: %s" % (
            initial_value, actual_value, condition),
        "py_expr": stateful_py_expr,
        "unit": "None",
        "lims": "None",
        "eqn": "None",
        "subs": "",
        "merge_subs": None,
        "dependencies": deps,
        "kind": "stateful",
        "arguments": ""
    })

    return "%s()" % py_name, new_structure


def add_n_smooth(identifier, smooth_input, smooth_time, initial_value, order,
                 subs, merge_subs, deps):
    """
    Constructs stock and flow chains that implement the calculation of
    a smoothing function.

    Parameters
    ----------
    identifier: str
        The python-safe name of the smooth.

    smooth_input: str
        Reference to the model component that is the input to the
        smoothing function.

    smooth_time: str
        Can be a number (in string format) or a reference to another model
        element which will calculate the delay. This is calculated throughout
        the simulation at runtime.

    initial_value: str
        This is used to initialize the stocks that are present in the delay.
        We initialize the stocks with equal values so that the outflow in
        the first timestep is equal to this value.

    order: str
        The number of stocks in the delay pipeline. As we construct the delays
        at build time, this must be an integer and cannot be calculated from
        other model components. Anything else will yield a ValueError.

    subs: list of strings
        List of strings of subscript indices that correspond to the
        list of expressions, and collectively define the shape of the output

    merge_subs: list of strings
        List of the final subscript range of the python array after.

    deps: dict
        The dictionary with all the denpendencies in the expression.

    Returns
    -------
    reference: str
        Reference to the smooth object `__call__` method, which will return
        the output of the smooth process.

    new_structure: list
        List of element construction dictionaries for the builder to assemble.

    """
    Imports.add("statefuls", "Smooth")

    deps = build_dependencies(
        deps,
        {
            "initial": [initial_value, order],
            "step": [smooth_input, smooth_time]
        })

    new_structure = []
    py_name = "_smooth_%s" % identifier

    if len(subs) == 0:
        stateful_py_expr = (
            "Smooth(lambda: %s, lambda: %s,"
            "lambda: %s, lambda: %s, '%s')"
            % (smooth_input, smooth_time, initial_value, order, py_name)
        )

    else:
        # only need to re-dimension init and input as xarray will take care of
        # other
        stateful_py_expr = (
            "Smooth(_smooth_input_%s, lambda: %s,"
            " _smooth_init_%s, lambda: %s, '%s')"
            % (identifier, smooth_time, identifier, order, py_name)
        )

        # following elements not specified in the model file, but must exist
        # create the delay initialization element
        new_structure.append({
            "py_name": "_smooth_init_%s" % identifier,
            "parent_name": identifier,
            "real_name": "Implicit",
            "kind": "setup",  # not specified in the model file, but must exist
            "py_expr": initial_value,
            "subs": subs,
            "merge_subs": merge_subs,
            "doc": "Provides initial conditions for %s function" % \
                    identifier,
            "unit": "See docs for %s" % identifier,
            "lims": "None",
            "eqn": "None",
            "arguments": "",
        })

        new_structure.append({
            "py_name": "_smooth_input_%s" % identifier,
            "parent_name": identifier,
            "real_name": "Implicit",
            "kind": "component",
            "doc": "Provides input for %s function" % identifier,
            "subs": subs,
            "merge_subs": merge_subs,
            "unit": "See docs for %s" % identifier,
            "lims": "None",
            "eqn": "None",
            "py_expr": smooth_input,
            "arguments": "",
        })

    new_structure.append({
        "py_name": py_name,
        "parent_name": identifier,
        "real_name": "Smooth of %s" % smooth_input,
        "doc": "Smooth time %s \n Initial value %s \n Smooth order %s" % (
            smooth_time, initial_value, order),
        "py_expr": stateful_py_expr,
        "unit": "None",
        "lims": "None",
        "eqn": "None",
        "subs": "",
        "merge_subs": None,
        "dependencies": deps,
        "kind": "stateful",
        "arguments": "",
    })

    return "%s()" % py_name, new_structure


def add_n_trend(identifier, trend_input, average_time, initial_trend,
                subs, merge_subs, deps):
    """
    Constructs Trend object.

    Parameters
    ----------
    identifier: str
        The python-safe name of the trend.

    trend_input: str
        Input of the trend.

    average_time: str
        Average time of the trend.

    trend_initial: str
        This is used to initialize the trend.

    subs: list of strings
        List of strings of subscript indices that correspond to the
        list of expressions, and collectively define the shape of the output.

    merge_subs: list of strings
        List of the final subscript range of the python array after
        merging with other objects.

    deps: dict
        The dictionary with all the denpendencies in the expression.

    Returns
    -------
    reference: str
        Reference to the trend object `__call__` method, which will return the
        output of the trend process.

    new_structure: list
        List of element construction dictionaries for the builder to assemble.

    """
    Imports.add("statefuls", "Trend")

    deps = build_dependencies(
        deps,
        {
            "initial": [initial_trend, trend_input, average_time],
            "step": [trend_input, average_time]
        })

    new_structure = []
    py_name = "_trend_%s" % identifier

    if len(subs) == 0:
        stateful_py_expr = "Trend(lambda: %s, lambda: %s,"\
                           " lambda: %s, '%s')" % (
                               trend_input, average_time,
                               initial_trend, py_name)

    else:
        # only need to re-dimension init as xarray will take care of other
        stateful_py_expr = "Trend(lambda: %s, lambda: %s,"\
                           " _trend_init_%s, '%s')" % (
                               trend_input, average_time,
                               identifier, py_name)

        # following elements not specified in the model file, but must exist
        # create the delay initialization element
        new_structure.append({
            "py_name": "_trend_init_%s" % identifier,
            "parent_name": identifier,
            "real_name": "Implicit",
            "kind": "setup",  # not specified in the model file, but must exist
            "py_expr": initial_trend,
            "subs": subs,
            "merge_subs": merge_subs,
            "doc": "Provides initial conditions for %s function"
                    % identifier,
            "unit": "See docs for %s" % identifier,
            "lims": "None",
            "eqn": "None",
            "arguments": "",
        })

    new_structure.append({
        "py_name": py_name,
        "parent_name": identifier,
        "real_name": "trend of %s" % trend_input,
        "doc": "Trend average time: %s \n Trend initial value %s"
        % (average_time, initial_trend),
        "py_expr": stateful_py_expr,
        "unit": "None",
        "lims": "None",
        "eqn": "None",
        "subs": "",
        "merge_subs": None,
        "dependencies": deps,
        "kind": "stateful",
        "arguments": "",
    })

    return "%s()" % py_name, new_structure


def add_initial(identifier, value, deps):
    """
    Constructs a stateful object for handling vensim's 'Initial' functionality.

    Parameters
    ----------
    identifier: str
        The python-safe name of the initial.

    value: str
        The expression which will be evaluated, and the first value of
        which returned.

    deps: dict
        The dictionary with all the denpendencies in the expression.

    Returns
    -------
    reference: str
        Reference to the Initial object `__call__` method,
        which will return the first calculated value of `identifier`.

    new_structure: list
        List of element construction dictionaries for the builder to assemble.

    """
    Imports.add("statefuls", "Initial")

    deps = build_dependencies(
        deps,
        {
            "initial": [value]
        })

    py_name = "_initial_%s" % identifier

    stateful = {
        "py_name": py_name,
        "parent_name": identifier,
        "real_name": "Initial %s" % identifier,
        "doc": "Returns the value taken on during the initialization phase",
        "py_expr": "Initial(lambda: %s, '%s')" % (value, py_name),
        "unit": "None",
        "lims": "None",
        "eqn": "None",
        "subs": "",
        "merge_subs": None,
        "dependencies": deps,
        "kind": "stateful",
        "arguments": "",
    }

    return "%s()" % stateful["py_name"], [stateful]


def add_tab_data(identifier, real_name, subs,
                 subscript_dict, merge_subs, keyword):
    """
    Constructs an object for handling Vensim's regular DATA components.

    Parameters
    ----------
    identifier: str
        The python-safe name of the external values.

    real_name: str
        The real name of the variable.

    subs: list of strings
        List of strings of subscript indices that correspond to the
        list of expressions, and collectively define the shape of the output.

    subscript_dict: dict
        Dictionary describing the possible dimensions of the stock's
        subscripts.

    merge_subs: list of strings
        List of the final subscript range of the python array after
        merging with other objects.

    keyword: str
        Data retrieval method ('interpolate', 'look forward', 'hold backward').

    Returns
    -------
    reference: str
        Reference to the TabData object `__call__` method, which will
        return the retrieved value of data for the current time step.

    new_structure: list
        List of element construction dictionaries for the builder to assemble.

    """
    Imports.add("data", "TabData")

    coords = utils.simplify_subscript_input(
        utils.make_coord_dict(subs, subscript_dict, terse=False),
        subscript_dict, return_full=False, merge_subs=merge_subs)
    keyword = (
        "'%s'" % keyword.strip(":").lower() if isinstance(keyword, str) else
        keyword)
    name = "_data_%s" % identifier

    data = {
        "py_name": name,
        "parent_name": identifier,
        "real_name": "Data for %s" % identifier,
        "doc": "Provides data for data variable %s" % identifier,
        "py_expr": "TabData('%s', '%s', %s, %s)" % (
            real_name, identifier, coords, keyword),
        "unit": "None",
        "lims": "None",
        "eqn": "None",
        "subs": subs,
        "merge_subs": merge_subs,
        "kind": "tab_data",
        "arguments": "",
    }

    return "%s(time())" % data["py_name"], [data]


def add_ext_data(identifier, file_name, tab, time_row_or_col, cell, subs,
                 subscript_dict, merge_subs, keyword):
    """
    Constructs a external object for handling Vensim's GET XLS DATA and
    GET DIRECT DATA functionality.

    Parameters
    ----------
    identifier: str
        The python-safe name of the external values.

    file_name: str
        Filepath to the data.

    tab: str
        Tab where the data is.

    time_row_or_col: str
        Identifier to the starting point of the time dimension.

    cell: str
        Cell identifier where the data starts.

    subs: list of strings
        List of strings of subscript indices that correspond to the
        list of expressions, and collectively define the shape of the output.

    subscript_dict: dict
        Dictionary describing the possible dimensions of the stock's
        subscripts.

    merge_subs: list of strings
        List of the final subscript range of the python array after
        merging with other objects.

    keyword: str
        Data retrieval method ('interpolate', 'look forward', 'hold backward').

    Returns
    -------
    reference: str
        Reference to the ExtData object `__call__` method, which will
        return the retrieved value of data for the current time step.

    new_structure: list
        List of element construction dictionaries for the builder to assemble.

    """
    Imports.add("external", "ExtData")

    coords = utils.simplify_subscript_input(
        utils.make_coord_dict(subs, subscript_dict, terse=False),
        subscript_dict, return_full=False, merge_subs=merge_subs)
    keyword = (
        "'%s'" % keyword.strip(":").lower() if isinstance(keyword, str) else
        keyword)
    name = "_ext_data_%s" % identifier

    # Check if the object already exists
    if name in build_names:
        # Create a new py_name with ADD_# ending
        # This object name will not be used in the model as
        # the information is added to the existing object
        # with add method.
        kind = "external_add"
        name = utils.make_add_identifier(name, build_names)
        py_expr = ".add(%s, %s, %s, %s, %s, %s)"
    else:
        # Regular name will be used and a new object will be created
        # in the model file.
        build_names.add(name)
        kind = "external"
        py_expr = "ExtData(%s, %s, %s, %s, %s, %s,\n"\
                  "        _root, '{}')".format(name)

    external = {
        "py_name": name,
        "parent_name": identifier,
        "real_name": "External data for %s" % identifier,
        "doc": "Provides data for data variable %s" % identifier,
        "py_expr": py_expr % (file_name, tab, time_row_or_col, cell, keyword,
                              coords),
        "unit": "None",
        "lims": "None",
        "eqn": "None",
        "subs": subs,
        "merge_subs": merge_subs,
        "kind": kind,
        "arguments": "",
    }

    return "%s(time())" % external["py_name"], [external]


def add_ext_constant(identifier, file_name, tab, cell,
                     subs, subscript_dict, merge_subs):
    """
    Constructs a external object for handling Vensim's GET XLS CONSTANT and
    GET DIRECT CONSTANT functionality.

    Parameters
    ----------
    identifier: str
        The python-safe name of the external values.

    file_name: str
        Filepath to the data.

    tab: str
        Tab where the data is.

    cell: str
        Cell identifier where the data starts.

    subs: list of strings
        List of strings of subscript indices that correspond to the
        list of expressions, and collectively define the shape of the output.

    subscript_dict: dict
        Dictionary describing the possible dimensions of the stock's
        subscripts.

    merge_subs: list of strings
        List of the final subscript range of the python array after
        merging with other objects.

    Returns
    -------
    reference: str
        Reference to the ExtConstant object `__call__` method,
        which will return the read value of the data.

    new_structure: list
        List of element construction dictionaries for the builder to assemble.

    """
    Imports.add("external", "ExtConstant")

    coords = utils.simplify_subscript_input(
        utils.make_coord_dict(subs, subscript_dict, terse=False),
        subscript_dict, return_full=False, merge_subs=merge_subs)
    name = "_ext_constant_%s" % identifier

    # Check if the object already exists
    if name in build_names:
        # Create a new py_name with ADD_# ending
        # This object name will not be used in the model as
        # the information is added to the existing object
        # with add method.
        kind = "external_add"
        name = utils.make_add_identifier(name, build_names)
        py_expr = ".add(%s, %s, %s, %s)"
    else:
        # Regular name will be used and a new object will be created
        # in the model file.
        kind = "external"
        py_expr = "ExtConstant(%s, %s, %s, %s,\n"\
                  "            _root, '{}')".format(name)
    build_names.add(name)

    external = {
        "py_name": name,
        "parent_name": identifier,
        "real_name": "External constant for %s" % identifier,
        "doc": "Provides data for constant data variable %s" % identifier,
        "py_expr": py_expr % (file_name, tab, cell, coords),
        "unit": "None",
        "lims": "None",
        "eqn": "None",
        "subs": subs,
        "merge_subs": merge_subs,
        "kind": kind,
        "arguments": "",
    }

    return "%s()" % external["py_name"], [external]


def add_ext_lookup(identifier, file_name, tab, x_row_or_col, cell,
                   subs, subscript_dict, merge_subs):
    """
    Constructs a external object for handling Vensim's GET XLS LOOKUPS and
    GET DIRECT LOOKUPS functionality.

    Parameters
    ----------
    identifier: str
        The python-safe name of the external values.

    file_name: str
        Filepath to the data.

    tab: str
        Tab where the data is.

    x_row_or_col: str
        Identifier to the starting point of the lookup dimension.

    cell: str
        Cell identifier where the data starts.

    subs: list of strings
        List of strings of subscript indices that correspond to the
        list of expressions, and collectively define the shape of the output.

    subscript_dict: dict
        Dictionary describing the possible dimensions of the stock's
        subscripts.

    merge_subs: list of strings
        List of the final subscript range of the python array after
        merging with other objects.

    Returns
    -------
    reference: str
        Reference to the ExtLookup object `__call__` method,
        which will return the retrieved value of data after interpolating it.

    new_structure: list
        List of element construction dictionaries for the builder to assemble.

    """
    Imports.add("external", "ExtLookup")

    coords = utils.simplify_subscript_input(
        utils.make_coord_dict(subs, subscript_dict, terse=False),
        subscript_dict, return_full=False, merge_subs=merge_subs)
    name = "_ext_lookup_%s" % identifier

    # Check if the object already exists
    if name in build_names:
        # Create a new py_name with ADD_# ending
        # This object name will not be used in the model as
        # the information is added to the existing object
        # with add method.
        kind = "external_add"
        name = utils.make_add_identifier(name, build_names)
        py_expr = ".add(%s, %s, %s, %s, %s)"
    else:
        # Regular name will be used and a new object will be created
        # in the model file.
        kind = "external"
        py_expr = "ExtLookup(%s, %s, %s, %s, %s,\n"\
                  "          _root, '{}')".format(name)
    build_names.add(name)

    external = {
        "py_name": name,
        "parent_name": identifier,
        "real_name": "External lookup data for %s" % identifier,
        "doc": "Provides data for external lookup variable %s" % identifier,
        "py_expr": py_expr % (file_name, tab, x_row_or_col, cell, coords),
        "unit": "None",
        "lims": "None",
        "eqn": "None",
        "subs": subs,
        "merge_subs": merge_subs,
        "kind": kind,
        "arguments": "x",
    }

    return "%s(x)" % external["py_name"], [external]


def add_macro(identifier, macro_name, filename, arg_names, arg_vals, deps):
    """
    Constructs a stateful object instantiating a 'Macro'.

    Parameters
    ----------
    identifier: str
        The python-safe name of the element that calls the macro.

    macro_name: str
        Python safe name for macro.

    filename: str
        Filepath to macro definition.

    func_args: dict
        Dictionary of values to be passed to macro, {key: function}.

    Returns
    -------
    reference: str
        Reference to the Initial object `__call__` method,
        which will return the first calculated value of `initial_input`.

    new_structure: list
        List of element construction dictionaries for the builder to assemble.

    """
    Imports.add("statefuls", "Macro")

    deps = build_dependencies(
        deps,
        {
            "initial": arg_vals,
            "step": arg_vals
        })

    py_name = "_macro_" + macro_name + "_" + identifier

    func_args = "{ %s }" % ", ".join(
        ["'%s': lambda: %s" % (key, val) for key, val in zip(arg_names,
                                                             arg_vals)])

    stateful = {
        "py_name": py_name,
        "parent_name": identifier,
        "real_name": "Macro Instantiation of " + macro_name,
        "doc": "Instantiates the Macro",
        "py_expr": "Macro(_root.joinpath('%s'), %s, '%s',"
        " time_initialization=lambda: __data['time'],"
        " py_name='%s')" % (filename, func_args, macro_name, py_name),
        "unit": "None",
        "lims": "None",
        "eqn": "None",
        "subs": "",
        "merge_subs": None,
        "dependencies": deps,
        "kind": "stateful",
        "arguments": "",
    }

    return "%s()" % stateful["py_name"], [stateful]


def add_incomplete(var_name, dependencies):
    """
    Incomplete functions don't really need to be 'builders' as they
    add no new real structure, but it's helpful to have a function
    in which we can raise a warning about the incomplete equation
    at translate time.

    parameters
    ----------
    var_name: str
        The python-safe name of the incomplete variable.

    dependencies: list
        The list of the dependencies in the variable.

    Returns
    -------
    str:
        Inclompete funcion call.

    """
    Imports.add("functions", "incomplete")

    warnings.warn(
        "%s has no equation specified" % var_name, SyntaxWarning, stacklevel=2
    )

    # first arg is `self` reference
    return "incomplete(%s)" % ", ".join(dependencies), []


def build_dependencies(deps, exps):
    # TODO document

    deps_dict = {"initial": {}, "step": {}}

    for target, exprs in exps.items():
        expr = ".".join(exprs)
        for dep in deps:
            n_calls = len(
                re.findall(
                    "(?<![0-9A-Za-z_])" + dep + "(?![0-9A-Za-z_])",
                    expr)
            )
            if n_calls > 0:
                deps_dict[target][dep] = n_calls

    return deps_dict


def build_function_call(function_def, user_arguments, dependencies=set()):
    """
    Build a function call using the arguments from the original model.

    Parameters
    ----------
    function_def: dict
        Function definition map with following keys:
        - name: name of the function.
        - parameters: list with description of all parameters of this function
            - name
            - optional?
            - type: [
                "expression", - provide converted expression as parameter for
                                runtime evaluating before the method call
                "lambda",     - provide lambda expression as parameter for
                                delayed runtime evaluation in the method call
                "time",       - provide access to current instance of
                                time object
                "scope",      - provide access to current instance of
                                scope object (instance of Macro object)
                "predef"      - provide an invariant argument. Argument not
                                given in Vensim/Xmile but needed for python.
                "ignore"      - ignore an user argument. Argument given in
                                Vensim/Xmile but not needed for python.
                "subs_range_to_list"
                              - provides the list of subscripts in a given
                                subscript range
            ]

    user_arguments: list
        Arguments provided from model.

    dependencies: set (optional)
        Set to update dependencies if needed.

    Returns
    -------
    str:
        Function call.

    """
    if isinstance(function_def, str):
        return function_def + "(" + ",".join(user_arguments) + ")"

    if function_def["name"] == "not_implemented_function":
        user_arguments = ["'" + function_def["original_name"] + "'"] + \
            user_arguments
        warnings.warn(
            "\n\nTrying to translate "
            + function_def["original_name"]
            + " which it is not implemented on PySD. The translated "
            + "model will crash... "
        )

    if "module" in function_def:
        if function_def["module"] in ["numpy", "xarray"]:
            # import external modules
            Imports.add(function_def["module"])
        else:
            # import method from PySD module
            Imports.add(function_def["module"], function_def["name"])

    if "parameters" in function_def:
        parameters = function_def["parameters"]
        user_argument = ""
        arguments = []
        argument_idx = 0
        for parameter_idx in range(len(parameters)):
            parameter_def = parameters[parameter_idx]
            is_optional = (
                parameter_def["optional"] if "optional" in parameter_def else
                False
            )
            if argument_idx >= len(user_arguments) and is_optional:
                break

            parameter_type = (
                parameter_def["type"] if "type" in parameter_def else
                "expression")

            if parameter_type in ["expression",
                                  "lambda",
                                  "subs_range_to_list"]:
                user_argument = user_arguments[argument_idx]
                argument_idx += 1
            elif parameter_type == "time":
                if "time" in dependencies:
                    dependencies["time"] += 1
                else:
                    dependencies["time"] = 1
            elif parameter_type == "ignore":
                argument_idx += 1
                continue

            arguments.append(
                {
                    "expression": user_argument,
                    "lambda": "lambda: " + user_argument,
                    "time": "__data['time']",
                    "scope": "__data['scope']",
                    "predef": parameter_def["name"],
                    "subs_range_to_list": f"_subscript_dict['{user_argument}']"
                }[parameter_type]
            )

        return function_def["name"] + "(" + ", ".join(arguments) + ")"

    return function_def["name"] + "(" + ",".join(user_arguments) + ")"

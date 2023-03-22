import pyclbr

def get_from_module(module):

    classes = []
    functions = []
    
    module_data = pyclbr.readmodule_ex(module)

    for name, data in module_data.items():
        if isinstance(data, pyclbr.Function):
            functions.append(data)

    module_data = pyclbr.readmodule(module)

    for name, data in module_data.items():
        if isinstance(data, pyclbr.Class):
            classes.append(data)
    return [classes, functions]


def ensure_tabs(assembly_code):
    assembly_code = "\t".join(assembly_code.split("    "))
    return assembly_code
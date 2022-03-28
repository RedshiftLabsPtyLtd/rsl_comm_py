# Author: Dr. Konstantin Selyunin
# Created: 7 April 2020
# Modified: 28 March 2022
# Version: v0.5
# License: MIT

import os

from pathlib import Path
from rsl_comm_py.rsl_generator import RslGenerator
from textwrap import indent
from datetime import datetime


if __name__ == '__main__':
    script_folder = Path(__file__).parent
    svd_file = script_folder / 'rsl_xml_svd' / 'um7.svd'
    rsl_svd_generator = RslGenerator(svd_file=svd_file)
    um7_main_registers = indent(rsl_svd_generator.generate_props_for_main_register_map(), ' ' * 4)
    um7_hidden_registers = indent(rsl_svd_generator.generate_props_for_hidden_registers(), ' ' * 4)

    today = datetime.now().strftime('%Y.%m.%d')
    params_dict = {
        'generated_code_for_main_register_map': um7_main_registers,
        'generated_code_for_hidden_register_map': um7_hidden_registers,
        'today': today
    }
    um7_template = script_folder / 'templates'/ 'um7_template.jinja2'
    gen_code = RslGenerator.render_template_to_str(um7_template, params_dict)
    with open('um7_registers.py', 'w') as fd:
        fd.write(gen_code)

    reg_addr_enum_template = script_folder / 'templates'/'python_reg_access.jinja2'

    param_dict = {'version': 'v0.2',
                  'date': today,
                  'cregs': rsl_svd_generator.cregs,
                  'dregs': rsl_svd_generator.dregs,
                  'commands': rsl_svd_generator.commands,
                  'module': 'um7_serial',
                  'classname': 'UM7Serial',
                  'svd': 'um7',
                  'object': 'um7'}
    gen_code = RslGenerator.render_template_to_str(reg_addr_enum_template, param_dict)
    with open('um7_py_accessor.py', 'w') as fd:
        fd.write(gen_code)


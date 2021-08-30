# Author: Dr. Konstantin Selyunin
# Created: 30 August 2021
# Modified: 30 August 2021
# Version: v0.1
# License: MIT

import os
import os.path

from datetime import datetime
from pathlib import Path
from textwrap import indent
from rsl_comm_py.rsl_generator import RslGenerator


if __name__ == '__main__':
    script_folder = Path(__file__).parent
    svd_file = script_folder / 'rsl_xml_svd' / 'um8.svd'
    rsl_svd_generator = RslGenerator(svd_file=svd_file)
    um8_main_registers = indent(rsl_svd_generator.generate_props_for_main_register_map(), ' ' * 4)
    um8_hidden_registers = indent(rsl_svd_generator.generate_props_for_hidden_registers(), ' ' * 4)

    today = datetime.now().strftime('%Y.%m.%d')
    params_dict = {
        'generated_code_for_main_register_map': um8_main_registers,
        'generated_code_for_hidden_register_map': um8_hidden_registers,
        'today': today
    }
    um8_template = script_folder / 'templates' / 'um8_template.jinja2'
    gen_code = RslGenerator.render_template_to_str(um8_template, params_dict)
    with open('um8_registers.py', 'w') as fd:
        fd.write(gen_code)

    reg_addr_enum_template = script_folder / 'templates' / 'python_reg_access.jinja2'
    param_dict = {'version': 'v0.1',
                  'date': today,
                  'cregs': rsl_svd_generator.cregs,
                  'dregs': rsl_svd_generator.dregs,
                  'commands': rsl_svd_generator.commands,
                  'module': 'um8_serial',
                  'classname': 'UM8Serial',
                  'svd': 'um8',
                  'object': 'um8'}
    gen_code = RslGenerator.render_template_to_str(reg_addr_enum_template, param_dict)
    with open('um8_py_accessor.py', 'w') as fd:
        fd.write(gen_code)


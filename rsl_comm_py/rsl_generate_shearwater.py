# Author: Dr. Konstantin Selyunin
# Created: 7 April 2020
# Modified: 12 June 2020
# Version: v0.5
# License: MIT

import os.path

from rsl_comm_py.rsl_generator import RslGenerator
from textwrap import indent
from datetime import datetime


if __name__ == '__main__':
    script_folder = os.path.dirname(__file__)
    svd_file = os.path.join(script_folder, os.pardir, 'rsl_xml_svd/shearwater.svd')
    rsl_svd_generator = RslGenerator(svd_file=svd_file)
    shearwater_main_registers = indent(rsl_svd_generator.generate_props_for_main_register_map(), ' ' * 4)
    shearwater_hidden_registers = indent(rsl_svd_generator.generate_props_for_hidden_registers(), ' ' * 4)

    today = datetime.now().strftime('%Y.%m.%d')
    params_dict = {
        'generated_code_for_main_register_map': shearwater_main_registers,
        'generated_code_for_hidden_register_map': shearwater_hidden_registers,
        'today': today
    }
    shearwater_template = os.path.join(script_folder, os.pardir, 'um7py/templates/shearwater_template.jinja2')
    gen_code = RslGenerator.render_template_to_str(shearwater_template, params_dict)
    with open('shearwater_registers.py', 'w') as fd:
        fd.write(gen_code)

    reg_addr_enum_template = os.path.join(script_folder, os.pardir, 'um7py/templates/python_reg_access.jinja2')
    param_dict = {'version': 'v0.2',
                  'date': today,
                  'cregs': rsl_svd_generator.cregs,
                  'dregs': rsl_svd_generator.dregs,
                  'commands': rsl_svd_generator.commands,
                  'module': 'shearwater_serial',
                  'classname': 'ShearWaterSerial',
                  'svd': 'shearwater',
                  'object': 'shearwater'}
    gen_code = RslGenerator.render_template_to_str(reg_addr_enum_template, param_dict)
    with open('shearwater_py_accessor.py', 'w') as fd:
        fd.write(gen_code)

    reg_map_template = os.path.join(script_folder, os.pardir, 'um7py/templates/register_map.h.jinja2')
    param_dict = {'version': 'v0.2',
                  'date': today,
                  'regs': rsl_svd_generator.regs,
                  'define_guard': 'RSL_SHEARWATER_REGISTER_MAP_H'}
    gen_code = RslGenerator.render_template_to_str(reg_map_template, param_dict)
    with open('shearwater.h', 'w') as fd:
        fd.write(gen_code)

    reg_addr_enum_template = os.path.join(script_folder, os.pardir, 'um7py/templates/register_enum.h.jinja2')
    param_dict = {'version': 'v0.3',
                  'date': today,
                  'cregs': rsl_svd_generator.cregs,
                  'dregs': rsl_svd_generator.dregs,
                  'commands': rsl_svd_generator.commands,
                  'define_guard': 'RSL_SHEARWATER_REGISTER_ENUM_H'}
    gen_code = RslGenerator.render_template_to_str(reg_addr_enum_template, param_dict)
    with open('shearwater_enum.h', 'w') as fd:
        fd.write(gen_code)

    #  HIDDEN_REGISTERS
    hidden_reg_map_template = os.path.join(script_folder, os.pardir, 'um7py/templates/register_map.h.jinja2')
    reg_map_out = 'shearwater_hidden.h'
    param_dict = {'version': 'v0.2',
                  'date': today,
                  'regs': rsl_svd_generator.hidden_regs,
                  'define_guard': 'RSL_SHEARWATER_HIDDEN_REGISTER_MAP_H'}
    gen_code = RslGenerator.render_template_to_str(hidden_reg_map_template, param_dict)
    with open('shearwater_hidden.h', 'w') as fd:
        fd.write(gen_code)

    reg_addr_enum_template = os.path.join(script_folder, os.pardir, 'um7py/templates/register_hidden_enum.h.jinja2')
    param_dict = {'version': 'v0.2',
                  'date': today,
                  'regs': rsl_svd_generator.hidden_regs,
                  'define_guard':  'RSL_SHEARWATER_HIDDEN_REGISTER_ENUM_MAP_H'}
    gen_code = RslGenerator.render_template_to_str(reg_addr_enum_template, param_dict)
    with open('shearwater_hidden_enum.h', 'w') as fd:
        fd.write(gen_code)

    reg_hidden_enum_template = os.path.join(script_folder, os.pardir, 'um7py/templates/python_hidden_reg_access.jinja2')
    param_dict = {'version': 'v0.2',
                  'date': today,
                  'regs': rsl_svd_generator.hidden_regs}
    gen_code = RslGenerator.render_template_to_str(reg_hidden_enum_template, param_dict)
    with open('shearwater_hidden_py_accessor.py', 'w') as fd:
        fd.write(gen_code)

    reg_python_config_template = os.path.join(script_folder, os.pardir,
                                              'um7py/templates/python_shearwater_config.jinja2')
    param_dict = {'hidden_regs': rsl_svd_generator.hidden_regs,
                  'config_regs': rsl_svd_generator.cregs,
                  'data_regs': rsl_svd_generator.dregs,
                  'command_regs': rsl_svd_generator.commands}
    gen_code = RslGenerator.render_template_to_str(reg_python_config_template, param_dict)
    with open('ShearwaterConfiguration.py', 'w') as fd:
        fd.write(gen_code)

from typing import Any, Iterable
import lxml.etree as ET
from pygalgen.generator.pluggability.strategy import Strategy, StrategyStage
from pygalgen.generator.common.params.argument_parser_conversion import \
    obtain_and_convert_parser, extract_useful_info_from_parser

import pygalgen.generator.common.xml_utils as xu


class DefaultParams(Strategy):
    STAGE = StrategyStage.PARAMS

    def __init__(self, args: Any, macros):
        super(DefaultParams, self).__init__(args, macros, self.STAGE)

    def apply_strategy(self, xml_output: ET.ElementTree, file_path: str,
                       module_name: str) -> ET.ElementTree:
        inputs = xml_output.find(".//inputs")

        parser = obtain_and_convert_parser(file_path)
        data_inputs = set(item for item in self.args.inputs.split(","))
        param_info = extract_useful_info_from_parser(parser, data_inputs)

        sections = {}
        for param in param_info:
            if param.section not in sections:
                sections[param.section] = \
                    xu.create_section(inputs, param.section, False)

            curr_root = sections[param.section]

            if param.is_repeat:
                curr_root = xu.create_repeat(curr_root, param.name + "_repeat")

            curr_root = xu.create_param(curr_root, param.attribute,
                                        param.type, param.optional,
                                        param.label, param.help)

            if param.is_select:
                for choice in param.choices:
                    xu.create_option(curr_root, str(choice),
                                     str(choice).capitalize())

        return xml_output

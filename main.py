from argparse import ArgumentParser

from dotenv import load_dotenv

from core import ParamsToExecuteScript
from core import ScriptManager

if __name__ == '__main__':
    load_dotenv()

    script_types: list = [param.value for param in ParamsToExecuteScript]

    parser = ArgumentParser(
        prog='Script de extraccion de datos',
        description='Scripts para extraccion de datos de PPas',
    )
    parser.add_argument(
        '--process',
        help=f'Inserte los nombres de los scripts a ejecutar, ejemplo: {script_types}',
        nargs="+",
        default=script_types
    )
    args = parser.parse_args()

    params_list = args.process
    script_manager: ScriptManager = ScriptManager(params_to_execute=params_list)
    script_manager.execute()

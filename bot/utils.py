""" A collection of useful functions """

import os
import ujson
import aiofiles


class FunctionDescriptor(object):
    """ TODO """

    def __init__(self, function):
        self.function = function

    def __str__(self):
        return ""


async def get_json_file(bot_instance):
    """ Return the dictionary who represent the json file located in private.json """
    root_dir = os.path.dirname(os.path.abspath(__file__))

    async with aiofiles.open(f"{root_dir}/../data.json", mode="r") as _file:
        data = await bot_instance.loop.run_in_executor(
            None, ujson.loads, await _file.read()
        )

        return data

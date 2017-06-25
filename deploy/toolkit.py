import click
import lambda_deploy
import lambda_schedule
from os import path
import sys
import re


@click.command()
@click.pass_context
@click.option("--function_name", default="test", help="Name of the function.")
@click.option("--file_name", default="test.py", help="Name of the file where "
              "the handler function can be found.")
@click.option("--handler", default="handler", help="Name of the handler "
              "function.")
@click.option("--every", default="1d", help="The interval to invoke the "
              "function, like 1m, 1h or 1d.")
@click.argument("dir_to_deploy")
def deploy(ctx, function_name, file_name, handler, every, dir_to_deploy):

    print(function_name)
    print(dir_to_deploy)
    print(file_name)
    print(handler)

    if not path.isdir("./" + dir_to_deploy):
        sys.exit("Please specify an existing directory.")
    elif len(function_name) > 64:
        sys.exit("Please specify a proper function name with max 64 "
                 "characters.")
    elif not path.isfile("./" + dir_to_deploy + "/" + file_name):
        sys.exit("Please specify an existing handler file name.")
    elif len(every) < 2 or len(every) > 3:
        sys.exit("Please specify a correct interval, like 1m, 1h or 1d.")

    match = re.match(r"([0-9]+)([a-z]+)", every, re.I)
    print(match)
    if match is None:
        sys.exit("Please specify a correct interval, like 1m, 1h or 1d.")

    (interval_number, interval_name) = match.groups()
    if not (interval_name.lower() == "m" or
            interval_name.lower() == "h" or
            interval_name.lower() == "d"):
        sys.exit("Please specify a correct interval, like 1m, 1h or 1d.")
    # elif len(sys.argv) >= 6:
        # Make for more environmentals.../make a dict from it

    print(interval_number, interval_name)
    print("Param check succeeded")

    lambda_deploy.deploy(dir_to_deploy, function_name, file_name, handler)
    lambda_schedule.schedule(function_name, interval_number, interval_name)


if __name__ == '__main__':
    deploy()

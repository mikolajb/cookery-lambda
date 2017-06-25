# todo: cron expression? check if function is already scheduled.
# Run like: python3 lambda_schedule.py getPod4 1 days

import aws_connect


# def get_params():
#     if len(sys.argv) < 4:
#         sys.exit("Please run as follows: python3 lambda_schedule.py "
#                  "--function_name --interval_number --interval_name")
#     elif len(sys.argv[1]) > 64:
#         sys.exit("Please specify a proper function name with max 64 "
#                  "characters.")
#     elif not sys.argv[2].isdecimal():
#         sys.exit("Please specify an integer.")
#     elif int(sys.argv[2]) == 0:
#         sys.exit("Please specify an integer greater than 0.")
#     elif not (sys.argv[3].lower() == "minutes" or
#               sys.argv[3].lower() == "hours" or
#               sys.argv[3].lower() == "days"):
#         sys.exit("Please name: minutes, hours or days.")

#     return (sys.argv[1], int(sys.argv[2]), sys.argv[3])


def check_interval(number, name):
    if name.lower() == "d" and number > 30:
        number = 30
    elif name.lower() == "h" and number > 23:
        number = 23
    elif name.lower() == "m" and number > 59:
        number = 59

    if name.lower() == "d":
        name = "days"
    elif name.lower() == "h":
        name = "hours"
    elif name.lower() == "m":
        name = "minutes"

    if number == 1:
        name = name[:-1]

    return (number, name)


# if __name__ == "__main__":
def schedule(function_name, interval_number, interval_name):
    interval_number = int(interval_number)
    (interval_number, interval_name) = check_interval(interval_number,
                                                      interval_name)
    rule_name = str(interval_number) + interval_name

    cloud_event_client = aws_connect.setup_client("events")

    # Check if a rule exists, when it does not, create one.
    if not aws_connect.check_existing_rules(cloud_event_client, rule_name):
        aws_connect.set_rule(cloud_event_client, rule_name,
                             interval_number, interval_name)

    aws_connect.apply_rule_to_function(cloud_event_client,
                                       rule_name, function_name)
    aws_connect.add_permission(function_name, rule_name, cloud_event_client)

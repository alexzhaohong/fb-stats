#!/usr/bin/python
import os
import json
import pdb

sender_name = "Kyle Goff"
message_dir = None
message_stats = {}

def calculate_basic_stats():
    global message_stats

    for message_type in os.listdir(message_dir):
        # Skip these for now, not interesting
        if message_type in ['filtered_threads', 'messages_requests', 'stickers_used']:
            continue

        # Navigate down to the user level
        message_type_path = os.path.join(message_dir, message_type)
        for user in os.listdir(message_type_path):
            user_path = os.path.join(message_type_path, user)

            # Track the names of the files used to combine after
            files_list = []
            user_messages = {}
            for json_file in os.listdir(user_path):
                json_path = os.path.join(user_path, json_file)

                # Skip anything that isn't a json file
                if os.path.splitext(json_file)[-1] != ".json":
                    continue

                # Load the json file into a dictionary for this user
                files_list.append(json_file)
                with open(json_path, "r") as json_open_file:
                    user_messages[json_file] = json.load(json_open_file)

            # Now go back through and collect stats on the user
            message_stats.update({"{}".format(user) : {}})
            message_stats[user].update({"Messages exchanged with {}:".format(user) : 0})
            message_stats[user].update({"Messages sent to {}:".format(user) : 0})
            for json_file in files_list:
                message_stats[user]["Messages exchanged with {}:".format(user)] += len(user_messages[json_file]['messages'])

                # Go through each message to see if script runner sent it
                # TODO I still think this is grabbing too many, might need another check
                for message in user_messages[json_file]['messages']:
                    if sender_name == message['sender_name']:
                        message_stats[user]["Messages sent to {}:".format(user)] += 1

    # Get total messages
    total_messages_sent = 0
    for user in message_stats.keys():
        total_messages_sent += message_stats[user]["Messages sent to {}:".format(user)]

    # Add generic stats to the dictionary
    message_stats.update({"generic" : {}})
    message_stats["generic"].update({"Total messages sent:" : total_messages_sent})
    print(total_messages_sent)


def calculate_bad_words():
    return None


def print_all(message_stats):
    print("WIP")


def analyze_all(dump_dir, intensity=0):
    global message_dir

    # Get the message directory to work with and save to this file
    message_dir = os.path.join(os.path.realpath(dump_dir), "messages")

    calculate_basic_stats()
    return message_stats
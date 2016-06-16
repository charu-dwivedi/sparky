#! /usr/bin/env python2
import utils
import speechtest as speech
import utilsvoiceblend as uvb
import summarizer
from Tkinter import StringVar

create_room_keywords = ["create", "make", "room"]
name_room_keywords = ["called"]
delete_room_keywords = ["delete"]
add_members_keywords = ["with", "add"]
schedule_meeting_keywords = ["schedule", "meeting", "follow up", "set up"]
change_room_name_keywords = ["change", "name", "rename"]
summarizer_keywords = ["summarize"]
transcript_keywords =["transcript"]

"""
Internal Functions
"""
def is_room_name(rooms, room_name, longer_room_name):
    if room_name not in rooms:
        return False

def translate_to_commands(user, user_input):
    room_name, title = '', ''
    for i in range(len(user_input)):
        input_word = user_input[i]
        if input_word in summarizer_keywords:
            processed = process_for_summarize(user, user_input, i)
            if processed != None:
                return summarizer.summarize(user, processed[0], processed[1], processed[2], processed[3], processed[4])
        if input_word in transcript_keywords:
            processed = process_for_transcript(user, user_input, i)
            if processed != None:
                return summarizer.get_transcript(user, processed[0], processed[1], processed[2], processed[3])

# returns a (room_name, days_limit, hours_limit, minutes_limit)
def process_for_transcript(user, user_input, i):
    rooms = utils.get_all_rooms(user)
    room_name, potential_room_name, i2, = '', user_input[i+1], i
    if potential_room_name in rooms:
        if i + 1 < len(user_input):
            longer_potential_room_name = potential_room_name + user_input[i+1]
            if longer_potential_room_name not in rooms:
                i2 = i + 1
                room_name = potential_room_name
        else:
            i2 = i + 1
            room_name = potential_room_name
            return (room_name, None, None, None)
    else:
        for j in range(i+2, len(user_input)):
            potential_room_name += ' ' + user_input[j]
            if potential_room_name in rooms:
                if j + 1 < len(user_input):
                    longer_potential_room_name = potential_room_name + user_input[j+1]
                    if longer_potential_room_name not in rooms:
                        i2 = j + 1
                        room_name = potential_room_name
                        break
                else:
                    i2 = j + 1
                    room_name = potential_room_name
                    return (room_name, None, None, None)
   
    days_limit, hours_limit, minutes_limit = None, None, None
    return (room_name, days_limit, hours_limit, minutes_limit)

# returns a (room_name, days_limit, hours_limit, minutes_limit, title)
def process_for_summarize(user, user_input, i):
    rooms = utils.get_all_rooms(user)
    room_name, potential_room_name, i2, = '', user_input[i+1], i
    if potential_room_name in rooms:
        if i + 1 < len(user_input):
            longer_potential_room_name = potential_room_name + user_input[i+1]
            if longer_potential_room_name not in rooms:
                i2 = i + 1
                room_name = potential_room_name
        else:
            i2 = i + 1
            room_name = potential_room_name
            return (room_name, None, None, None, None)
    else:
        for j in range(i+2, len(user_input)):
            potential_room_name += ' ' + user_input[j]
            if potential_room_name in rooms:
                if j + 1 < len(user_input):
                    longer_potential_room_name = potential_room_name + user_input[j+1]
                    if longer_potential_room_name not in rooms:
                        i2 = j + 1
                        room_name = potential_room_name
                        break
                else:
                    i2 = j + 1
                    room_name = potential_room_name
                    return (room_name, None, None, None, None)
    title = ''
    for j in range(i2, len(user_input)):
        if user_input[j] == 'as':
            continue
        title += user_input[j]

    if title == '':
        title = None
    days_limit, hours_limit, minutes_limit = None, None, None
    return (room_name, days_limit, hours_limit, minutes_limit, title)

def create_room_dialog(room_name_added, room_members_added, text, room_name="", room_members=[]):
    room_id = ""
    if room_name_added:
        room_id = utils.make_room('charu', room_name)
    else:
        name_prompt = "What would you like to name your room?"
        speech.speech_play_test(name_prompt)
        while not room_name:
            room_name = speech.speechrec()
        room_id = utils.make_room('charu', room_name) 
    if room_members_added:
        utils.add_members('charu', room_name, room_members)
    else:
        ask_add_members = "Would you like to add members?"
        speech.speech_play_test(ask_add_members)
        resp = ""
        while not resp:
            resp = speech.speechrec()
        if 'n' in resp.lower():
            no_response = "Ok, " + room_name + "has been created"
            speech.speech_play_test(no_response)
        if 'y' in resp.lower():
            yes_response = "Ok, please name your members"
            speech.speech_play_test(yes_response)
            new_members = []
            while not new_members:
                new_members = speech.speechrec()
            new_members_array = new_members.split()
            print new_members_array
            new_member_email = uvb.find_members_voice('charu', new_members_array, text)
            print new_member_email
            utils.add_members_with_room_id('charu', room_id, new_member_email)
            added_members_response = "Members have ben added to " + room_name 
            speech.speech_play_test(added_members_response)

"""
Call process to use langprocess
"""
def process(user, user_input, text):
    room_caller = 0
    for words in create_room_keywords:
        if words in user_input.lower():
            room_caller += 1 
    if room_caller == 2:
        create_room_dialog(False, False, user_input)
    print user_input.lower()
    print translate_to_commands(user, user_input.lower().split())

# process('chris', 'chris tanay beast beast transcript Ping Pong SJ-29 peanut')

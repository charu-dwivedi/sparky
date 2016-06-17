#! /usr/bin/env python2
import utils
import speechtest as speech
import utilsvoiceblend as uvb
import summarizer
from Tkinter import StringVar
import meeting_scheduler as ms


create_room_keywords = ["create", "make", "room"]
name_room_keywords = ["called"]
delete_room_keywords = ["delete"]
add_members_keywords = ["with", "add"]
schedule_meeting_keywords = ["schedule", "meeting", "follow up", "set up"]
rename_room_keywords = ["change", "name", "rename", 'reading'] #lol
rename_room_transition_keywords = ['as', 'to']
summarizer_keywords = ["summarize", "summarized", "sunrise"] # lol
transcript_keywords = ["transcript", "transcribe"]

"""
Internal Functions
"""
def isInt(stringInt):
    try: 
        int(stringInt)
        return True
    except ValueError:
        return False

# tries to find a room name building from index i
# returns None if fails
def get_room_name(user_input, rooms, i):
    if i >= len(user_input):
        return None

    potential_room_name = user_input[i]
    if potential_room_name in rooms:
        if i + 1 < len(user_input):
            longer_potential_room_name = potential_room_name + ' ' + user_input[i+1]
            if longer_potential_room_name not in rooms:
                return (potential_room_name, i+1)
        else:
            return (potential_room_name, i+1)

    for j in range(i+1, len(user_input)):
        potential_room_name += ' ' + user_input[j]
        if potential_room_name in rooms:
            if j + 1 < len(user_input):
                longer_potential_room_name = potential_room_name + ' ' + user_input[j+1]
                if longer_potential_room_name not in rooms:
                    return (potential_room_name, j+1)
            else:
                return (potential_room_name, j+1)
    return None

# looks for time in user_input starting from index i
def get_time(user_input, i):
    if i >= len(user_input):
        return None

    days_limit, hours_limit, minutes_limit = None, None, None
    time, unit = -1, None
    potential = ''
    for j in range(i, len(user_input)):
        word = user_input[j]
        if word == 'yesterday':
            time, unit = 1, 'day'
            break;
        elif word == 'next':
            potential = 'next'
            continue
        elif word == 'week':
            if potential == 'next':
                time, unit = 7, 'day'
                break;
            else:
                time *= 7
                unit = 'day'
                break;
        elif isInt(word):
            time = int(word)
        elif word == 'day' or word == 'days':
            unit = 'day'
        elif word == 'hour' or word == 'hours':
            unit = 'hour'
        elif word == 'minute' or word == 'minutes' or word == 'min':
            unit = 'min'
        else:
            potential = ''
    if time > 0 and unit:
        if unit == 'day':
            days_limit = time
        elif unit == 'hour':
            hours_limit = time
        else:
            minutes_limit = time

    print 'days limit: ' + str(days_limit)
    print 'hours limit: ' + str(hours_limit)
    print 'minutes limit: ' + str(minutes_limit)
    return (days_limit, hours_limit, minutes_limit)

"""
Summarizer Functions
"""
def translate_to_commands(user, user_input):
    """
    Function does what process does but for summarize and transcript
    The magic numbers in summarize and get_transcript are arbitrary
    max messages we get--we do this b/c if not specified, the Spark API
    assumes a limit of 50
    """
    for i in range(len(user_input)):
        input_word = user_input[i]
        if input_word in summarizer_keywords:
            processed = get_room_name_and_time_limits(user, user_input, i+1)
            if processed is not None:
                print 'Summarized ' + str(processed)
                return summarizer.summarize(user, processed[0], 100, processed[1], processed[2], processed[3])
        if input_word in transcript_keywords:
            processed = get_room_name_and_time_limits(user, user_input, i+1)
            if processed is not None:
                print 'Transcript ' + str(processed)
                return summarizer.get_transcript(user, processed[0], 500, processed[1], processed[2], processed[3])
        if input_word in rename_room_keywords:
            processed = process_for_rename_room(user, user_input, i+1)
            if processed is not None:
                print 'Rename ' + str(processed)
                utils.rename_room(user, processed[0], processed[1])
                return True
    return False

# returns a (room_name, days_limit, hours_limit, minutes_limit)
def get_room_name_and_time_limits(user, user_input, i):
    if i >= len(user_input):
        return None

    room_name_and_next_index = get_room_name(user_input, utils.get_all_rooms(user), i)
    if room_name_and_next_index is None:
        return None
    room_name, i2 = room_name_and_next_index

    if i2 >= len(user_input):
        return (room_name, None, None, None)
    """
    # Title doesn't do anything in summarizer
    title = ''
    for j in range(i2, len(user_input)):
        if user_input[j] == 'as':
            continue
        title += user_input[j]

    if title == '':
        title = None
    """
    days_limit, hours_limit, minutes_limit = get_time(user_input, i2)
    return (room_name, days_limit, hours_limit, minutes_limit)

"""
Room Command Functions
"""
def process_for_rename_room(user, user_input, i):
    if i >= len(user_input):
        return None
    rooms = utils.get_all_rooms(user)
    room_name_and_next_index = get_room_name(user_input, rooms, i)
    if room_name_and_next_index is None:
        return None
    room_name, i2 = room_name_and_next_index
    if i2+1 >= len(user_input) or user_input[i2] not in rename_room_transition_keywords:
        return None
    i2 += 1
    new_room_name = ''
    while i2 < len(user_input):
        new_room_name += user_input[i2] + ' '
        i2 += 1
    return (room_name, new_room_name.rstrip())

def check_name_room_true(user_input):
    input_arr = (user_input.lower()).split()
    for x in range(len(input_arr)):
        # if input_arr[x] in name_room_keywords:
        if name_room_keywords[0] == input_arr[x]:
            if x < (len(input_arr)-1):
                return input_arr[x+1]
    return

def check_add_members_true(user_input):
    member_arr = []
    input_arr = (user_input.lower()).split()
    not_lower_case_input_arr = user_input.split()
    for keyword in add_members_keywords:
        for x in range(len(input_arr)):
            if keyword == input_arr[x]:
                for y in range(x+1, len(input_arr)):
                    if not (not_lower_case_input_arr[y] == "and"):
                        if (not_lower_case_input_arr[y] == "called"):
                            return member_arr
                        member_arr.append(not_lower_case_input_arr[y])
                        print member_arr
                return member_arr

def create_room_dialog(room_name_added, room_members_added, room_name="", room_members=[]):
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
        new_member_email = uvb.find_members_voice('charu', room_members)
        utils.add_members_with_room_id('charu', room_id, new_member_email)
        added_response = "Ok, " + room_name + "has been created with members"
        speech.speech_play_test(added_response)
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
            new_member_email = uvb.find_members_voice('charu', new_members_array)
            print new_member_email
            utils.add_members_with_room_id('charu', room_id, new_member_email)
            added_members_response = "Members have ben added to " + room_name
            speech.speech_play_test(added_members_response)

def schedule_meeting_dialog(start, end, attendees=[]):
    # users = [("Tanay Nathan", "tanathan@cisco.com")]
    speech.speech_play_test("What room would you like to invite?")
    if len(attendees) == 0:
        ms.schedule(users, start, end)
        speech.speech_play_test("Ok, created meeting.")
        return "Ok, created meeting."
    else:
        for attendee in attendees:
            users += utils.find_members(utils.developer_tokens['tanay'], attendee)
        ms.schedule(users, start, end)

"""
Main function for langprocess
Interface between voice and execution of commands 
"""
def process(user_input, user='charu'):
    output = None
    try:
        output = translate_to_commands(user, user_input.lower().split())
    except Exception as e:
        print 'Not summarize or transcript'
    try:
        if output:
            output = output.encode('ascii', 'ignore')
            with open('summary.txt', 'w') as f:
                f.write(output)
            print 'wrote summary'
    except Exception as e:
        print output

    for words in create_room_keywords:
        if words in user_input.lower():
            room_name_true = False
            room_name = check_name_room_true(user_input)
            added_members_true = False
            added_members = check_add_members_true(user_input)
            if room_name:
                room_name_true = True
            if added_members:
                added_members_true = True
            create_room_dialog(room_name_true, added_members_true, room_name, added_members)
            break
    for words in schedule_meeting_keywords:
        if words in user_input.lower():
            return schedule_meeting_dialog("2016-08-10T13:00:00","2016-08-10T14:00:00")

"""
Test calls
"""
# process('konichiwa charu-sama summarize hacker next week tanananay')
# process('konichiwa charu-sama summarize hacker group 2 days ago tanananay')
# process('konichiwa charu-sama transcribe hacker group 2 days ago tanananay')
# process('chris tanay beast beast transcript Ping Pong SJ-29 3 days peanut', 'chris')
# process('filler filler rename hacker to abandoned hacker', 'chris')

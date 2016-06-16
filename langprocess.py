#! /usr/bin/env python2
import utils
import speechtest as speech
import utilsvoiceblend as uvb
import summarizer
from Tkinter import StringVar
import meeting_scheduler as ms


create_room_keywords = ["create", "make", "room"]
name_room_keywords = "called"
delete_room_keywords = ["delete"]
add_members_keywords = ["with", "add"]
schedule_meeting_keywords = ["schedule", "meeting", "follow up", "set up"]
change_room_name_keywords = ["change", "name", "rename"]
summarizer_keywords = ["summarize", "summarized", "sunrise"] # lol
transcript_keywords =["transcript", "transcribe"]

"""
Internal Functions
"""
def is_room_name(rooms, room_name, longer_room_name):
    if room_name not in rooms:
        return False

def isInt(stringInt):
    try: 
        int(stringInt)
        return True
    except ValueError:
        return False

def get_days(user_input, index):
    days_limit, hours_limit, minutes_limit = None, None, None
    time, unit = -1, None
    potential = ''
    for j in range(index, len(user_input)):
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
        elif  word == 'day' or word == 'days':
            unit = 'day'
        elif word == 'hour' or 'hours':
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
    """
    room_name, title = '', ''
    for i in range(len(user_input)):
        input_word = user_input[i]
        if input_word in summarizer_keywords:
            processed = process_for_summarize(user, user_input, i)
            if processed != None:
                return summarizer.summarize(user, processed[0], 100, processed[1], processed[2], processed[3])
        if input_word in transcript_keywords:
            processed = process_for_transcript(user, user_input, i)
            if processed != None:
                return summarizer.get_transcript(user, processed[0], 300, processed[1], processed[2], processed[3])

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

    days_limit, hours_limit, minutes_limit = get_days(user_input, i2)
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
    days_limit, hours_limit, minutes_limit = get_days(user_input, i2)
    return (room_name, days_limit, hours_limit, minutes_limit)

"""
Room Command Functions
"""
def check_name_room_true(user_input):
    input_arr = (user_input.lower()).split()
    for x in range(len(input_arr)):
        if name_room_keywords == input_arr[x]:
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
def process(user_input):
    try:
        with open('summary.txt', 'w') as f:
            f.write(translate_to_commands('charu', user_input.lower().split()))
    except Exception as e:
        print 'Not summarize or transcript'
    else:
        print translate_to_commands('charu', user_input.lower().split())
    finally:
        print 'Not summarize or transcript'

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
process('konichiwa charu-sama summarize hacker 2 days from now tanananay')
# process('chris', 'chris tanay beast beast transcript Ping Pong SJ-29 peanut')
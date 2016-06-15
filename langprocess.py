#! /usr/bin/env python2
import utils
import speechtest as speech

def process(user_input):
    create_room_keywords = ["create"]
    name_room_keywords = ["called"]
    delete_room_keywords = ["delete"]
    add_members_keywords = ["with", "add"]
    schedule_meeting_keywords = ["schedule", "meeting", "follow up", "set up"]
    change_room_name_keywords = ["change", "name", "rename"]
    summarizer_keywords = ["summarize"]
    for words in create_room_keywords:
        if words in user_input.lower():
            create_room_dialog(False, False)


def create_room_dialog(room_name_added, room_members_added, room_name="", room_members=[]):
    if room_name_added:
        utils.make_room('charu', room_name)
    else:
        name_prompt = "What would you like to name your room?"
        speech.speech_play_test(name_prompt)
        while not room_name:
            room_name = speech.speechrec()
        utils.make_room('charu', room_name)
    if room_members_added:
        utils.add_members('charu', room_name, room_members)
    else:
        ask_add_members = "Would you like to add members?"
        speech.speech_play_test(ask_add_members)
        while not resp:
            resp = speech.speechrec()
        if 'n' in resp.lower():
            no_response = "Ok, " + room_name + "has been created"
            speech.speech_play_test(no_response)
        if 'y' in resp.lower():
            yes_response = ""

def create_room_dialog(room_name_added, room_name="", room_members_added=0, room_members=[]):
	if room_name_added:
		utils.make_room('charu', room_name)
	else:
		name_prompt = "What would you like to name your room?"
		speech.speech_play_test(name_prompt)
		room_name = speech.speechrec()
		utils.make_room('charu', room_name)
	if room_members_added:
		utils.add_members('charu', room_name, )

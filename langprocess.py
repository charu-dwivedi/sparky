#! /usr/bin/env python2
import utils
import speechtest as speech
import utilsvoiceblend as uvb
from Tkinter import StringVar

def process(user_input, text):
    create_room_keywords = ["create", "make", "room"]
    name_room_keywords = ["called"]
    delete_room_keywords = ["delete"]
    add_members_keywords = ["with", "add"]
    schedule_meeting_keywords = ["schedule", "meeting", "follow up", "set up"]
    change_room_name_keywords = ["change", "name", "rename"]
    summarizer_keywords = ["summarize"]
    room_caller = 0
    for words in create_room_keywords:
        if words in user_input.lower():
            room_caller +=1
    if room_caller == 2:
        create_room_dialog(False, False, text)


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
            utils.add_members('charu', room_id, new_member_email)
            added_members_response = "Members have ben added to " + room_name 
            speech.speech_play_test(added_members_response)

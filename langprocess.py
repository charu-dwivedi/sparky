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


def create_room_dialog(room_name_added, room_name="", room_members_added, room_members=[]):
	if room_name_added:
		utils.make_room('charu', room_name)
	else:
		name_prompt = "What would you like to name your room?"
		speech.speech_play_test(name_prompt)
		room_name = speech.speechrec()
		utils.make_room('charu', room_name)
	if room_members_added:
		utils.add_members('charu', room_name, )




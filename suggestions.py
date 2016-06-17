with open('suggested_users.json') as sugg:
    sugg_users = json.load(sugg)

def check_suggested_members(member_name):
    if member_name in sugg_users:
        if (len(sugg_users[member_name])>1):
            print "Did you mean one of these? "
            count =1
            for suggested_member in sugg_users[member_name]:
                print count + ": "+ suggested_member[0]
                print "   " + suggested_member[1]
            num = raw_input("Respond with a number: ")
            return sugg_users[member_name][num-1][1]
        else:
            return sugg_users[member_name][0][1]
    else:
        return 0
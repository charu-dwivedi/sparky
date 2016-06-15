import requests
import json

AUTHENTICATION_KEY="Bearer MzYwODVlM2QtMzg5Yy00MzI5LWFkMzYtYzg5NzE0MGJhM2M5MTlkZGQ4OGUtOWI5"

def update(oldname, newname):
            
            search_url = 'https://api.ciscospark.com/v1/rooms'

            headers = {
                'Authorization': AUTHENTICATION_KEY
            }

            rooms = requests.get(search_url, headers=headers).json()

            rcount = len(rooms['items'])
            roomID = 0
     
            for i in range(rcount):

                
                roomTitle = rooms['items'][i]['title']
                
                if roomTitle == oldname:
                    roomID = rooms['items'][i]['id']
                    
                  
                if roomID != 0:
                    update_url = 'https://api.ciscospark.com/v1/rooms/%s' %roomID

                    params = {
                        'title': newname
                        }

                    update = requests.put(update_url, headers = headers, data = params).json()
                 
            if roomID == 0:
                print 'No room found'
 
            else:
                print 'Room updated'

oname = raw_input('Room to be updated: ')
nname = raw_input('Enter new name: ')

update(oname, nname)

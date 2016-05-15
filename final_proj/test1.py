# from firebase import firebase
# firebase = firebase.FirebaseApplication('https://ece5990.firebaseio.com', None)
# result = firebase.get('/users', None)
# print result



# new_user = 'Ozgur Vatansever'
# dict1 = {'print': 'pretty'}
# dict2 = {'X_FANCY_HEADER': 'VERY FANCY'}

# result = firebase.post(('/users', (new_user, dict1, dict2)))
# print result
# {u'name': u'-Io26123nDHkfybDIGl7'}

# result = firebase.post('/users', new_user, {'print': 'silent'}, {'X_FANCY_HEADER': 'VERY FANCY'})
# print result == None
# # True

import subprocess
import sys
import datetime
import socket


from firebase.firebase import FirebaseApplication, FirebaseAuthentication

ON_RPI = False if sys.platform.find('darwin') > -1 else True

def postIP():

    SECRET = 'D9H4yWL1t3AhHs4kMiLUZYyo4LtemKyj39me0heV'
    DSN = 'https://ece5990.firebaseio.com'
    EMAIL = 'zyren00@gmail.com'
    authentication = FirebaseAuthentication(SECRET,EMAIL, True, True)
    firebase = FirebaseApplication(DSN, authentication)

    firebase.get('/ip', None,
                 params={'print': 'pretty'},
                 headers={'X_FANCY_HEADER': 'very fancy'})

    # data = {'name': 'Ozgur Vatansever', 'age': 26,            'created_at': datetime.datetime.now()}
    try:
        if ON_RPI:
            cmd = "ifconfig |grep 'inet addr:10.'"
            line =  subprocess.check_output(cmd, shell=True)
            colon = line.find(':')
            Bcast = line.find('Bcast')
            ip = line[colon+1:Bcast].strip()
        else:
            # cmd = "ifconfig |grep 'inet '"
            # line =  subprocess.check_output(cmd, shell=True)
            # netmask = line.find('netmask')
            # ten = line.find('inet')
            ip = socket.gethostbyname(socket.gethostname())

    except Exception as e:
    	print e
    
    firebase.delete('/ip', None)

    data = {'ip' : ip, 'time': datetime.datetime.now()}

    snapshot = firebase.post('/ip', data)
    print 'IP', ip, 'posted to firebase'

    def callback_get(response):
        # with open('/dev/null', 'w') as f:
        #     f.write(response)
        # print(response)
        pass
    firebase.get_async('/ip', snapshot['name'], callback=callback_get)
if __name__ == '__main__':
    postIP()
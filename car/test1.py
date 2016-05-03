from firebase import firebase
firebase = firebase.FirebaseApplication('https://ece5990.firebaseio.com', None)
result = firebase.get('/users', None)
print result
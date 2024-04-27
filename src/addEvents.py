import os, requests, random

def addEvents():
    URL_addEvent = 'http://localhost:5000/api/add_event'
    URL_register = 'http://localhost:5000/api/register'
    URL_login = 'http://localhost:5000/api/login'

    data = {
        "email": os.urandom(4).hex() + "@tests.com",
        "password": (password := os.urandom(8).hex()),
        "password_confirm": password
    }

    r = requests.post(URL_register, data=data, allow_redirects=True)
    assert r.status_code == 200 and r.url == 'http://localhost:5000/api/login'
    data.pop("password_confirm")
    s = requests.Session()
    r = s.post(URL_login, data=data, allow_redirects=True)
    assert r.status_code == 200 and r.url == 'http://localhost:5000/api/dashboard'

    categories = ["Mutuo", "Consulenza", "Assicurazione", "Investimento", "Apertura conto", "Chiusura conto", "Consulenza finanziaria"]
    for e in range(1, 31):
        i = 830
        while i < 1700:
            new_hour = i + 30

            if not random.randint(0, 1):
                i = (new_hour if new_hour % 100 < 60 else (new_hour // 100 + 1) * 100)
                continue
            
            s.post(URL_addEvent, json={
                'date' : f'2024-05-{e}',
                'start_hour' : i, 
                'end_hour' : (i := (new_hour if new_hour % 100 < 60 else (new_hour // 100 + 1) * 100)), 
                'category' : f'{categories[random.randint(0, len(categories))]}', 'operator_id' : 1
            })
            assert r.status_code == 200
            
if __name__ == '__main__':
    try:
        addEvents()
        print("Events added successfully")
    except Exception as e:
        print(f"Error in adding evnents: {e}")
import os, requests, random

def addEvents():
    URL_addEvent = "http://localhost/api/add_event"
    URL_register = "http://localhost/api/register"
    URL_login = "http://localhost/api/login"

    data = {
        "email": os.urandom(4).hex() + "@tests.com",
        "password": (password := os.urandom(8).hex()),
        "password_confirm": password
    }

    r = requests.post(URL_register, data=data, allow_redirects=True)
    assert r.status_code == 200 and r.url == "http://localhost/login"
    data.pop("password_confirm")
    s = requests.Session()
    r = s.post(URL_login, data=data, allow_redirects=True)
    assert r.status_code == 200 and r.url == "http://localhost/dashboard"

    categories = ["Mutuo", "Consulenza", "Assicurazione", "Investimento", "Apertura conto", "Chiusura conto", "Consulenza finanziaria"]
    i = 830
    while i < 1700:
        new_hour = i + 30
        if str(i)[:-2] == '60':
            i += 40

        r.post(URL_addEvent, json={'date' : f'2024-05-{random.randint(1,30)}', 'start_hour' : i, 'end_hour' : (i := (new_hour if new_hour % 100 < 60 else (new_hour // 100 + 1) * 100)), 'category' : f'{categories[random.randint(0, len(categories))]}', 'operator_id' : 1})
        assert r.status_code == 200

        i += 30
        
if  __name__ == '__main__':
    addEvents()
    print('Events added successfully.')
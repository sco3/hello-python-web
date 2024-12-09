import time
import uuid
import requests
import json


def main():
    # Everything is good when payload is small
    huge_payload = ""
    array = []
    for i in range(100000):
        array.append(str(uuid.uuid4()))

    huge_payload = json.dumps(array)

    # Send request each 1 second reusing single connection (without connection reuse it works well)
    with requests.Session() as session:
        while True:
            try:
                response = session.post("http://127.0.0.1:8000", huge_payload)
                print(
                    response.text
                )  # server will be responding with either 'OK' or 'FAIL'

                # In case if server reports 'FAIL' - we reproduced the issue and are OK to exit
                if response.text == "FAIL":
                    break

            except KeyboardInterrupt:
                break

            except BaseException as ex:
                print(str(ex))

            time.sleep(0.1)


if __name__ == "__main__":
    main()

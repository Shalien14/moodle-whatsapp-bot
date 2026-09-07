def fetch_notifications(session, sesskey, userid):
    service_url = "https://online.uom.lk/lib/ajax/service.php"

    payload = {
        "index": 0,
        "methodname": "message_popup_get_popup_notifications",
        "args": {
            "limit": 20,
            "offset": 0,
            "useridto": str(userid)
        }
    }

    params = {
        "sesskey": sesskey
    }

    response = session.post(
        service_url,
        params=params,
        json=[payload]
    )

    response.raise_for_status()

    result = response.json()

    if result[0]["error"]:
        raise Exception(result[0]["exception"]["message"])

    data = result[0]["data"]

    return data["notifications"], data["unreadcount"]
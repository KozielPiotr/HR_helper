def login(client, username, password):
    resp = client.post("/login", data=dict(username=username, password=password), follow_redirects=True)
    return resp

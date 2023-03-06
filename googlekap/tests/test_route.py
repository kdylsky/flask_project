def test_auth(client):
    r = client.get(
        "/auth",
        follow_redirects=True
    )
    assert r.status_code == 200

    r = client.get(
        "/auth/register",
        follow_redirects=True #리다이렉션이 되면 그 주소를 따라가고, 해당 response값을 가지고 온다. 최종적인 return값을 이용한다는 의미
    )
    assert r.status_code == 200

    r = client.get(
        "/auth/login",
        follow_redirects=True
    )
    assert r.status_code == 200

    r = client.get(
        "/auth/logout",
        follow_redirects=True
    )
    assert r.status_code == 200

def test_base(client):
    r = client.get(
        "/",
        follow_redirects = True
    )
    assert r.status_code == 200
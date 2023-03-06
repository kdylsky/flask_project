def test_get_users(client):
    r = client.get("/api/users", follow_redirects=True)
    assert r.status_code == 200
    assert len(r.json) == 1


def test_get_user(client, user_data):
    r = client.get("api/users/1", follow_redirects=True)
    assert r.status_code == 200
    assert r.json.get("user_id") == user_data.get("user_id")
    assert r.json.get("user_name") == user_data.get("user_name")


def test_post_user(client, user_data):
    r = client.post("api/users", data=user_data)
    assert r.status_code == 409  # 유저 아이디는 유닉크하기 때문에 에러가 난다.

    # 새로운 유저 데이터 생성
    new_user_data = user_data.copy()
    new_user_data["user_id"] = "test_id2"
    r = client.post("api/users", data=new_user_data)
    assert r.status_code == 201

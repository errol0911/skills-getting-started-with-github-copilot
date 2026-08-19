def test_unregister_removes_participant(client):
    email = "sophia@mergington.edu"

    response = client.delete("/activities/Programming%20Class/unregister", params={"email": email})

    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from Programming Class"

    activities = client.get("/activities").json()
    assert email not in activities["Programming Class"]["participants"]


def test_unregister_unknown_activity_returns_404(client):
    response = client.delete(
        "/activities/Unknown%20Club/unregister", params={"email": "student@mergington.edu"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_non_participant_returns_404(client):
    response = client.delete(
        "/activities/Chess%20Club/unregister", params={"email": "notenrolled@mergington.edu"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_unregister_missing_email_returns_422(client):
    response = client.delete("/activities/Chess%20Club/unregister")

    assert response.status_code == 422

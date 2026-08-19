def test_signup_then_unregister_updates_activity_participants(client):
    email = "workflow@mergington.edu"

    signup_response = client.post("/activities/Tennis%20Club/signup", params={"email": email})
    assert signup_response.status_code == 200

    activities_after_signup = client.get("/activities").json()
    assert email in activities_after_signup["Tennis Club"]["participants"]

    unregister_response = client.delete("/activities/Tennis%20Club/unregister", params={"email": email})
    assert unregister_response.status_code == 200

    activities_after_unregister = client.get("/activities").json()
    assert email not in activities_after_unregister["Tennis Club"]["participants"]


def test_unregistering_same_participant_twice_returns_404_second_time(client):
    email = "alex@mergington.edu"

    first_response = client.delete("/activities/Basketball%20Team/unregister", params={"email": email})
    assert first_response.status_code == 200

    second_response = client.delete("/activities/Basketball%20Team/unregister", params={"email": email})
    assert second_response.status_code == 404
    assert second_response.json()["detail"] == "Student is not signed up for this activity"


def test_signup_does_not_enforce_max_participants_current_behavior(client):
    base_activities = client.get("/activities").json()
    max_participants = base_activities["Chess Club"]["max_participants"]
    initial_count = len(base_activities["Chess Club"]["participants"])

    extra_signups = max_participants - initial_count + 1
    for idx in range(extra_signups):
        response = client.post(
            "/activities/Chess%20Club/signup", params={"email": f"overflow{idx}@mergington.edu"}
        )
        assert response.status_code == 200

    activities = client.get("/activities").json()
    final_count = len(activities["Chess Club"]["participants"])
    assert final_count > max_participants

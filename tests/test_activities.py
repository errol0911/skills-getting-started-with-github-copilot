def test_get_activities_returns_expected_dictionary(client):
    response = client.get("/activities")

    assert response.status_code == 200
    activities = response.json()
    assert isinstance(activities, dict)
    assert len(activities) == 9
    assert "Chess Club" in activities


def test_each_activity_contains_expected_fields(client):
    response = client.get("/activities")
    activities = response.json()

    expected_fields = {"description", "schedule", "max_participants", "participants"}
    for activity in activities.values():
        assert expected_fields.issubset(activity.keys())
        assert isinstance(activity["participants"], list)

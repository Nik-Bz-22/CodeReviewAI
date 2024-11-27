from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_review_code():
    response = client.post(
        "/review/",
        json={
        "github_repo_url": "https://github.com/Nik-Bz-22/SCA",
        "assignment_description": """# Python engineer test assessment - the Spy Cat Agency  ### Overview  This task involves building a CRUD application. The goal is to create a system that showcases your understanding in building RESTful APIs, interacting with SQL-like databases, and integrating third-party services. The test assessment is expected to be done within 2 hours.  ### Requirements  Spy Cat Agency (SCA) asked you to create a management application, so that it simplifies their spying work processes. SCA needs a system to manage their cats, missions they undertake, and targets they are assigned to.  From cats perspective, a mission consists of spying on targets and collecting data. One cat can only have one mission at a time, and a mission assumes a range of targets (minimum: 1, maximum: 3). While spying, cats should be able to share the collected data into the system by writing notes on a specific target. Cats will be updating their notes from time to time and eventually mark the target as complete. If the target is complete, notes should be frozen, i.e. cats should not be able to update them in any way. After completing all of the targets, the mission is marked as completed.  From the agency perspective, they regularly hire new spy cats and so should be able to add them to and visualize in the system. SCA should be able to create new missions and later assign them to cats that are available. Targets are created in place along with a mission, meaning that there will be no page to see/create all/individual targets.  **Backend Requirements:**  - **Spy Cats**     - Ability to create a spy cat in the system         - A cat is described as Name, Years of Experience, Breed, and Salary.         - Breed must be validated, see General     - Ability to remove spy cats from the system     - Ability to update spy cats’ information (Salary)     - Ability to list spy cats     - Ability to get a single spy cat - **Missions / Targets**     - Ability to create a mission in the system along with targets in one single request         - A mission contains information about Cat, Targets and Complete state         - Each target is unique to a mission, so the endpoint should accept an object describing targets         - A target is described as Name, Country, Notes and Complete state     - Ability to delete a mission         - A mission cannot be deleted if it is already assigned to a cat     - Ability to update mission targets         - Ability to mark it as completed         - Ability to update Notes             - Notes cannot be updated if either the target or the mission is completed     - Ability to assign a cat to a mission     - Ability to list missions     - Ability to get a single mission - **General**     - Framework         - Use any of: FastAPI, Django     - Database         - You can use any database     - Validations         - Make sure endpoints validate the request body and return an adequate status code if it’s not valid         - Validate cat’s breed with [TheCatAPI](https://api.thecatapi.com/v1/breeds)  ### Sharing the results  - Make a repository on Github - Add a README explaining how to build/start the application. Include any information you think will be useful for us - Define all of the endpoints in a Postman collection and add link to it in the README - As you have the repository in place, share a link to it with our recruiter. We will review it within 5-7 business days and return with a feedback - Don't hesitate to ask any questions  Thank you!""",
        "candidate_level": "Junior"
        },
    )
    resp_json = response.json()["review"]
    assert response.status_code == 200
    assert resp_json
    assert resp_json["files"]
    assert  resp_json["downsides"]
    assert  resp_json["comments"]
    assert  resp_json["rating"]
    assert  resp_json["conclusion"]



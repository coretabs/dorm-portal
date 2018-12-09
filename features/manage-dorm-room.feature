Feature: Managing dormitory and room data

    Scenario: As a manager 
              I want to manage my dorms and its rooms
              So that I can offer them for students

        Given two managers (one for alfam&dovec and one for homedorm)
        Given we have dorms(alfam & dovec & homedorm) + 2 rooms in alfam

        When hitting GET /manager/dorms endpoint
        Then get 200 OK with alfam and dovec
        And he wont get any other non-owned dorm data


        

        When manager asks serializer to bring alfam dorm data
        Then get valid serialized alfam data for the manager

        When hitting GET /manager/dorms/{alfam-id}
        Then get 200 OK with alfam

        When hitting GET /manager/dorms/{homedorm-id} for non-owned dorm
        Then get forbidden 403 for homedorm
        And the other manager can get his homedorm




        When deserializing data for updating alfam dorm
        Then validate the deserialized data for updating alfam

        When hitting PUT /manager/dorms/{alfam-id} to update history
        Then get 200 OK for updating alfam

        When deleting a photo for alfam dorm
        Then getting alfam with the deleted photo
        And bring that deleted alfam photo again

        When hitting DELETE /manager/dorms/{alfam-id}/photos/{id}
        Then delete that photo from alfam

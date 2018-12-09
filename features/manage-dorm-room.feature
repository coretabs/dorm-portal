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



        When deserializing bank data for alfam
        Then validate the deserialized bank data for alfam

        When hitting PUT /manager/dorms/{alfam-id}/bank-accounts/{isbank-id}
        Then get 200 OK and for updating alfam isbank data

        when hitting same endpoint above to partially update isbank
        Then get 200 OK and for partially updating alfam isbank data
        
        When hitting POST /manager/dorms/{alfam-id}/bank-accounts
        Then get 201 CREATED and for adding alfam ziraat data

        When hitting POST DELETE /manager/dorms/{alfam-id}/bank-accounts/{ziraat-id}
        Then get 204 NO CONTENT and for deleting alfam ziraat bank




        When hitting POST /manager/dorms/{alfam-id}/photos
        Then get 201 CREATED and for adding alfam photo

        When hitting DELETE /manager/dorms/{alfam-id}/photos/{alfam-photo-id}
        Then delete that photo from alfam




        When deserializing data for updating alfam dorm
        Then validate the deserialized data for updating alfam

        When hitting PUT /manager/dorms/{alfam-id}
        Then get 200 OK for updating alfam

        

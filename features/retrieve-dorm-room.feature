Feature: Retrieving dormitory data

    Scenario: As a user 
              I want to get all the dormitory data
              So that I can know what they offer

        Given we have 2 dormitories with 2 rooms each

        When serializing alfam to get its all data
        Then get valid serialized alfam data with 2 rooms

        When hitting GET /dorms/{alfam-id} endpoint
        Then get 200 OK with alfam data
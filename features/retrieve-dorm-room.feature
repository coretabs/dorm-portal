Feature: Retrieving dormitory data

    Scenario: As a user 
              I want to get all the dormitory data
              So that I can know what they offer

        Given we have 2 dormitories with 2 rooms each
        Given we have 3 users with reviewable reservations
        Given we have 3 reviews of 4.5, 5.0, 2.2, 1.0

        When asking for last 3 reviews
        Then get last 3 reviews without the first 4.5

        When asking for reviews statistics
        Then get 4 reviews and 3.175 avg rating

        When serializing alfam to get its all data
        Then get valid serialized alfam data with 2 rooms

        When hitting GET /dorms/{alfam-id} endpoint
        Then get 200 OK with alfam data
Feature: Reviews

    Scenario: As a manager
              I want to ask students for reviews
              So that I know my dorm deficits

        Given two managers (one for alfam&dovec and one for homedorm)
        Given we have dorms(alfam & dovec & homedorm) + 2 rooms in alfam
        Given two students reserved first room and one reserved second one

        """
        Given is same as Managing-Reservations scenario
        """
        
        When both reservations arent confirmed
        Then is_reviewable is false for non-confirmed reservations

        When reservation is confirmed and after three months
        Then is_reviewable is true for confirmed past 3 months reservation
        
        When reservation is confirmed and before three months
        Then is_reviewable is false for confirmed less 3 months reservation

        When reservation is already reviewed
        Then is_reviewable is false for already reviewed reservation
        And return the first reservation is_reviewed into false

        


        When asking for review and saving
        Then validate data and send email for review asking

        When hitting POST /manager/dorms/{alfam-id}/reservations/{res-id}/ask-review
        Then get 200 OK for sending review email

        When hitting POST /manager/dorms/{alfam-id}/reservations/{res-id}/ask-review for non-reviewable
        Then get 400 Bad Request for reviewing non-reviewable

    Scenario: As a student
              I want to review a dorm
              So that I let others know about my experience

        Given two managers (one for alfam&dovec and one for homedorm)
        Given we have dorms(alfam & dovec & homedorm) + 2 rooms in alfam
        Given two students reserved first room and one reserved second one

        When creating a review for a reservation
        Then reservation is_reviewed should be True

        When creating a review for is_reviewable=False reservation
        Then creating review throws NonReviewableReservation




        When serializing dorm reviews
        Then get valid serialized dorm reviews

        When hitting GET /dorm/{alfam-id}/reviews
        Then get 200 OK with alfam reviews



        
        When deserializing dorm review sent by user
        Then get validated deserialized review
        And save that review successfully

        When hitting POST /reservations/{res-id}/add-review
        Then get 201 Created for creating the review

        When hitting POST /reservations/{res-id}/add-review for non-reviewable dorm
        Then get 400 Bad Request for not creating the review

        When hitting POST /reservations/{res-id}/add-review for non-owned reservation
        Then get 403 forbidden for not creating the review

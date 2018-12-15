Feature: Quota
    Scenario: As a student
              I want to make reservations
              So that I get a room to stay in

        Given we have 2 dormitories (and 1 room each available to reserve)

        When create a reservation
        Then quota of the room should decrease
        And deadline date should be equal to today+room_confirmation_days
        Then cleanup that reservation




        When creating reservation for room 1
        Then create a reservation for that student for room 1

        When creating reservation for room 2 for same user
        Then create a reservation for that student for room 2
        And first pending reservation should be deleted
        And quota of that room increase


        When a reservation is non-pending and creating another reservation
        Then not being able to create that reservation
        """
        we do this to ensure a receipt wont be gone
        if a student has a problem, he can contact support
        and they can reject his application then he can create another application
        """

        When retrieving an expired reservation
        Then decrease the quota for that expired reservation


        When hitting POST /reservations for room 1
        Then get 200 OK for creating that reservation

        When hitting POST /reservations with logging in
        Then get 401 Unauthorized to ensure reservation after login

        When hitting POST /reservations and no quota left
        Then get 400 Bad request to ensure using available quota




        When serializing reservation data
        Then get valid serialized data
        And confirmation_deadline_date form is 2018-12-15

        When hitting GET /reservations/{res-id}
        Then get 200 OK and reservation details

        When hitting GET /reservations/{res-id} for expired reservation
        Then get 200 OK and the expired reservation




        When hitting POST /reservations/{res-id}/receipt to add new receipt
        Then get 201 created for adding a receipt

        When hitting POST /reservations/{res-id}/receipt for rejected/confirmed/expired
        Then get 400 bad request for not updatable reservation

        When hitting POST /reservations/{res-id}/receipt non-owned reservation 
        Then get forbidden 403 for non-owned reservation
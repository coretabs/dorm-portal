Feature: Quota
    Scenario: As a student
              I want to make reservations
              So that I get a room to stay in

        Given we have 2 dormitories (and 1 room each) with some quota

        When create a reservation
        Then quota of the room should decrease
        And deadline date should be equal to today+room_confirmation_days
        Then cleanup that reservation




        When hitting POST /reservations with logging in
        Then get 401 Unauthorized to ensure reservation after login

        When hitting POST /reservations and no quota left
        Then get 400 Bad request to ensure using available quota

        When hitting POST /reservations for room 1
        Then create a reservation for that student for room 1

        When hitting POST /reservations for room 2
        Then create a reservation for that student for room 2
        And quota of that room increase
        And first reservation should be deleted

        When second reservation becomes non-pending
        And hitting POST /reservations for room 1 again
        Then not being able to create that reservation
        """we do this to ensure a reciept wont be gone
        if a student has a problem, he can contact support
        and they can reject his application then he can create another application"""




        When serializing reservation data
        Then get valid serialized data

        When hitting GET /reservations/{res-id}
        Then get 200 OK and reservation details

        When hitting GET /reservations/{res-id} for expired reservation
        Then get 200 OK and the expired reservation
        And decrease the quota for that expired reservation




        When hitting POST /reservations/{res-id}/reciept to add new reciept
        Then get 201 created for adding a reciept

        When hitting POST /reservations/{res-id}/reciept for rejected/confirmed/expired
        Then get 400 bad request for not updatable reservation

        When hitting POST /reservations/{res-id}/reciept non-owned reservation 
        Then get forbidden 403 for non-owned reservation
Feature: Reservation

    Scenario: As a student
              I want to make reservations
              So that I get a room to stay in

        Given we have 2 dormitories (and 1 room each available to reserve)
        Given two students who reserved nothing


        When create a reservation
        Then quota of the room should decrease
        And deadline date should be equal to today+room_confirmation_days

        When create a reservation for the same room
        Then quota of the room should be the same

        When creating reservation for room 2 for same user
        Then create a reservation for that student for room 2
        And first pending reservation should be deleted
        And quota of that room increase

        
        When a reservation is non-pending and creating another reservation
        Then throw an exception for creating that reservation
        But if the reservation is confirmed, rejected, or expired
        Then its okay to create another reservation
        """
        we do this to ensure a receipt wont be gone
        if a student has a problem, he can contact support
        and they can reject his application then he can create another application
        """

		When retrieving an expired reservation
        Then change its status into expired and increase room quota

        Given cleanup all reservations

        
        When hitting POST /reservations for room 1
        Then get 201 Created for creating that reservation
        And cleanup the created reservation

        When hitting POST /reservations with logging in
        Then get 403 Forbidden to ensure reservation after login

        When hitting POST /reservations and no quota left
        Then get 400 Bad request to ensure using available quota

        When hitting POST /reservations and he has a non-finished reservation
        Then get 400 Bad request to ensure finishing his reservation first



        When serializing reservation data
        Then get valid serialized data
        And confirmation_deadline_date form is 2018-12-15

        When hitting GET /reservations/{res-id}
        Then get 200 OK and reservation details

        When hitting GET /reservations/{res-id} for expired reservation
        Then get 200 OK and the expired reservation

        When hitting GET /reservations/{res-id} for non-owned reservation
        Then get 403 Forbidden for non-owned reservation



        When adding a receipt to a reservation
        Then it should update the status into WAITING_FOR_MANAGER_ACTION_STATUS
        But adding a receipt to a rejected/confirmed/expired reservation
        Then it should throw NonUpdatableReservationException

        When hitting POST /reservations/{res-id}/receipt to add new receipt
        Then get 201 created for adding a receipt

        When hitting POST /reservations/{res-id}/receipt for rejected/confirmed/expired
        Then get 400 bad request for not updatable reservation

        When hitting POST /reservations/{res-id}/receipt non-owned reservation
        Then get forbidden 403 for non-owned reservation
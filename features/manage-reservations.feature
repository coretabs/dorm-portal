Feature: Managing dormitory and room data

    Scenario: As a manager
              I want to manage my dorms reservations
              So that I respond to students requests

        Given two managers (one for alfam&dovec and one for homedorm)
        Given we have dorms(alfam & dovec & homedorm) + 2 rooms in alfam
        Given two students reserved first room and one reserved second one

        When changing reservation status into rejected
        Then quota of that room should increase

        When manager asks for reservations in specific dorm
        Then he gets all those reservations

        When serializing those reservations
        Then get valid serialized reservations
        And confirmation_deadline_date

        When hitting GET /manager/dorms/{id}/reservations
        Then get 200 OK with all the reservations

        When hitting PUT /manager/dorms/{id}/reservations/{id} into confirmed
        Then get 200 OK for updating that reservation into confirmed

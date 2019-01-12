Feature: Managing reservations

    Scenario: As a manager
              I want to manage my dorms reservations
              So that I respond to students requests

        Given two managers (one for alfam&dovec and one for homedorm)
        Given we have dorms(alfam & dovec & homedorm) + 2 rooms in alfam
        Given two students reserved first room and one reserved second one
        Given two user have expired reservations for room2

        """
        available quota is generally 5 in factory.py
        """

        When updating expired reservations
        Then res3 & res4 will get expired
        And res1 & res2 are not expired


        

        When changing reservation status into rejected
        Then quota of that room should increase by 1

        When asking for reservations status statistics by dorm_id
        Then get the correct reservations status statistics


        When serializing all dorm reservations
        Then get valid serialized reservations

        When hitting GET /manager-dorms/{alfam-id}/reservations
        Then get 200 OK with all the reservations

        When hitting GET /manager-dorms/{homedorm-id}/reservations non-owned dorm
        Then get 403 forbidden for homedorm reservations
        And the other manager can get his homedorm reservations



        When deserializing reservation new data
        Then get valid deserialized reservation data

        When hitting PUT /manager-dorms/{alfam-id}/reservations/{res1-id} into manager_updated
        Then get 200 OK for updating that reservation into manager_updated

        When hitting PUT /manager-dorms/{alfam-id}/reservations/{res1-id} into rejected
        Then get 200 OK for updating that reservation into rejected
        And collect quota from that rejected reservation

        When hitting PUT non-owned reservation into manager_updated
        Then get 403 forbidden for updating non-owned reservation


    Scenario: As a manager
              I want to let the quota be collected automatically  
              So that I can sleep at night well :D

        Given two managers (one for alfam&dovec and one for homedorm)
        Given we have dorms(alfam & dovec & homedorm) + 2 rooms in alfam
        Given two students reserved first room and one reserved second one
        Given two user have expired reservations for room2

        """
        already defined above
        """

        """
        available quota is generally 5 in factory.py
        """

        When calling the collecting the quota command
        Then room1_allowed_quota=4 and room2_allowed_quota=4
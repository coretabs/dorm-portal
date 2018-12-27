Feature: Managing room data

    Scenario: As a manager 
              I want to manage my rooms
              So that I can offer them for students

        Given two managers (one for alfam&dovec and one for homedorm)
        Given we have dorms(alfam & dovec & homedorm) + 2 rooms in alfam

        """
        Implemented already in manager-dorm.py
        """


        When getting manager filters to add to a room from serializer
        Then get valid serialized room filters

        When hitting GET /manager-dorms/filters
        Then get 200 OK with filters




        When deserializing the third room data
        Then validate the deserialized data of the third room
        And save the third room to alfam

        When hitting POST /manager/dorms/{alfam-id}/rooms
        Then get 201 created for adding a third room in alfam

        When hitting POST /manager/dorms/{alfam-id}/rooms for non-owned dorm
        Then get 403 forbidden for adding a third room in non-owned


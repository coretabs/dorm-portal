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
        Then delete that third room in alfam

        When hitting POST /manager/dorms/{alfam-id}/rooms
        Then get 201 created for adding a third room in alfam

        When hitting POST /manager/dorms/{alfam-id}/rooms for non-owned dorm
        Then get 403 forbidden for adding a third room in non-owned dorm




        Given total_quota=10, allowed_quota=5 for both rooms
        Given first room in alfam has 2 reserved from its quota
        Given second room in alfam has 1 reserved from its quota

        When asking for statistics for rooms in alfam
        Then room1 (total_quota=10, allowed_quota=3, reserved_rooms_number=2)
        And room2 (total_quota=10, allowed_quota=4, reserved_rooms_number=1)

        When serializing all rooms with statistics for alfam dorm
        Then get serialized rooms with statistics for alfam dorm

        When hitting GET /manager/dorms/{alfam-id}/rooms
        Then get 200 OK with rooms statistics for alfam

        When hitting GET /manager/dorms/{alfam-id}/rooms for non-owned dorm
        Then get 403 forbidden for getting rooms statistics in non-owned dorm
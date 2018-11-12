Feature: Activity Facility filter

    Scenario: The user wants to filter dorms whether they have
              swimming pool or free Wifi
        Given we have 2 dormitory with different facilities
        When filtering dorms by swimming pool
        Then get only the dorm which has swimming pool

        Given we have 2 dormitoroes with room-specific facilities
        When filtering dorms by having one room with luxury shower & air conditioner
        Then get only the dorm which has luxury shower with just one room
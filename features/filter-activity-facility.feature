Feature: Feature filter

    Scenario: The user wants to filter dorms whether they have
              swimming pool or free Wifi

        Given we have 2 dormitory with different features
        When filtering dorms by swimming pool
        Then get only the dorm which has swimming pool

    Scenario: The user wants to filter dorms whether they have
              luxury shower & air conditioner

        Given we have 2 dormitoroes with room-specific features
        When filtering dorms by having one room with luxury shower
        Then get only alfam with just one room which has luxury shower

        When filtering dorms by luxury shower & air conditioner
        Then get only alfam with just one rooms having luxury shower & air conditioner

        When filtering dorms by air conditioner
        Then get only alfam with two rooms having air conditioner
Feature: Integral feature

    Scenario: The user wants to filter numbers based on
              a min and a max value

        Given we have 4 rooms different prices (alfam: 3 rooms, dovec: 1 room)

        When filtering alfam prices between 500, 1500
        Then get alfam dormitory with just 2 rooms

        When filtering dovec with wrong price range
        Then not getting any dorm in dovec for wrong price
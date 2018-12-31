Feature: Getting all filters

    Scenario: The user wants to get all available filters
              for all the dorms we have

        Given we have 2 dormitory with 3 prices and 3 meal options

        When adding main filters (duration)
        Then will get main filters (duration and category)

        When getting additional_filters: prices and meals
        Then get additional_filters: with price min_max and meals

        When having more than one integral filter (bathrooms)
        Then will get bathrooms with the max bathrooms number correctly

        And not get main filters with the additional filters

        When adding features filters for dorms and rooms
        Then get both features filters for dorms and room

        When requesting GET /filters
        Then get 200 OK and all filters in GET /filters
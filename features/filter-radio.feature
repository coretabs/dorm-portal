Feature: Radio filter

    Scenario: The user wants to filter dorms by type of meal
              There are three meal types (breakfast, dinner, both)
        Given we have 1 dormitory with 2 rooms
        When filtering alfam rooms by meal Breakfast
        Then get alfam dormitory with just one room having Breakfast

        When filtering alfam rooms by meal Dinner
        Then get alfam dormitory with just two room having Dinner

        When filtering alfam rooms by meal Breakfast & Dinner
        Then get dormitory with all room having Breakfast & Dinner
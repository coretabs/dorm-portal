Feature: Quota
    Scenario: As a student
              I want to get only dorms with available quota
              So that I wont get stuck at the end of my reservation

        Given we have 2 dormitories (and 1 room each) with some quota
        When getting available dorms
        Then get alfam dormitory and not getting dovec
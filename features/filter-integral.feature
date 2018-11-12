Feature: Integral feature

    Scenario:
        Given we have 2 dormitories
        When filtering alfam right price
        Then get alfam dormitory

        When filtering dovec wrong price
        Then not getting any dorm
Feature: Currency converter
    Scenario: As a student
              I want to see the room in the price that I want
              So that I will know how much I will pay

        Given we have 2 dormitory with 4 rooms with couple of choices
        # already defined in dorm_filtering.py

        Given we have all exchange rates
        Given two rooms price currencies are in USD and one in TRY and one in EUR
        Given the rate to TRY is 5 and rate for EUR is 0.5

        """
        Room prices are:
        1000 USD
        1200 USD
        1700 TRY
        2000 EUR
        """

        When get dorms with USD currency
        Then get all rooms in USD

        When get dorms with TRY currency
        Then get all rooms in TRY

        When get dorms with EUR currency
        Then get all rooms in EUR




        When hitting POST /dorms endpoint in USD
        Then get 200 OK with USD prices

        When hitting POST /dorms endpoint in TRY
        Then get 200 OK with TRY prices

        When hitting POST /dorms endpoint in EUR
        Then get 200 OK with EUR prices

        When hitting POST /dorms endpoint in non registered currency
        Then get 200 OK with default price currency (USD)

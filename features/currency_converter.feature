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




        When filtering rooms price with USD currency between 300 and 1500
        Then get three filtered rooms in USD (340 & 1000 & 1200)

        When filtering rooms price with TRY currency between 1500 and 5100
        Then get two filtered rooms in TRY (1700 & 5000)

        When filtering rooms price with EUR currency between 500 and 2000
        Then get three filtered rooms in EUR (500 & 600 & 2000)


        

        When serializing min_value max_value for price in USD
        Then get min_value=340 and max_value=4000 for USD

        When serializing min_value max_value for price in TRY
        Then get min_value=1700 and max_value=20000 for TRY

        When serializing min_value max_value for price in EUR
        Then get min_value=170 and max_value=2000 for EUR




        When hitting POST /dorms endpoint in USD
        Then get 200 OK with USD prices

        When hitting POST /dorms endpoint in TRY
        Then get 200 OK with TRY prices

        When hitting POST /dorms endpoint in EUR
        Then get 200 OK with EUR prices

        When hitting POST /dorms endpoint in non registered currency
        Then get 200 OK with default price currency (USD)

Feature: Multiple locale (language & currency) 

    Scenario: As a user 
              I want to get filters in his own language
              So that I can understand what to filter

        Given we have 3 langs En,Ar,Tr and 2 currencies USD,TL

        When serializing 3 langs En,Ar,Tr and 2 currencies USD,TL
        Then get valid serialized languages and currencies

        When hitting GET /locale endpoint
        Then get 200 OK with langs and currencies

        Given we have 1 dorm with 2 rooms with meals and luxury shower
        
        When hitting GET /filters endpoint in English
        Then get 200 OK with English filters

        When hitting GET /filters endpoint in Turkish
        Then get 200 OK with Turkish filters

        When hitting POST /dorms endpoint in English
        Then get 200 OK with English rooms characteristics

        When hitting POST /dorms endpoint in Turkish
        Then get 200 OK with Turkish rooms characteristics

        When hitting POST /dorms endpoint in non registered language
        Then get 200 OK with Default language (EN) rooms characteristics
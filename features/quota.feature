Feature: Quota
    Scenario: we have 2 dormitories (alfam & dovec) 
              with 1 room for each and only alfam has quota more than zero
        Given we have 2 dormitories with some quota
        When getting available dorms
        Then get alfam dormitory and not getting dovec
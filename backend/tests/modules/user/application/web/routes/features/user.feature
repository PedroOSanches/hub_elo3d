Feature: Partner registration
    As a new partner
    I want to register on the platform
    So that I can join the Elo3D Hub network.

    Scenario: Partner registration
        Given that I have provided valid information
        When I submit my registration
        Then my user account should be created

    Scenario: Partner registration fails due to missing parameters
        Given that I have provided informations with missing parameters
        When I submit my registration
        Then my user accound should not be created
        And I should receive an error message missing parameter
    
    Scenario: Partner registration fails due to wrong type parameters
        Given that I have provided informations with wrong type parameters
        When I submit my registration
        Then my user accound should not be created
        And I should receive an error message wrong parameter
Feature: Login

    As a user,
    I want to log in to the platform,
    So that I can access the features corresponding to my profile.

    Scenario: Login successful
        Given that I have provided valid credentials
        When I submit my login credentials
        Then I should successfully log in and access the EloHub 3D platform
        And authentication tokens are set in my cookies
    
    Scenario: Unauthorized Login
        Given that I have provided invalid credentials
        When I submit my login credentials
        Then my login is not accept
        And authentication tokens aren't set in my cookies
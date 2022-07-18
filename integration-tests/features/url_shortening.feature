Feature: Manage clinicians installations
  As a developer
  I want to have efficient way to manage url shortening
  So that I can simplify users' workflows

  Background: 
    Given I have a URL
  
  Scenario: URL is shortened
    When I send the URL to the shortener
    Then I get a short code from the shortener
  
  Scenario Outline: Long URL can be retrieved up to "maximum uses" times
    Given I send the URL with <maximum_uses> maximum uses to the shortener
    And I get a short code from the shortener
    When I retrieve the long URL <use_count> times
    Then I get <result>
    Examples:
      | maximum_uses | use_count | result           |
      | 5            | 4         | the original url |
      | 7            | 7         | the original url |
      | 8            | 9         | an error         |
 
  Scenario: Once expired, identical URL can no longer be shortened
    Given I send the URL with 1 maximum use to the shortener
    And I get a short code from the shortener
    And I retrieve the long URL 1 time
    And I send the URL with 5 maximum uses to the shortener
    When I retrieve the long URL 1 time
    Then I get an error

  Scenario: Static activation codes
    Given a short code for a static activation
    When I retrieve the long URL 1 time
    Then I get the original url

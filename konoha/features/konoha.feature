Feature: Display pages
    Konoha is a CMS system that uses yaml data
    to store user-defined content.

    Scenario: Display pages
        Given Page 'index2' with url '/' and template 'test/index.html'
        When We request url '/' from server
        Then Returned page contains 'This is index page'


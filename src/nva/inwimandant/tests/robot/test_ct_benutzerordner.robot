# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s nva.inwimandant -t test_benutzerordner.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src nva.inwimandant.testing.NVA_INWIMANDANT_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/nva/inwimandant/tests/robot/test_benutzerordner.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a Benutzerordner
  Given a logged-in site administrator
    and an add Benutzerordner form
   When I type 'My Benutzerordner' into the title field
    and I submit the form
   Then a Benutzerordner with the title 'My Benutzerordner' has been created

Scenario: As a site administrator I can view a Benutzerordner
  Given a logged-in site administrator
    and a Benutzerordner 'My Benutzerordner'
   When I go to the Benutzerordner view
   Then I can see the Benutzerordner title 'My Benutzerordner'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Benutzerordner form
  Go To  ${PLONE_URL}/++add++Benutzerordner

a Benutzerordner 'My Benutzerordner'
  Create content  type=Benutzerordner  id=my-benutzerordner  title=My Benutzerordner

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Benutzerordner view
  Go To  ${PLONE_URL}/my-benutzerordner
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Benutzerordner with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Benutzerordner title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}

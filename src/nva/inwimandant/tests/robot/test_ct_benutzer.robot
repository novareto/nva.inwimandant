# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s nva.inwimandant -t test_benutzer.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src nva.inwimandant.testing.NVA_INWIMANDANT_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/nva/inwimandant/tests/robot/test_benutzer.robot
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

Scenario: As a site administrator I can add a Benutzer
  Given a logged-in site administrator
    and an add Benutzerordner form
   When I type 'My Benutzer' into the title field
    and I submit the form
   Then a Benutzer with the title 'My Benutzer' has been created

Scenario: As a site administrator I can view a Benutzer
  Given a logged-in site administrator
    and a Benutzer 'My Benutzer'
   When I go to the Benutzer view
   Then I can see the Benutzer title 'My Benutzer'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Benutzerordner form
  Go To  ${PLONE_URL}/++add++Benutzerordner

a Benutzer 'My Benutzer'
  Create content  type=Benutzerordner  id=my-benutzer  title=My Benutzer

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Benutzer view
  Go To  ${PLONE_URL}/my-benutzer
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Benutzer with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Benutzer title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}

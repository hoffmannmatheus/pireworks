#App Activity (Home Activity)

##Overview

This is the initial Activity that a user gets to experience once the App is first launched.

Kindly view actual code to get more detailed information : 
[a link](https://github.com/hoffmannmatheus/pireworks/blob/master/src/app/pireworks/app/src/main/java/com/pireworks/app/pireworks/HomeActivity.java)

1. `onCreate` handles the creation of the Activity (initiation of an activity lifecyle) acquirng  all the pre-set screen layout information from an XML file and instantiating the various resources that is used to create the activity.

2. The various `onClick(OnClickListener)` hanldes the different button intents as the buttons are clicked by the user.

3. `IntentFilter` handles the different states that can be invoked from the device adapter through the the current activity.

4. `onPause` handles the action of cancelling the discovery of bluetooth devices when the Activity is paused.

5. `onDestroy` handles the closing of the Activity.

6. `showEnabled`  handles the change of display from the bluetooth being disabled to enabled.

7. `showDisabled`  handles the change of display from the bluetooth being enabled to disabled.

8. `showUnsupported` handles the display of when of when a bluetooth adpater is not supported or inactive on a device.

9. `showToast` handles the tiny widget display messages that are seen by the user when the state of the bluetooth adapter is changed from "Enabled" and the displaying of "Found Device".

10. `onReceive` handles the authorized communcation between the app Activity and the Bluetooth Adapter found on the device. It processes requests for a state change to the adapter and recieves state change responses or actions that are requested for.

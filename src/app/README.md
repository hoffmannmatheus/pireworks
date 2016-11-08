#App Activity (Home Activity)

##Overview

This is the initial Activity that a user experiences once the App is first launched.

Kindly view actual code to get more detailed information : 
[Home Activity Code](https://github.com/hoffmannmatheus/pireworks/blob/master/src/app/pireworks/app/src/main/java/com/pireworks/app/pireworks/HomeActivity.java)

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

#Bluetooth Activity (Device List Activity)

##Overview

This is the Activity that displays the list of discovered Bluetooth devices which can be paired / unpaired.

Kindly view actual code to get more detailed information : [DeviceListActivity code] (https://github.com/hoffmannmatheus/pireworks/blob/master/src/app/pireworks/app/src/main/java/com/pireworks/app/pireworks/DeviceListActivity.java)

1. `onCreate` -  launches activity by fetching all the required UI components from the [activity_paired_devices.xml] (https://github.com/hoffmannmatheus/pireworks/blob/master/src/app/pireworks/app/src/main/res/layout/activity_paired_devices.xml) file and instantiating the Device List Adapter to discover Bluetooth devices ; Bluetooth device discovery is a runtime activity and hence we use intents to facilitate late binding; Sets the adapter to default BluetoothAdapter and register the Bluetooth Broadcast receiver.

2. `mPairReceiver` - broadcast receiver; whenever an Intent Broadcast is received, the onReceive method is executed.

3. `onReceive` - whenever the state of the Bluetooth device is changed i.e. when the ACTION_BOND_STATE changes from paired to unpaired or vice versa), the method checks for the state of the device in real-time and displays a static text view accordingly.

4. `onDestroy` - unregister the broadcast receiver and close activity

5. `showToast` -  shows a static text view of the BluetoothContext for a short duration of time 

6. `pairDevice` - uses the createBond method from the BluetoothDevice class to pair a selected Bluetooth device with the current one

7. `unpairDevice` - uses the removeBond method from the BluetoothDevice class to pair a selected Bluetooth device with the current one

8. `onDeviceClick`- creates an intent for the PirewroksActivity and adds the device to the pireworks device list

9. `onPairButtonClick` - pairs the selected device if not already paired or unpairs the selected device if already in paired state.

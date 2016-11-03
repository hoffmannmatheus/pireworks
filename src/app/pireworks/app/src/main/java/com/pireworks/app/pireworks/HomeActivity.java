package com.pireworks.app.pireworks;

import android.app.ProgressDialog;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.IntentFilter;
import android.graphics.Color;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import java.util.ArrayList;
import java.util.Set;

/** The HomeActivity extends the AppCompatActivity that serves as the base class for activities that use support action bar featured**/
public class HomeActivity extends AppCompatActivity {

    private TextView mStatusTv;
    private Button mActivateBtn;
    private Button mPairedBtn;
    private Button mScanBtn;

    private ProgressDialog mProgressDlg;

    private ArrayList<BluetoothDevice> mDeviceList = new ArrayList<BluetoothDevice>();

    private BluetoothAdapter mBluetoothAdapter;

    @Override
    
     
    /** onCreate function instantiates the Activity by taking all it's Pre-Set layout values from a HomeActivity XML file."""
    """ The Bundle savedInstanceState is used here to save all the data the activity uses to help restore an activity once a destroyed activity is created again""" 
    """ It has a bluetooh adapter method to instantiate default adapter found on the device.(mBluetoothAdapter)"""
    """ Also has the (mProgressDlg) method to handle the display of the progress when ever devices are being scanned **/  
        
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.activity_home);

        mStatusTv = (TextView) findViewById(R.id.tv_status);
        mActivateBtn= (Button) findViewById(R.id.btn_enable);
        mPairedBtn = (Button) findViewById(R.id.btn_view_paired);
        mScanBtn = (Button) findViewById(R.id.btn_scan);

        mBluetoothAdapter = BluetoothAdapter.getDefaultAdapter();

        mProgressDlg = new ProgressDialog(this);

        mProgressDlg.setMessage("Scanning...");
        mProgressDlg.setCancelable(false);
        mProgressDlg.setButton(DialogInterface.BUTTON_NEGATIVE, "Cancel", new DialogInterface.OnClickListener() {
           
            @Override
            /** onClick method handles the various button actions that are carried out by a user """
            """ mActivateBtn (onClicklistener) carries out the action of enabling and disabling on the app through the bluetooth adapter on the device and if there isn't an existing"""
            """ adapter, shows (Unsupported Message)."""   
            """ mScanBtn (onClicklistener) carries out the action using the bluetooth adapter to discover devices"""
            """ mPairedBtn (onClicklistener) carries the action of pairing with bluetooth devices found in the Bluetooth Device Array List"""    
            """ Intent filter handles the requests that are sent to the devices bluetooh adapter to handle different states of the adapter"""
            """ The Receiver handles the different state change requests and responses that is gotten from the bluetooth adapter **/    
            public void onClick(DialogInterface dialog, int which) {
                dialog.dismiss();

                mBluetoothAdapter.cancelDiscovery();
            }
        });

        if (mBluetoothAdapter == null) {
            showUnsupported();
        } else {
            mPairedBtn.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    Set<BluetoothDevice> pairedDevices = mBluetoothAdapter.getBondedDevices();

                    if (pairedDevices == null || pairedDevices.size() == 0) {
                        showToast("No Paired Devices Found");
                    } else {
                        ArrayList<BluetoothDevice> list = new ArrayList<BluetoothDevice>();

                        list.addAll(pairedDevices);

                        Intent intent = new Intent(HomeActivity.this, DeviceListActivity.class);
                        intent.putParcelableArrayListExtra(DeviceListActivity.EXTRA_DEVICE_LIST, list);
                        startActivity(intent);
                    }
                }
            });

            mScanBtn.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View arg0) {
                    mBluetoothAdapter.startDiscovery();
                }
            });

            mActivateBtn.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    if (mBluetoothAdapter.isEnabled()) {
                        mBluetoothAdapter.disable();

                        showDisabled();
                    } else {
                        Intent intent = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
                        startActivityForResult(intent, 1000);
                    }
                }
            });

            if (mBluetoothAdapter.isEnabled()) {
                showEnabled();
            } else {
                showDisabled();
            }
        }

        IntentFilter filter = new IntentFilter();

        filter.addAction(BluetoothAdapter.ACTION_STATE_CHANGED);
        filter.addAction(BluetoothDevice.ACTION_FOUND);
        filter.addAction(BluetoothAdapter.ACTION_DISCOVERY_STARTED);
        filter.addAction(BluetoothAdapter.ACTION_DISCOVERY_FINISHED);

        registerReceiver(mReceiver, filter);
    }

    @Override
    /** onPause method carries out the action of pausing the bluetooth adapter when it's in discovery state"""
    """ The actual method is called up from the class AppCompatActivity **/   
        
    public void onPause() {
        if (mBluetoothAdapter != null) {
            if (mBluetoothAdapter.isDiscovering()) {
                mBluetoothAdapter.cancelDiscovery();
            }
        }

        super.onPause();
    }

    @Override
    /** The onDestroy method is called from the AppCompatActivity class and handles the closing of the Activity and also the unregistering of the receiver"""
    """ that handles the action state change of the bluetooth adapter **/ 
        
    public void onDestroy() {
        unregisterReceiver(mReceiver);

        super.onDestroy();
    }
    
 /** These two methods (showEnabled and showDisabled) carry the action of displaying the different states that can be invoked when user clicks on"""
 """ mActivateBtn."""   
 """ The method showUnsupported carries out the action of displaying to a message of (Bluetooth Unsupported), if adapter is unavailable or inactive**/    
   
     private void showEnabled() {
        mStatusTv.setText("Bluetooth is On");
        mStatusTv.setTextColor(Color.BLUE);

        mActivateBtn.setText("Disable");
        mActivateBtn.setEnabled(true);

        mPairedBtn.setEnabled(true);
        mScanBtn.setEnabled(true);
    }

    private void showDisabled() {
        mStatusTv.setText("Bluetooth is Off");
        mStatusTv.setTextColor(Color.RED);

        mActivateBtn.setText("Enable");
        mActivateBtn.setEnabled(true);

        mPairedBtn.setEnabled(false);
        mScanBtn.setEnabled(false);
    }

    private void showUnsupported() {
        mStatusTv.setText("Bluetooth is unsupported by this device");

        mActivateBtn.setText("Enable");
        mActivateBtn.setEnabled(false);

        mPairedBtn.setEnabled(false);
        mScanBtn.setEnabled(false);
    }

    /** This method carries out the action of displaying a little display widget **/
    private void showToast(String message) {
        Toast.makeText(getApplicationContext(), message, Toast.LENGTH_SHORT).show();
    }
    
/** This method handles the reciever with in this activity that communicates with the device bluetooth adapter to invoke the different state(intent)changes"""
"""  BluetoothAdapter.ACTION_STATE_CHANGED this handles the initial request of making a state change"""
"""  BluetoothAdapter.STATE_ON this state when requested is to turn on the bluetooth adapter on the device and send back a reposnse to the reciever for the"""
""" action to take effect within the app Activity""" 
""" BluetoothAdapter.ACTION_DISCOVERY_STARTED this action is for the discovery (scanning) of bluetooth devices around. The found devices are added to an Array List"""
""" BluetoothAdapter.ACTION_DISCOVERY_FINISHED this action handles the closing of the discovery state."""
""" BluetoothDevice.ACTION_FOUND this action handles the state of the discovered devices and parsing them on to the Bluetooth device ArrayList **/
    
    private final BroadcastReceiver mReceiver = new BroadcastReceiver() {
        public void onReceive(Context context, Intent intent) {
            String action = intent.getAction();

            if (BluetoothAdapter.ACTION_STATE_CHANGED.equals(action)) {
                final int state = intent.getIntExtra(BluetoothAdapter.EXTRA_STATE, BluetoothAdapter.ERROR);

                if (state == BluetoothAdapter.STATE_ON) {
                    showToast("Enabled");

                    showEnabled();
                }
            } else if (BluetoothAdapter.ACTION_DISCOVERY_STARTED.equals(action)) {
                mDeviceList = new ArrayList<BluetoothDevice>();

                mProgressDlg.show();
            } else if (BluetoothAdapter.ACTION_DISCOVERY_FINISHED.equals(action)) {
                mProgressDlg.dismiss();

                Intent newIntent = new Intent(HomeActivity.this, DeviceListActivity.class);
                newIntent.putParcelableArrayListExtra(DeviceListActivity.EXTRA_DEVICE_LIST, mDeviceList);
                startActivity(newIntent);
            } else if (BluetoothDevice.ACTION_FOUND.equals(action)) {
                BluetoothDevice device = (BluetoothDevice) intent.getParcelableExtra(BluetoothDevice.EXTRA_DEVICE);

                mDeviceList.add(device);

                showToast("Found device " + device.getName());
            }
        }
    };

}

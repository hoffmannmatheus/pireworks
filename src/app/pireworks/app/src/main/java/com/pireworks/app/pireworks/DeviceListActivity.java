package com.pireworks.app.pireworks;

import android.app.Activity;
import android.bluetooth.BluetoothDevice;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.os.Bundle;
import android.widget.ListView;
import android.widget.Toast;

import com.pireworks.app.pireworks.adapter.DeviceListAdapter;

import java.lang.reflect.Method;
import java.util.ArrayList;

public class DeviceListActivity extends Activity implements DeviceListAdapter.OnDeviceListListener {

    public static final String EXTRA_DEVICE_LIST = "bluetooth_device_list";

    private ListView mListView;
    private DeviceListAdapter mAdapter; 
    private ArrayList<BluetoothDevice> mDeviceList;

    /**  Perform Initial activities for launching -
         1. Get UI elements from the xml and set the content for the activity
         2. Get default Bluetooth adapter 
         3. Register the broadcast receiver.
    **/
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        
        setContentView(R.layout.activity_paired_devices);

        //populate bluetooth device list
        mDeviceList	= getIntent().getExtras().getParcelableArrayList(EXTRA_DEVICE_LIST);
        
        //create list view for paired devices
        mListView = (ListView) findViewById(R.id.lv_paired);
        
        //get default blueetooth adapter and add devices to the list at runtime
        mAdapter = new DeviceListAdapter(this);
        mAdapter.setData(mDeviceList);
        mAdapter.setListener(this);

        mListView.setAdapter(mAdapter);
        
        //register the broadcast reciever so that it can be invoked when the bluetooth state is changed
        registerReceiver(mPairReceiver, new IntentFilter(BluetoothDevice.ACTION_BOND_STATE_CHANGED));
    }

    
    /** Unregister the broadcast receiver to avoid memmory leaks 
        and then
        destroy the activity
    **/
    @Override
    public void onDestroy() {
        unregisterReceiver(mPairReceiver);

        super.onDestroy();
    }

    /** Display text like scanning/discovering devices
        w.r.t the Bluetooth Application context
    **/
    private void showToast(String message) {
        Toast.makeText(getApplicationContext(), message, Toast.LENGTH_SHORT).show();
    }
    
    /** Use BluetoothDevice's createBond() 
        to pair the selected device 
    **/
    private void pairDevice(BluetoothDevice device) {
        try {
            Method method = device.getClass().getMethod("createBond", (Class[]) null);
            method.invoke(device, (Object[]) null);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
   
    /** Use BluetoothDevice's removeBond() 
        to unpair the selected device
    **/
    private void unpairDevice(BluetoothDevice device) {
        try {
            Method method = device.getClass().getMethod("removeBond", (Class[]) null);
            method.invoke(device, (Object[]) null);

        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    /** Create the BroadcastReceiver object to recieve BroadCastIntent from Bluetooth devices
        and show toast when the state of the bluetooth devices change
    **/
    private final BroadcastReceiver mPairReceiver = new BroadcastReceiver() {
        public void onReceive(Context context, Intent intent) {
            String action = intent.getAction();

            if (BluetoothDevice.ACTION_BOND_STATE_CHANGED.equals(action)) {
                final int state 		= intent.getIntExtra(BluetoothDevice.EXTRA_BOND_STATE, BluetoothDevice.ERROR);
                final int prevState	= intent.getIntExtra(BluetoothDevice.EXTRA_PREVIOUS_BOND_STATE, BluetoothDevice.ERROR);

                if (state == BluetoothDevice.BOND_BONDED && prevState == BluetoothDevice.BOND_BONDING) {
                    showToast("Paired");
                } else if (state == BluetoothDevice.BOND_NONE && prevState == BluetoothDevice.BOND_BONDED){
                    showToast("Unpaired");
                }

                mAdapter.notifyDataSetChanged();
            }
        }
    };

    /** Add the selected bluetooth device to the pireworks_device_list
        and launch Pirewroks Activity
    **/
    @Override
    public void onDeviceClick(BluetoothDevice device) {
        if (device == null) {
            return;
        }
        Intent newIntent = new Intent(this, PireworksActivity.class);
        newIntent.putExtra(PireworksActivity.EXTRA_DEVICE, device);
        startActivity(newIntent);
    }

    /** Pair the selected bluetooth device if it is not already paired
        else unpair device
    **/
    @Override
    public void onPairButtonClick(BluetoothDevice device) {

        if (device.getBondState() == BluetoothDevice.BOND_BONDED) {
            unpairDevice(device);
        } else {
            showToast("Pairing...");

            pairDevice(device);
        }
    }
}

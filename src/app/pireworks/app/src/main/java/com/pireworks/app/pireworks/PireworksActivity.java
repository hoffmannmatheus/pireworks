package com.pireworks.app.pireworks;

import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothSocket;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.UUID;

public class PireworksActivity extends AppCompatActivity implements View.OnClickListener {

    public static final String EXTRA_DEVICE = "pireworks_bluetooth_device";

    private static final UUID mUUID= UUID.fromString("12a2f831-b43e-4a7e-a850-5ff5143c29a7");

    private BluetoothDevice mDevice;

    private BluetoothSocket mBluetoothSocket;
    private InputStream mInputStream;
    private OutputStream mOutputStream;
    private MessageReader mMessageReader;

    private TextView mDeviceMessagesTextView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_pireworks);

        mDevice = getIntent().getExtras().getParcelable(EXTRA_DEVICE);
        mDeviceMessagesTextView = (TextView) findViewById(R.id.pireworks_device_messages);

        TextView deviceNameTextView = (TextView) findViewById(R.id.pireworks_device_name);
        TextView deviceAddressTextView = (TextView) findViewById(R.id.pireworks_device_address);
        Button sendButton = (Button) findViewById(R.id.pireworks_send_message_button);

        if (mDevice != null) {
            deviceNameTextView.setText(mDevice.getName());
            deviceAddressTextView.setText(mDevice.getAddress());


            try {
//                Method method = mDevice.getClass().getMethod("createInsecureRfcommSocket", (Class[]) null);
//                mBluetoothSocket = (BluetoothSocket) method.invoke(mDevice, (Object[]) null);
                mBluetoothSocket = mDevice.createRfcommSocketToServiceRecord(mDevice.getUuids()[0].getUuid());
                mBluetoothSocket.connect();
                mInputStream = mBluetoothSocket.getInputStream();
                mOutputStream = mBluetoothSocket.getOutputStream();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }

        if (mInputStream == null || mOutputStream == null) {
            Toast.makeText(this, "Could not connect to device!", Toast.LENGTH_LONG).show();
            finish();
            return;
        }

        mMessageReader = new MessageReader();
        mMessageReader.start();

        sendButton.setOnClickListener(this);
    }

    @Override
    protected void onDestroy() {
        if (mBluetoothSocket != null) {
            try {
                mBluetoothSocket.close();
                mBluetoothSocket = null;
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        if (mInputStream != null) {
            try {
                mInputStream.close();
                mInputStream = null;
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        if (mOutputStream != null) {
            try {
                mOutputStream.close();
                mOutputStream = null;
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        if (mMessageReader != null) {
            mMessageReader.interrupt();
            mMessageReader = null;
        }
        super.onDestroy();
    }

    @Override
    public void onClick(View view) {
        switch (view.getId()) {
            case R.id.pireworks_send_message_button:
                String message = "numb_" + Math.random();
                sendMessage(message);
                break;
        }
    }

    // HELPER METHODS
    private void sendMessage(String message) {
        if (mOutputStream != null && message != null) {
            try {
                mOutputStream.write(message.getBytes());
            } catch (IOException e) {
                e.printStackTrace();
            }
            appendMessage("me", message);
        }
    }

    private void appendMessage(final String from, final String message) {
        if (mDeviceMessagesTextView != null) {
            runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    mDeviceMessagesTextView.append("\n" + from + ": " + message);
                }
            });
        }
    }

    class MessageReader extends Thread {

        public void run() {
            byte[] buffer = new byte[1024];
            int bytes;

            while (mDevice.getBondState() == BluetoothDevice.BOND_BONDED && mInputStream != null) {
                try {

                    bytes = mInputStream.read(buffer);
                    appendMessage(mDevice.getName(), new String(buffer, 0, bytes));

                } catch (IOException e) {
                    e.printStackTrace();
                }

            }
        }
    }
}

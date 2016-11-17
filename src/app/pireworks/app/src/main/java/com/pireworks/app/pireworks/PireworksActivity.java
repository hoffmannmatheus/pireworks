package com.pireworks.app.pireworks;

import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothSocket;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import com.google.gson.Gson;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import com.pes.androidmaterialcolorpickerdialog.ColorPicker;
import com.pireworks.app.pireworks.Helper.BluetoothHelper;
import com.pireworks.app.pireworks.data.Configuration;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.UUID;


public class PireworksActivity extends AppCompatActivity implements View.OnClickListener {

    public static final String EXTRA_DEVICE = "pireworks_bluetooth_device";

    private static final UUID mUUID = UUID.fromString("12a2f831-b43e-4a7e-a850-5ff5143c29a7");

    private BluetoothDevice mDevice;

    private int triggerOffset;
    private int triggerThreshold;
    private int amplitudeIntensity;
    private HashMap<String,String> userColorMap;
    private Configuration config;

    private BluetoothHelper bluetoothHelper;

    private BluetoothSocket mBluetoothSocket;
    private InputStream mInputStream;
    private OutputStream mOutputStream;
    private MessageReader mMessageReader;

    ArrayList<Integer> selectButtonList;

    private int defaultColorR = 125;
    private int defaultColorG = 100;
    private int defaultColorB = 55;

    private int selectedColorRGB;



    final ColorPicker cp = new ColorPicker(PireworksActivity.this, defaultColorR, defaultColorG, defaultColorB);



    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_pireworks);

        mDevice = getIntent().getExtras().getParcelable(EXTRA_DEVICE);

        TextView deviceNameTextView = (TextView) findViewById(R.id.pireworks_device_name);
        EditText threshold = (EditText) findViewById(R.id.thresholdInput);
        EditText offset = (EditText) findViewById(R.id.offsetInput);

        Button selectA = (Button) findViewById(R.id.selectA);
        Button selectB = (Button) findViewById(R.id.selectB);
        Button selectC = (Button) findViewById(R.id.selectC);
        Button selectD = (Button) findViewById(R.id.selectD);
        Button selectE = (Button) findViewById(R.id.selectE);
        Button selectF = (Button) findViewById(R.id.selectF);
        Button selectG = (Button) findViewById(R.id.selectG);
        Button selectH = (Button) findViewById(R.id.selectH);

        Button save = (Button) findViewById(R.id.saveButton);

        selectButtonList = new ArrayList<Integer>();
        selectButtonList.add(R.id.selectA);
        selectButtonList.add(R.id.selectB);
        selectButtonList.add(R.id.selectC);
        selectButtonList.add(R.id.selectD);
        selectButtonList.add(R.id.selectE);
        selectButtonList.add(R.id.selectF);
        selectButtonList.add(R.id.selectG);
        selectButtonList.add(R.id.selectH);

        if (mDevice != null) {
            deviceNameTextView.setText(mDevice.getName());

            try {
//              Method method = mDevice.getClass().getMethod("createInsecureRfcommSocket", (Class[]) null);
//              mBluetoothSocket = (BluetoothSocket) method.invoke(mDevice, (Object[]) null);
                mBluetoothSocket = mDevice.createRfcommSocketToServiceRecord(mDevice.getUuids()[0].getUuid());
                mBluetoothSocket.connect();
                mOutputStream = mBluetoothSocket.getOutputStream();
                mInputStream = mBluetoothSocket.getInputStream();
            } catch (Exception e) {
                e.printStackTrace();
                Toast.makeText(this, "Cannot start socket: " + e.getMessage(), Toast.LENGTH_SHORT);
                finish();
            }
        }

        if (mInputStream == null || mOutputStream == null) {
            Toast.makeText(this, "Could not connect to device!", Toast.LENGTH_LONG).show();
            finish();
            return;
        }

        mMessageReader = new MessageReader();
        mMessageReader.start();

        selectA.setOnClickListener(this);
        selectB.setOnClickListener(this);
        selectC.setOnClickListener(this);
        selectD.setOnClickListener(this);
        selectE.setOnClickListener(this);
        selectF.setOnClickListener(this);
        selectG.setOnClickListener(this);
        selectH.setOnClickListener(this);

        threshold.setOnClickListener(this);
        offset.setOnClickListener(this);
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
        if ( selectButtonList.contains(Integer.valueOf(view.getId()))){
            cp.show(); //show colorPicker dialog
            Button okColor = (Button)cp.findViewById(R.id.okColorButton);

            okColor.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {

            /* You can get single channel (value 0-255)
                    selectedColorR = cp.getRed();
                    selectedColorG = cp.getGreen();
                    selectedColorB = cp.getBlue();
             */

            /* Or the android RGB Color (see the android Color class reference) */
                    selectedColorRGB = cp.getColor();
                    cp.dismiss();
                }
            });

            switch (view.getId()){
                case R.id.selectA: userColorMap.put("A", String.valueOf(selectedColorRGB));break;
                case R.id.selectB: userColorMap.put("B", String.valueOf(selectedColorRGB)); break;
                case R.id.selectC: userColorMap.put("C", String.valueOf(selectedColorRGB)); break;
                case R.id.selectD: userColorMap.put("D", String.valueOf(selectedColorRGB));break;
                case R.id.selectE: userColorMap.put("E", String.valueOf(selectedColorRGB)); break;
                case R.id.selectF: userColorMap.put("F", String.valueOf(selectedColorRGB)); break;
                case R.id.selectG: userColorMap.put("G", String.valueOf(selectedColorRGB)); break;
                case R.id.selectH: userColorMap.put("H", String.valueOf(selectedColorRGB)); break;
            }
        }

        if(view.getId() == R.id.thresholdInput)
            this.triggerThreshold = R.id.thresholdInput;

        if(view.getId() == R.id.offsetInput)
            this.triggerOffset = R.id.offsetInput;

        if(view.getId() == R.id.saveButton){
            if (this.userColorMap == null)
                config = new Configuration(this.triggerThreshold,this.triggerOffset,this.amplitudeIntensity);
            else
                config = new Configuration(this.triggerThreshold, this.triggerOffset, this.amplitudeIntensity,this.userColorMap);
            bluetoothHelper.sendMessage(this.mOutputStream,this.config);
        }
    }


    @Override
    public void onStart() {
        super.onStart();

    }

    @Override
    public void onStop() {
        super.onStop();
    }

    class MessageReader extends Thread {

        public void run() {
            byte[] buffer = new byte[1024];
            int bytes;

            while (mDevice.getBondState() == BluetoothDevice.BOND_BONDED && mInputStream != null) {
                try {

                    bytes = mInputStream.read(buffer);
                    String json = new String(buffer, 0, bytes);

                    JsonParser jsonParser = new JsonParser();
                    JsonObject object = (JsonObject) jsonParser.parse(json);

                    String configName = object.get("name").getAsString();
                    JsonObject colorMap = object.get("colors").getAsJsonObject();

                    bluetoothHelper.appendMessage(mDevice.getName(), (new Gson()).toJson(object));

                } catch (IOException e) {
                    e.printStackTrace();
                }

            }
        }
    }
}

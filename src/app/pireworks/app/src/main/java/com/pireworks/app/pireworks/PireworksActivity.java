package com.pireworks.app.pireworks;

import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothSocket;
import android.content.res.TypedArray;
import android.graphics.Color;
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
import com.pireworks.app.pireworks.Helper.BluetoothHelper;
import com.pireworks.app.pireworks.data.Configuration;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.UUID;

import petrov.kristiyan.colorpicker.ColorPicker;


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

    private EditText mThresholdEditText;
    private EditText mOffsetEditText;
    private EditText mIntensityEditText;

    ArrayList<Integer> selectButtonList;

    protected TypedArray ta;
    protected String chosenColor;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_pireworks);

        mDevice = getIntent().getExtras().getParcelable(EXTRA_DEVICE);
        userColorMap = Configuration.getDefaultColorMap();

        TextView deviceNameTextView = (TextView) findViewById(R.id.pireworks_device_name);
        mThresholdEditText  = (EditText) findViewById(R.id.thresholdInput);
        mOffsetEditText     = (EditText) findViewById(R.id.offsetInput);
        mIntensityEditText  = (EditText) findViewById(R.id.intensityInput);

        Button selectA = (Button) findViewById(R.id.selectA);
        Button selectB = (Button) findViewById(R.id.selectB);
        Button selectC = (Button) findViewById(R.id.selectC);
        Button selectD = (Button) findViewById(R.id.selectD);
        Button selectE = (Button) findViewById(R.id.selectE);
        Button selectF = (Button) findViewById(R.id.selectF);
        Button selectG = (Button) findViewById(R.id.selectG);
        Button selectH = (Button) findViewById(R.id.selectH);

        findViewById(R.id.saveButton).setOnClickListener(this);

        selectButtonList = new ArrayList<Integer>();
        createButtonList();

        ta = getResources().obtainTypedArray(R.array.default_colors);

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

        bluetoothHelper = new BluetoothHelper();

        selectA.setOnClickListener(this);
        selectB.setOnClickListener(this);
        selectC.setOnClickListener(this);
        selectD.setOnClickListener(this);
        selectE.setOnClickListener(this);
        selectF.setOnClickListener(this);
        selectG.setOnClickListener(this);
        selectH.setOnClickListener(this);
    }

    private void createButtonList() {
        selectButtonList.add(R.id.selectA);
        selectButtonList.add(R.id.selectB);
        selectButtonList.add(R.id.selectC);
        selectButtonList.add(R.id.selectD);
        selectButtonList.add(R.id.selectE);
        selectButtonList.add(R.id.selectF);
        selectButtonList.add(R.id.selectG);
        selectButtonList.add(R.id.selectH);
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
    public void onClick(final View view) {
        if ( selectButtonList.contains(Integer.valueOf(view.getId()))){

            ColorPicker colorPicker = new ColorPicker(this);
            colorPicker.setColors(R.array.default_colors);
            colorPicker.setColumns(5);
            colorPicker.setDismissOnButtonListenerClick(true);
            colorPicker.setOnChooseColorListener(new ColorPicker.OnChooseColorListener() {

                @Override
                public void onChooseColor(int position,int color) {
                    if (position < 0) return;
                    chosenColor = getChosenColor(ta.getString(position));
                    ((Button) findViewById(view.getId())).setBackgroundColor(color);
                    ((Button) findViewById(view.getId())).setTextColor(Color.WHITE);
                    switch (view.getId()) {
                        case R.id.selectA: userColorMap.put("A", chosenColor);break;
                        case R.id.selectB: userColorMap.put("B", chosenColor); break;
                        case R.id.selectC: userColorMap.put("C", chosenColor); break;
                        case R.id.selectD: userColorMap.put("D", chosenColor);break;
                        case R.id.selectE: userColorMap.put("E", chosenColor); break;
                        case R.id.selectF: userColorMap.put("F", chosenColor); break;
                        case R.id.selectG: userColorMap.put("G", chosenColor); break;
                        case R.id.selectH: userColorMap.put("H", chosenColor); break;
                    }
                }

                @Override
                public void onCancel(){
                }
            });
            colorPicker.show(); //show colorPicker dialog

        }

        if(view.getId() == R.id.saveButton){
            triggerThreshold = Integer.parseInt(mThresholdEditText.getText().toString());
            amplitudeIntensity = Integer.parseInt(mIntensityEditText.getText().toString());
            triggerOffset = Integer.parseInt(mOffsetEditText.getText().toString());
            config = new Configuration(this.triggerThreshold, this.triggerOffset, this.amplitudeIntensity,this.userColorMap);
            bluetoothHelper.sendMessage(this.mOutputStream, this.config);
        }
    }




   private String getChosenColor(String chosenColor) {
        switch(chosenColor.toLowerCase()){
            case "#ffff0000": return "red";
            case "#ff00ff00": return "green";
            case "#ff0000ff": return "blue";
            case "#ff008080": return "teal";
            case "#ff800080": return "purple";
            case "#ff7fffd4": return "aquamarine";
            case "#ff37009b" : return "indigo";
            case "#ff370037": return "blueviolet";
            case "#ff78001e": return "pink";
            case "#ff32c832": return "springgreen";

        }
       return null;
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

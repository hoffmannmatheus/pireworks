package com.pireworks.app.pireworks.Helper;

import com.google.gson.Gson;
import com.google.gson.JsonObject;
import com.pireworks.app.pireworks.data.Configuration;

import java.io.IOException;
import java.io.OutputStream;

/**
 * Created by Ezhil on 17-Nov-16.
 */
public class BluetoothHelper {

    public void sendMessage(OutputStream mOutputStream, Configuration config){

        if( mOutputStream !=null){
            /**
             * TODO:
             * When requesting the current configuration, use "action" = "get".
             * If setting a config, use "action" = "set".
             * When setting a config, the configuration will be expected in a "config" key.
             *
             * Note the '(new Gson()).toJson(...)'. This is just to translate a 'json builder' to an
             * actual string, so it can appear in the text field.
             */

            JsonObject builder=new JsonObject();
            builder.addProperty("action","set");
            builder.addProperty("config",config.toString());
            String jsonMessage=(new Gson()).toJson(builder);

            try{
                mOutputStream.write(jsonMessage.getBytes());
            }catch(IOException e){
                e.printStackTrace();
            }
           // appendMessage("me", jsonMessage);
        }
    }

    public void appendMessage(final String from,final String message){
       /* if (mDeviceMessagesTextView != null) {
                        runOnUiThread(new Runnable() {
                                @Override
                                public void run() {
                                        mDeviceMessagesTextView.append("\n" + from + ": " + message);
                                    }
                            });
                   }*/

    }

}

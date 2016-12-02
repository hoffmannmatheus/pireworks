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

    public void sendConfig(OutputStream mOutputStream, Configuration config){

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



            JsonObject jsonColors=new JsonObject();
            jsonColors.addProperty("C",  config.getColorHashMap().get("C"));
            jsonColors.addProperty("D",  config.getColorHashMap().get("D"));
            jsonColors.addProperty("E",  config.getColorHashMap().get("E"));
            jsonColors.addProperty("F",  config.getColorHashMap().get("F"));
            jsonColors.addProperty("G",  config.getColorHashMap().get("G"));
            jsonColors.addProperty("A",  config.getColorHashMap().get("A"));
            jsonColors.addProperty("B",  config.getColorHashMap().get("B"));

            JsonObject jsonConfig=new JsonObject();
            jsonConfig.addProperty("trigger_threshold", config.getTriggerThreshold());
            jsonConfig.addProperty("trigger_offset", config.getTriggerOffset());
            jsonConfig.add("colors", jsonColors );

            JsonObject builder=new JsonObject();
            builder.addProperty("action","set");
            builder.add("config", jsonConfig);
            String jsonMessage=(new Gson()).toJson(builder);

            try{
                mOutputStream.write(jsonMessage.getBytes());
            }catch(IOException e){
                e.printStackTrace();
            }
        }
    }

    public void requestConfig(OutputStream mOutputStream){

        if( mOutputStream !=null){
            JsonObject builder=new JsonObject();
            builder.addProperty("action","get");
            String jsonMessage=(new Gson()).toJson(builder);

            try{
                mOutputStream.write(jsonMessage.getBytes());
            }catch(IOException e){
                e.printStackTrace();
            }
        }
    }
}

package com.pireworks.app.pireworks.data;

import java.util.HashMap;
import java.util.Map;

/**
 * Created by Ezhil on 10-Nov-16.
 */

public class Configuration {

     private Map<String, String> colorMap = new HashMap<String, String>();


    private int mAmplitudeIntensity;
    private int triggerThreshold;
    private int triggerOffset;

    public Configuration(int threshold, int offset, int intensity, HashMap<String,String> userColorMap){
        this.setTriggerThreshold(threshold);
        this.setTriggerOffset(offset);
        this.setmAmplitudeIntensity(intensity);
        this.setUserColorMap(userColorMap);
    }

    public Configuration(int threshold, int offset, int intensity){
        this.setTriggerThreshold(threshold);
        this.setTriggerOffset(offset);
        this.setmAmplitudeIntensity(intensity);
        this.setDefaultColorMap();
    }

    public int getTriggerThreshold(){
        return this.triggerThreshold;
    }

    public  int getTriggerOffset(){
        return this.triggerOffset;
    }

    public int getAmplitudeIntensity() {
        return this.mAmplitudeIntensity;
    }

    private void setTriggerThreshold(int triggerThreshold){
        this.triggerThreshold = triggerThreshold;
    }

    private void setTriggerOffset(int triggerOffset){
        this.triggerOffset = triggerOffset;
    }
    private void setmAmplitudeIntensity(int amplitudeIntensity){
        this.mAmplitudeIntensity = amplitudeIntensity;
    }

    private void setDefaultColorMap(){
        colorMap.put("C",  "FF0000");
        colorMap.put("D",  "FFFF00");
        colorMap.put("E",  "FF00FF");
        colorMap.put("F",  "FFFFFF");
        colorMap.put("G",  "00FFFF");
        colorMap.put("A",  "0000FF");
        colorMap.put("B",  "FF0FF0");

    }

    private void setUserColorMap(HashMap<String,String> userColorMap){
        this.colorMap = userColorMap;
    }

    public HashMap<String,String> getColHashMap(){
        return (HashMap<String, String>) this.colorMap;
    }
}

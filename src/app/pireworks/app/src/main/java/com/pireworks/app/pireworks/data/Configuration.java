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
        colorMap = getDefaultColorMap();
    }

    private void setUserColorMap(HashMap<String,String> userColorMap){
        this.colorMap = userColorMap;
    }

    public Map<String,String> getColorHashMap(){
        return this.colorMap;
    }

    public static HashMap<String, String> getDefaultColorMap() {
        HashMap<String, String> defaultMap = new HashMap<String, String>();
        defaultMap.put("C",  "red");
        defaultMap.put("D",  "green");
        defaultMap.put("E",  "blue");
        defaultMap.put("F",  "purple");
        defaultMap.put("G",  "teal");
        defaultMap.put("A",  "aquamarine");
        defaultMap.put("B",  "indigo");
        return defaultMap;
    }
}

package com.pireworks.app.pireworks;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;

public class SyncActivity extends AppCompatActivity implements View.OnClickListener {

    /**
     * The Log tag.
     */
    private static final String TAG = "SyncActivity";


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        Log.d(TAG, "onCreate");
        setContentView(R.layout.activity_sync);

        Button button = (Button) findViewById(R.id.sync_open);
        button.setOnClickListener(this);
    }

    @Override
    protected void onStart() {
        super.onStart();
        Log.d(TAG, "onStart");
    }

    @Override
    protected void onResume() {
        super.onResume();
        Log.d(TAG, "onResume");
    }

    @Override
    public void onClick(View view) {
        switch (view.getId()) {
            case R.id.sync_open:
                Intent intent = new Intent(this, PireworksActivity.class);
                startActivity(intent);
                break;
        }
    }
}

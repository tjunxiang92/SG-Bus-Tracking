package com.jxdesigns.sbsbustracking;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        final TextView tv = (TextView) findViewById(R.id.trackingView);

        Button clickButton = (Button) findViewById(R.id.startBtn);
        clickButton.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View v) {
                tv.setText("Clicked...");
            }
        });


        Spinner busSpinner = (Spinner) findViewById(R.id.busSpinner);

        // Array of choices
        final String colors[] = {"179", "199"};

        // Application of the Array to the Spinner
        ArrayAdapter<String> spinnerArrayAdapter = new ArrayAdapter<String>(this, android.R.layout.simple_spinner_item, colors);
        spinnerArrayAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item); // The drop down view
        busSpinner.setAdapter(spinnerArrayAdapter);


        busSpinner.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> parentView, View selectedItemView, int position, long id) {
                tv.setText("Item Changed...");
                processVolley();

                Spinner startSpinner = (Spinner) findViewById(R.id.startSpinner);
                ArrayAdapter<String> spinnerArrayAdapter = new ArrayAdapter<String>(MainActivity.this, android.R.layout.simple_spinner_item, colors);
                spinnerArrayAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item); // The drop down view
                startSpinner.setAdapter(spinnerArrayAdapter);
                // Toast.makeText(MainActivity.this, colors[position], Toast.LENGTH_LONG).show();
            }

            @Override
            public void onNothingSelected(AdapterView<?> parentView) {
                Toast.makeText(MainActivity.this, "herf", Toast.LENGTH_LONG).show();
            }
        });
    }

    protected void processVolley() {
        final TextView tv = (TextView) findViewById(R.id.trackingView);
        RequestQueue queue = Volley.newRequestQueue(MainActivity.this);
        String url = "http://jxdesigns.com";//"https://by.originally.us/busbuzz/v1/bus_stops/search2";

        Map<String, String> params = new HashMap<String, String>();
        params.put("os_type", "2");
        params.put("os_version", "23");
        params.put("ver", "73.0");
        params.put("os", "android");
        params.put("keywords", "199");

        JSONObject pJSON = new JSONObject(params);

        // Request a string response from the provided URL.
        StringRequest stringRequest = new StringRequest(Request.Method.GET, url,
                new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {
                        tv.setText(response);
                        //showJSON(response);
                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        tv.setText("Error Occured.");
                        // Toast.makeText(MainActivity.this,error.getMessage(),Toast.LENGTH_LONG).show();
                    }
                }) {
                    @Override
                    public Map<String, String> getHeaders() throws AuthFailureError {
                        Map<String, String>  params = new HashMap<String, String>();
                        params.put("userid", "160200");
                        params.put("secret", "ad1548d6791f37c15642a086966ab3f3d80919a6");
                        params.put("Content-Type", "application/json; charset=UTF-8");
                        params.put("Content-Length", "74");
                        params.put("Host", "by.originally.us");
                        params.put("Connection", "close");
                        params.put("Accept-Encoding", "gzip");
                        params.put("User-Agent", "okhttp/2.2.0");

                        return params;
                    }
                };

        queue.add(stringRequest);
    }

    private void showJSON(String json){
        JSONObject jsonObject = null;
        try {
            jsonObject = new JSONObject(json);
            JSONArray users = jsonObject.getJSONArray("result");
        } catch (JSONException e) {
            e.printStackTrace();
        }

    }
}

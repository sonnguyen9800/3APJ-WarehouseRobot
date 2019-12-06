package com.example.WarehouseRonbot;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Build;
import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ListView;
import android.widget.Toast;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

import com.example.warehouseronbot.R;

import java.util.ArrayList;
import java.util.Optional;
import java.util.Set;

public class HomeActivity extends AppCompatActivity implements AdapterView.OnItemClickListener {

    public static ArrayList<Device> devices;
    public static String EXTRA_ADDRESS = "device_address";
    //widgets
    ListView devicelist;
    CustomAdapter customAdapter;
    //Bluetooth
    private BluetoothAdapter myBluetooth = null;
    private Set<BluetoothDevice> pairedDevices;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_home);

        //Calling widgets
        devicelist = findViewById(R.id.listView);

        //if the device has bluetooth
        myBluetooth = BluetoothAdapter.getDefaultAdapter();

        if (myBluetooth == null) {
            //Show a mensag. that the device has no bluetooth adapter
            Toast.makeText(getApplicationContext(), "Bluetooth Device Not Available", Toast.LENGTH_LONG).show();
            //finish apk
            finish();
        }
//        else if(!myBluetooth.isEnabled())
//        {
//            //Ask to the user turn the bluetooth on
//            Intent turnBTon = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
//            startActivityForResult(turnBTon,1);
//        } else if (myBluetooth.isEnabled()) {
//            pairedDevicesList();
//        }
    }

    @Override
    protected void onResume() {
        super.onResume();
        Toast.makeText(this, "On Resume", Toast.LENGTH_SHORT).show();
        myBluetooth = BluetoothAdapter.getDefaultAdapter();
        if (!myBluetooth.isEnabled()) {
            //Ask to the user turn the bluetooth on
            Intent turnBTon = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
            startActivityForResult(turnBTon, 1);
        } else {
            pairedDevicesList();
        }
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        if (requestCode == 1) {
            if (resultCode == RESULT_OK) {
                pairedDevicesList();
            } else {
                finish();
            }
        } else if (requestCode == 2) {
            if (resultCode == RESULT_OK) {

            } else {
                // Error callback when connection is failed
                SharedPreferences preferences = getSharedPreferences("default_device", MODE_PRIVATE);
                preferences.edit().putString("address", null).apply();
            }
        }

    }

    //    Display paired devices
    private void pairedDevicesList() {
        pairedDevices = myBluetooth.getBondedDevices();
        devices = new ArrayList<>();

        if (pairedDevices.size() > 0) {
            devicelist.setVisibility(View.VISIBLE);
            for (BluetoothDevice bt : pairedDevices) {
                devices.add(new Device(bt.getName(), bt.getAddress())); //Get the device's name and the address
            }

            // Auto connecting bluetooth
            SharedPreferences preferences = getSharedPreferences("default_device", MODE_PRIVATE);
            String defaultAddress;
            if ((defaultAddress = preferences.getString("address", null)) != null) {


                Optional<Device> myDevice = devices.stream().filter(n->n.getAddress().equals(defaultAddress)).findFirst();
                if (myDevice.isPresent()) {
                    Toast.makeText(this, "Auto Connect", Toast.LENGTH_SHORT).show();
                    navigateToController(myDevice.get().getName(), myDevice.get().getAddress());
                } else {
                    preferences.edit().putString("address", null).apply();
                }

//                API Greater than 24
//                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.N) {
//                    Optional<Device> myDevice = null;
//                    myDevice = devices.stream().filter(n -> n.getAddress().equals(defaultAddress)).findFirst();
//                    if (myDevice.isPresent()) {
//                        Toast.makeText(this, "Auto Connect", Toast.LENGTH_SHORT).show();
//                        navigateToController(myDevice.get().getName(), myDevice.get().getAddress());
//                    } else {
//                        preferences.edit().putString("address", null).apply();
//                    }
//                }
////                For API machine level below 24+------------
//                else {
//                    Device myDevice = null;
//                    for (Device device : devices) {
//                        if (device.getAddress().equals(defaultAddress)) {
//                            myDevice = device;
//                        }
//                    }
//                    if (myDevice != null) {
//                        Toast.makeText(this, "Auto Connect", Toast.LENGTH_SHORT).show();
//                        navigateToController(myDevice.getName(), myDevice.getAddress());
//                    } else {
//                        preferences.edit().putString("address", null).apply();
//                    }
//                }

            }
        } else {
            devicelist.setVisibility(View.GONE);
            Toast.makeText(getApplicationContext(), "No Paired Bluetooth Devices Found.", Toast.LENGTH_LONG).show();
        }

//        final ArrayAdapter adapter = new ArrayAdapter(this,android.R.layout.simple_list_item_1, list);
        customAdapter = new CustomAdapter(this);
        devicelist.setAdapter(customAdapter);
        devicelist.setOnItemClickListener(this); //Method called when the device from the list is clicked
    }

    @Override
    public void onItemClick(AdapterView<?> adapterView, View view, int i, long l) {
        String name = devices.get(i).getName();
        String address = devices.get(i).getAddress();

        SharedPreferences preferences = getSharedPreferences("default_device", MODE_PRIVATE);
        preferences.edit().putString("address", address).apply();

        navigateToController(name, address);
    }

    public void navigateToController(String name, String address) {
        // Make an intent to start next activity.
        Intent intent = new Intent(HomeActivity.this, CarControllingActivity.class);
        //Change the activity.
        intent.putExtra("device_address", address); //this will be received at ledControl (class) Activity
        intent.putExtra("device_name", name);
        startActivityForResult(intent, 2);
    }


    public void onBluetoothSettingClicked(View view) {
//        Intent intent = new Intent(Intent.ACTION_MAIN, null);
//        intent.addCategory(Intent.CATEGORY_LAUNCHER);
//        ComponentName cn = new ComponentName("com.android.settings", "com.android.settings.bluetoothSettings");
//        intent.setComponent(cn);
//        intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
//        startActivity(intent);
        Intent intentOpenBluetoothSettings = new Intent();
        intentOpenBluetoothSettings.setAction(android.provider.Settings.ACTION_BLUETOOTH_SETTINGS);
        startActivityForResult(intentOpenBluetoothSettings, 2);
    }
}

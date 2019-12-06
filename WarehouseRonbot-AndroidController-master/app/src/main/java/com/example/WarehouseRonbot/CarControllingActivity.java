package com.example.WarehouseRonbot;

import android.annotation.SuppressLint;
import android.app.Activity;
import android.app.ProgressDialog;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothSocket;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Handler;
import android.util.Log;
import android.view.MotionEvent;
import android.view.View;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.Switch;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.example.warehouseronbot.R;

import java.io.IOException;
import java.util.UUID;

public class CarControllingActivity extends AppCompatActivity implements JoystickView.JoystickListener {
    private static final String TAG = CarControllingActivity.class.getName();

    private static final String SAMPLE_MESSAGE = CarControllingActivity.class.getName() + " SIMPLE TEXT";
    //SPP UUID. Look for it
    static final UUID myUUID = UUID.fromString("00001101-0000-1000-8000-00805F9B34FB");
    private Button test, disconnect;
    private Switch autoSwitch;
    private ImageButton rotateLeftBtn, rotateRightBtn;
    private String name = null;
    private String address = null;
    BluetoothSocket btSocket = null;
    BluetoothAdapter myBluetooth = null;
    private boolean isBtConnected = false;
    private ProgressDialog progress;
    private ConnectBT connectBT;

    @SuppressLint("ClickableViewAccessibility")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        Log.i(TAG, "onCreate: create the activity");
        Intent intent = getIntent();
        name = intent.getStringExtra("device_name");
        address = intent.getStringExtra("device_address"); //receive the address of the bluetooth device

        //view of the ledControl
        setContentView(R.layout.activity_car_controlling);

        //call the widgtes
        test = findViewById(R.id.test);
        disconnect = findViewById(R.id.disconnect);
        autoSwitch = findViewById(R.id.autoSwitch);
        rotateLeftBtn = findViewById(R.id.rotateLeftBtn);
        rotateRightBtn = findViewById(R.id.rotateRightBtn);

        connectBT = new ConnectBT(); //Call the class to connect
        connectBT.execute();

        test.setOnClickListener(new View.OnClickListener() {
            @Override

            public void onClick(View v) {

                sendMessage(SAMPLE_MESSAGE);      //method to turn on
            }
        });

        disconnect.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                disconnect(); //close connection
            }
        });

        rotateLeftBtn.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View view, MotionEvent motionEvent) {

                if (motionEvent.getAction() == MotionEvent.ACTION_DOWN) {
                    Toast.makeText(CarControllingActivity.this, "Rotate left", Toast.LENGTH_SHORT).show();
                    sendMessage("W");
                    return true;
                } else if (motionEvent.getAction() == MotionEvent.ACTION_UP) {
                    Toast.makeText(CarControllingActivity.this, "Stop", Toast.LENGTH_SHORT).show();
                    sendMessage("S");
                    return true;
                }
                return false;
            }
        });

        rotateRightBtn.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View view, MotionEvent motionEvent) {
                if (motionEvent.getAction() == MotionEvent.ACTION_DOWN) {
                    Toast.makeText(CarControllingActivity.this, "Rotate right", Toast.LENGTH_SHORT).show();
                    sendMessage("C");
                    return true;
                } else if (motionEvent.getAction() == MotionEvent.ACTION_UP) {
                    Toast.makeText(CarControllingActivity.this, "Stop", Toast.LENGTH_SHORT).show();
                    sendMessage("S");
                    return true;
                }
                return false;
            }
        });

        IntentFilter filter = new IntentFilter();
        filter.addAction(BluetoothDevice.ACTION_ACL_CONNECTED);
        filter.addAction(BluetoothDevice.ACTION_ACL_DISCONNECT_REQUESTED);
        filter.addAction(BluetoothDevice.ACTION_ACL_DISCONNECTED);
        this.registerReceiver(mReceiver, filter);

    }

    private String lastMessage;
    public void sendMessage(String message) {
        Log.i(TAG, "sendMessage: " + message);
        if (btSocket != null) {
            try {

                if (!message.equals(lastMessage)) {
                    lastMessage = message;
                    btSocket.getOutputStream().write(message.getBytes());
//                    Toast.makeText(this, message, Toast.LENGTH_SHORT).show();
                }
            } catch (IOException e) {
                Log.e(TAG, "sendMessage: TAG");
            }
        }
    }

    private char lastChar = 'S';
    public void sendMessage(char message) {
        Log.i(TAG, "sendMessage: " + message);
        if (btSocket != null) {
            try {

                if (message != lastChar) {
                    lastChar = message;
                    btSocket.getOutputStream().write(message);
//                    Toast.makeText(this, message, Toast.LENGTH_SHORT).show();
                }
            } catch (IOException e) {
                Log.e(TAG, "sendMessage: TAG");
            }
        }
    }

    public String getAddress() {
        return this.address;
    }


//    // fast way to call Toast
//    private void msg(String s) {
//        Toast.makeText(getApplicationContext(), s, Toast.LENGTH_LONG).show();
//    }

    @Override
    public void onJoystickMoved(float xPercent, float yPercent, int id, int direction) {

        if (direction == JoystickView.STICK_UP) {
            sendMessage('F');
            Log.i("Direction", "Up");
        } else if (direction == JoystickView.STICK_UPRIGHT) {
            sendMessage('2');
            Log.i("Direction", "Up-right");
        } else if (direction == JoystickView.STICK_RIGHT) {
            sendMessage('R');
            Log.i("Direction", "Right");
        } else if (direction == JoystickView.STICK_DOWNRIGHT) {
            sendMessage('5');
            Log.i("Direction", "Down-right");
        } else if (direction == JoystickView.STICK_DOWN) {
            sendMessage('B');
            Log.i("Direction", "Down");
        } else if (direction == JoystickView.STICK_DOWNLEFT) {
            sendMessage('8');
            Log.i("Direction", "Down-left");
        } else if (direction == JoystickView.STICK_LEFT) {
            sendMessage('L');
            Log.i("Direction", "Left");
        } else if (direction == JoystickView.STICK_UPLEFT) {
            sendMessage('b');
            Log.i("Direction", "Up-left");
        } else if (direction == JoystickView.STICK_NONE) {
            Log.i("Direction", "None");
            sendMessage('S');
        }

        Log.i("X", "" + xPercent);
        Log.i("Y", "" + yPercent);
    }

    public void disconnect() {
        if (btSocket != null) //If the btSocket is busy
        {
            try {
                btSocket.close(); //close connection
            } catch (IOException e) {
                Log.e(TAG, "Disconnect: ", e.getCause());
            }
        }
        finish(); //return to the first layout
    }

    // fast way to call Toast
    private void msg(String s)
    {
        Toast.makeText(getApplicationContext(),s,Toast.LENGTH_LONG).show();
    }

    private class ConnectBT extends AsyncTask<Void, Void, Void>  // UI thread
    {
        private boolean ConnectSuccess = true; //if it's here, it's almost connected

        @Override
        protected void onPreExecute()
        {
            progress = ProgressDialog.show(CarControllingActivity.this, "Connecting...", "Please wait!!!");  //show a progress dialog
        }

        @Override
        protected Void doInBackground(Void... devices) //while the progress dialog is shown, the connection is done in background
        {
            try
            {
                if (btSocket == null || !isBtConnected)
                {
                    myBluetooth = BluetoothAdapter.getDefaultAdapter();//get the mobile bluetooth device
                    BluetoothDevice dispositivo = myBluetooth.getRemoteDevice(address);//connects to the device's address and checks if it's available
                    btSocket = dispositivo.createInsecureRfcommSocketToServiceRecord(myUUID);//create a RFCOMM (SPP) connection
                    BluetoothAdapter.getDefaultAdapter().cancelDiscovery();
                    btSocket.connect();//start connection
                }
            }
            catch (IOException e)
            {
//                Toast.makeText(CarControllingActivity.this, "Error in catch", Toast.LENGTH_SHORT).show();
                ConnectSuccess = false;//if the try failed, you can check the exception here
            }
            return null;
        }
        @Override
        protected void onPostExecute(Void result) //after the doInBackground, it checks if everything went fine
        {
            super.onPostExecute(result);

            if (!ConnectSuccess)
            {
                msg("Connection Failed. Is it a SPP Bluetooth? Try again.");
                progress.dismiss();
                finish();
            }
            else
            {
                Toast.makeText(CarControllingActivity.this, "Connected", Toast.LENGTH_SHORT).show();
                isBtConnected = true;
                beginListenToData();
            }
            progress.dismiss();
        }
    }

    @Override
    public void onBackPressed() {
        disconnect();
        super.onBackPressed();
    }

    private Boolean stopThread;
    Thread thread;
    byte buffer[];
    public void beginListenToData() {
        sendMessage("PP");
        final Handler handler = new Handler();
        stopThread = false;
        buffer = new byte[1024];
        Thread thread  = new Thread(new Runnable() {
            public void run()
            {
                while(!Thread.currentThread().isInterrupted() && !stopThread)
                {

                    try
                    {
                        int byteCount = btSocket.getInputStream().available();
                        if(byteCount > 0)
                        {

                            byte[] rawBytes = new byte[byteCount];
                            btSocket.getInputStream().read(rawBytes);
                            String string = new String(rawBytes);

                            runOnUiThread(new Runnable() {
                                @Override
                                public void run() {
                                    Toast.makeText(CarControllingActivity.this, "Recieved: " + string, Toast.LENGTH_SHORT).show();
                                }
                            });

//                            if (string.equals("M:A")) {
//                                Log.i("Message", "M:A");
//                                handler.post(new Runnable() {
//                                    public void run()
//                                    {
//                                        Toast.makeText(CarControllingActivity.this, string, Toast.LENGTH_SHORT).show();
//                                        autoSwitch.setChecked(true);
//                                    }
//                                });
//                            } else if (string.equals("M:M")) {
//                                handler.post(new Runnable() {
//                                    public void run()
//                                    {
//                                        Toast.makeText(CarControllingActivity.this, string, Toast.LENGTH_SHORT).show();
//                                        autoSwitch.setChecked(false);
//                                    }
//                                });
//                            }
                        }
                    }
                    catch (IOException ex)
                    {
                        stopThread = true;
                    }
                }
            }
        });
        thread.start();
    }

    //The BroadcastReceiver that listens for bluetooth broadcasts
    private final BroadcastReceiver mReceiver = new BroadcastReceiver() {
        @Override
        public void onReceive(Context context, Intent intent) {
            String action = intent.getAction();
            BluetoothDevice device = intent.getParcelableExtra(BluetoothDevice.EXTRA_DEVICE);

            if (BluetoothDevice.ACTION_FOUND.equals(action)) {
            }
            else if (BluetoothDevice.ACTION_ACL_CONNECTED.equals(action)) {
            }
            else if (BluetoothAdapter.ACTION_DISCOVERY_FINISHED.equals(action)) {
            }
            else if (BluetoothDevice.ACTION_ACL_DISCONNECT_REQUESTED.equals(action)) {
            }
            else if (BluetoothDevice.ACTION_ACL_DISCONNECTED.equals(action)) {
                finish();
            }
        }
    };

}

package com.example.WarehouseRonbot;

import android.app.Activity;
import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.TextView;

import com.example.warehouseronbot.R;

public class CustomAdapter extends BaseAdapter {

    private Activity context;

    public CustomAdapter(Activity context) {
        this.context = context;
    }

    @Override
    public int getCount() {
        return HomeActivity.devices.size();
    }

    @Override
    public Object getItem(int i) {
        return null;
    }

    @Override
    public long getItemId(int i) {
        return 0;
    }

    @Override
    public View getView(int i, View view, ViewGroup viewGroup) {

        ViewHolder viewHolder;
        if (view == null) {
            LayoutInflater inflater = (LayoutInflater) context.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
            view = inflater.inflate(R.layout.custom_adapter_layout, null);
            viewHolder = new ViewHolder(view);
            view.setTag(viewHolder);
        } else {
            viewHolder = (ViewHolder) view.getTag();
        }

        viewHolder.name.setText(HomeActivity.devices.get(i).getName());
        viewHolder.address.setText(HomeActivity.devices.get(i).getAddress());

        return view;
    }

    private class ViewHolder {
        private TextView name;
        private TextView address;

        public ViewHolder(View view) {
            this.name = view.findViewById(R.id.name);
            this.address = view.findViewById(R.id.address);
        }
    }
}

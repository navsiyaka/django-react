import React from "react";
import {ResponsiveContainer, LineChart, CartesianGrid, XAxis, YAxis, Tooltip, Legend, Line, Brush} from "recharts";


export default ({data, syncId, keys}) =>
    <ResponsiveContainer width='100%' aspect={5.0/3.0}>
        <LineChart data={data}
                   margin={{top: 5, right: 30, left: 20, bottom: 5}}
                   syncId={syncId}
        >
            <CartesianGrid strokeDasharray="3 3"/>
            <XAxis dataKey="name"/>
            <YAxis/>
            <Tooltip/>
            <Legend/>
            {keys.map(key =>
                <Line type="monotone" dataKey={key} stroke="#8884d8" key={key} />
            )}
            <Brush data={data}/>
        </LineChart>
    </ResponsiveContainer>;

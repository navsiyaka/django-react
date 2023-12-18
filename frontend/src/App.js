import React from 'react';
import {ProvideDayStats} from "./hooks/useDayStats";
import Main from './containers/Main';

function App() {
    return (
        <ProvideDayStats>
            <Main/>
        </ProvideDayStats>
    );
}

export default App;

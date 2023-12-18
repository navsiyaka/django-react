import React, {useState, useContext, createContext} from "react";
import client from '../apiClient';

const dayStatsContext = createContext({});


export function ProvideDayStats({children}) {
    const dayStats = useProvideDayStats();
    return <dayStatsContext.Provider value={dayStats}>{children}</dayStatsContext.Provider>;
}

export const useDayStats = () => {
    return useContext(dayStatsContext);
};

function useProvideDayStats() {
    const [state, setState] = useState({
        isInProgress: undefined,
        isError: undefined,
        isSuccess: undefined,
        dateRange: undefined,
        data: undefined
    });

    const load = (dateRange) => {
        setState({
            isInProgress: true,
            dateRange,
            data: state.data
        });

        client
            .get(
                '/day-stats/',
                {
                    params: {
                        start_date: dateRange.start.format('YYYY-MM-DD'),
                        end_date: dateRange.end.format('YYYY-MM-DD')
                    }
                }
            )
            .then(response => {
                setState({
                    isSuccess: true,
                    data: response.data,
                    dateRange
                })
            })
            .catch(reason => {
                setState({
                    isError: true,
                    dateRange
                })
            });
    };

    return {
        load,
        ...state,
    };
}

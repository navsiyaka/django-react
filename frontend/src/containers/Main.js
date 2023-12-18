import React, {useState, useEffect} from "react";
import {useDayStats} from "../hooks/useDayStats";
import AutoComplete from './AutoComplete';
import Chart from './Chart';
import Grid from '@material-ui/core/Grid';
import Paper from '@material-ui/core/Paper'
import Typography from '@material-ui/core/Typography'
import DateRangePicker from 'react-daterange-picker';
import 'react-daterange-picker/dist/css/react-calendar.css';
import styled from 'styled-components';
import Moment from 'moment';
import {extendMoment} from 'moment-range'

const moment = extendMoment(Moment);


const MainContainer = styled(Grid).attrs({
    container: true
})`
  padding: 20px;
  flex-direction: column;
  align-items: stretch;
  
  @media (min-width: 600px) {
    flex-direction: column;
  }
`;

const ChartContainer = styled(Grid).attrs({
    item: true
})`
  min-width: 49%;
  text-align: center;
`;


const BlockContainer = styled(Paper)`
  padding: 20px;
  margin: 10px;
`;

function onlyUniqueIds(value, index, self) {
    return self.map(item => item.id).indexOf(value.id) === index;
}

export default function Main() {
    const dayStats = useDayStats();

    const [dateRange, setDateRange] = useState(
        moment.range(
            moment("2019-06-24"),
            moment("2019-06-30"),
        )
    );
    const [filterChoices, setFilterChoices] = useState({
        datasources: [],
        campaigns: []
    });
    const [filterSelected, setFilterSelected] = useState({
        datasources: [],
        campaigns: []
    });

    const [chartsData, setChartsData] = useState({
        clicks: [],
        impressions: [],
        keys: []
    });

    // Calculate visible campaigns
    const getChartKeys = () => {
        let chartKeys = [];
        (dayStats.data || []).forEach(item => {
            const datasourcesIds = filterSelected.datasources.map(v => v.id);
            const campaignsIds = filterSelected.campaigns.map(v => v.id);

            const isSelectedDatasource = datasourcesIds.indexOf(item.datasource.id) !== -1;
            const isSelectedCampaign = campaignsIds.indexOf(item.campaign.id) !== -1;

            // Skip not selected datasources and campaigns
            if (!isSelectedDatasource && !isSelectedCampaign) {
                return
            }

            chartKeys.push(item.campaign.name);
        });
        chartKeys = chartKeys.filter((value, index, self) => self.indexOf(value) === index);
        return chartKeys
    };

    const updateFilterChoices = () => {
        if (dayStats.data) {
            const datasources = dayStats.data.map(item => item.datasource).filter(onlyUniqueIds);
            const campaigns = dayStats.data.map(item => item.campaign).filter(onlyUniqueIds);

            const datasourcesIds = datasources.map(v => v.id);
            const campaignsIds = campaigns.map(v => v.id);

            setFilterChoices({
                datasources,
                campaigns
            });
            setFilterSelected({
                datasources: filterSelected.datasources.filter(v => datasourcesIds.indexOf(v.id) !== -1),
                campaigns: filterSelected.campaigns.filter(v => campaignsIds.indexOf(v.id) !== -1)
            })
        } else {
            setFilterChoices({
                datasources: [],
                campaigns: [],
            })
        }
    };

    const updateChartData = () => {
        const newChartData = {
            clicks: [],
            impressions: [],
            keys: []
        };

        if (!dayStats.data) {
            setChartsData(newChartData);
            return
        }

        const chartKeys = getChartKeys();
        newChartData.keys = chartKeys;

        let curDate = dateRange.start.clone();
        while (true) {
            if (curDate.isAfter(dateRange.end)) {
                break;
            }

            const dayItemClicks = {
                name: curDate.format('YYYY/MM/DD')
            };
            const dayItemImpressions = {
                name: curDate.format('YYYY/MM/DD')
            };

            const dayItems = dayStats.data
                .filter(item => moment(item.date).isSame(curDate));

            chartKeys.forEach(key => {
                const matchingItems = dayItems.filter(i => i.campaign.name === key);

                if (matchingItems.length === 1) {
                    dayItemClicks[key] = matchingItems[0].clicks;
                    dayItemImpressions[key] = matchingItems[0].impressions;
                } else {
                    dayItemClicks[key] = 0;
                    dayItemImpressions[key] = 0;
                }
            });

            newChartData.clicks.push(dayItemClicks);
            newChartData.impressions.push(dayItemImpressions);

            curDate = curDate.add(1, 'day');
        }

        setChartsData(newChartData);
    };


    useEffect(updateFilterChoices,
        [dayStats.data]
    );

    useEffect(updateChartData,
        [filterSelected, dayStats.data]
    );

    useEffect(
        () => dayStats.load(dateRange),
        [dateRange]
    );

    return (
        <MainContainer>

            <Grid item xs={12}>
                <BlockContainer>

                    <Typography variant={"h4"}>
                        Filters
                    </Typography>

                    <Grid container direction='row' spacing={10}>
                        <Grid item xs={12} md={4} lg={4}>
                            <AutoComplete label="Datasources"
                                          isLoading={dayStats.isInProgress}
                                          source={filterChoices.datasources}
                                          values={filterSelected.datasources}
                                          onChange={v => setFilterSelected({
                                              datasources: v,
                                              campaigns: filterSelected.campaigns
                                          })}
                            />
                            <AutoComplete label="Campaigns"
                                          isLoading={dayStats.isInProgress}
                                          source={filterChoices.campaigns}
                                          values={filterSelected.campaigns}
                                          onChange={v => setFilterSelected({
                                              campaigns: v,
                                              datasources: filterSelected.datasources
                                          })}
                            />
                        </Grid>

                        <Grid item xs={12} md={4}>
                            <DateRangePicker
                                firstOfWeek={1}
                                numberOfCalendars={1}
                                selectionType='range'
                                minimumDate={new Date(2000, 1, 1)}
                                showLegend={true}
                                value={dateRange}
                                onSelect={v => setDateRange(v)}
                            />
                        </Grid>
                    </Grid>

                </BlockContainer>
            </Grid>

            <Grid item>
                <BlockContainer>
                    <Grid container direction='row'>

                        <ChartContainer>
                            <Typography variant='h5'>
                                Clicks
                            </Typography>
                            <Chart syncId='sync-id'
                                   data={chartsData.clicks}
                                   keys={chartsData.keys}
                            />
                        </ChartContainer>

                        <ChartContainer>
                            <Typography variant='h5'>
                                Impressions
                            </Typography>
                            <Chart syncId='sync-id'
                                   data={chartsData.impressions}
                                   keys={chartsData.keys}
                            />
                        </ChartContainer>

                    </Grid>
                </BlockContainer>
            </Grid>

        </MainContainer>

    )
}

import React from 'react';
import {makeStyles, useTheme} from '@material-ui/core/styles';
import Input from '@material-ui/core/Input';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';
import Chip from '@material-ui/core/Chip';


const useStyles = makeStyles(theme => ({
    root: {
        display: 'flex',
        flexWrap: 'wrap',
    },
    formControl: {
        width: '100%',
        marginTop: '20px'
    },
    chips: {
        display: 'flex',
        flexWrap: 'wrap',
    },
    chip: {
        margin: 2,
    }
}));

const ITEM_HEIGHT = 48;
const ITEM_PADDING_TOP = 8;
const MenuProps = {
    minHeight: 200,
    PaperProps: {
        style: {
            maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
        },
    },
};

function getStyles(name, personName, theme) {
    return {
        fontWeight:
            personName.indexOf(name) === -1
                ? theme.typography.fontWeightRegular
                : theme.typography.fontWeightMedium,
    };
}

export default function AutoComplete({source, label = 'Label', isLoading, onChange, values}) {
    const classes = useStyles();
    const theme = useTheme();

    const getItemByName = name => {
        const matches = source.filter(item => item.name === name);

        if (matches.length === 1) {
            return matches[0];
        }
    };

    const handleChange = event => {
        const items = event.target.value.map(name => getItemByName(name));
        onChange(items);
    };

    const handleDelete = name => {
        const items = values.filter(v => v.name !== name);
        onChange(items);
    };

    return (
        <FormControl className={classes.formControl} disabled={isLoading}>
            <InputLabel htmlFor="select-multiple-chip" shrink>
                {label}
            </InputLabel>
            <Select
                multiple
                value={values.map(i => i.name)}
                onChange={handleChange}
                input={<Input id="select-multiple-chip"/>}
                renderValue={selected => (
                    <div className={classes.chips}>
                        {selected.map(name => (
                            <Chip key={name} label={name} className={classes.chip} onDelete={() => handleDelete(name)}/>
                        ))}
                    </div>
                )}
                MenuProps={MenuProps}
            >
                {source.map(item => (
                    <MenuItem key={item.name} value={item.name}
                              style={getStyles(item.name, values.map(v => v.name), theme)}>
                        {item.name}
                    </MenuItem>
                ))}
            </Select>
        </FormControl>
    );
}

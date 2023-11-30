import React from 'react';
import { useState, useEffect } from 'react';
import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';
import styles from './index.module.css';
import { Typography } from '@mui/material';
import Button from '@mui/material/Button';
import { useNavigate } from 'react-router-dom';
import { CircularProgress } from "@mui/material";
import { MenuItem, Checkbox, ListItemText, Select, InputLabel, FormControl, OutlinedInput, Tooltip } from '@mui/material';
import InfoIcon from '@mui/icons-material/Info';

const Home = () => {
    const [received, setReceived] = useState(false);
    const [loading, setLoading] = useState(false);
    const [models, setModels] = useState([]);
    const [path, setPath] = useState("");

    const modelList = [
        'kde',
        'hist',
        'hist-line',
        'kde_hist',
        'graph',
        'spy',
    ]
    useEffect(() => {
        if(received === true) {
            setLoading(true);
            let worked = APIcall();

            if(worked) {
                setLoading(false);
                getResults();
            }

        }

    }, [received]);

    let navigate = useNavigate();
    const getResults = () => {
        let respath = '/results';
        navigate(respath, {state: {
            imgpath: path,
        }});
    }
    const [params, setParams] = useState({
        'p0': "",
        'p1': "",
        'p2': "",
        'p3': "",
        'p4': "",
        plots: "",
        props: "",
        k: "",
    });

    const APIcall = async () => {
        console.log('entered here');
        await fetch('http://localhost:5000/', {
            method: 'POST',
            body: JSON.stringify(params)
            }).then((res) =>
        res.json().then((data) => {
            console.log("data to set as path:" + data);
            setPath(data);
        }));  

        return true;
    }

    const getSum1 = () => {
        setParams({
            'p1': document.getElementById('p1').value,
            'p2': document.getElementById('p2').value,
            'p3': document.getElementById('p3').value,
            'p4': document.getElementById('p4').value,
            'plots': models.join(' '),
            'props': document.getElementById('props').value,
            'k': document.getElementById('k').value,
        },);

        setReceived(true);
    }

    if(loading) {
        return(<CircularProgress />);
    }

    const handleChange = (event) => {
        const {
          target: { value },
        } = event;
        setModels(
          typeof value === 'string' ? value.split(',') : value,
        );
      };
    return (
        <Box className={styles.homepage}>

            <Typography variant='h4' className={styles.title} >Sparse Model Generator</Typography>
        
        <Box className={styles.homecontainer} >

                <Box className={styles.inputparams}>
                    <Typography variant='h6'><b>Input Parameters</b></Typography>
                    <Box className={styles.paramContainer}>
                        <TextField className={styles.numparam} id='p1' label='p1' type='number' />
                        <TextField className={styles.numparam} id='p2' label='p2' type='number' />
                        <TextField className={styles.numparam} id='p3' label='p3' type='number' />
                        <TextField className={styles.numparam} id='p4' label='p4' type='number' />
                        <TextField className={styles.numparam} id='k' label='k' type='number' />
                        <Tooltip title="each p value must be between 0 and 1. k should be greater than 2.">
                            <InfoIcon />
                        </Tooltip>
                    </Box>
                    <Box className={styles.paramContainer}> 
                        <TextField className={styles.param} id='props' label='props' type='text' />

                        <FormControl sx={{ m: 1, width: 300 }}>
                            <InputLabel>plots</InputLabel>
                            <Select
                            labelId="plots"
                            multiple
                            value={models}
                            onChange={handleChange}
                            input={<OutlinedInput label="Plot" />}
                            renderValue={(selected) => selected.join(', ')}
                            // MenuProps={MenuProps}
                            >
                            {modelList.map((name) => (
                                <MenuItem key={name} value={name}>
                                <Checkbox checked={models.indexOf(name) > -1} />
                                <ListItemText primary={name} />
                                </MenuItem>
                            ))}
                            </Select>
                        </FormControl>
                    </Box>
                </Box>

        </Box>

        <Box className={styles.generatebutton}>
            <Button 
                sx = {{height:100, width: 300, fontSize: 20, borderRadius:12}}
                size='large' 
                variant='contained' 
                onClick={() => getSum1()}>
                    Generate
            </Button>
        </Box>

        </Box>
    );
}

export default Home;
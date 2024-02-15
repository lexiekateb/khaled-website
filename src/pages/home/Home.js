import React from 'react';
import { useState, useEffect } from 'react';
import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';
import styles from './index.module.css';
import { Typography } from '@mui/material';
import Button from '@mui/material/Button';
import { useNavigate } from 'react-router-dom';
import { CircularProgress } from "@mui/material";

import { MenuItem, Checkbox, ListItemText, Select, InputLabel, FormControl, OutlinedInput, FormControlLabel } from '@mui/material';

const Home = () => {
    const [received, setReceived] = useState(false);
    const [loading, setLoading] = useState(false);
    const [models, setModels] = useState([]);
    const [path, setPath] = useState("");
    const [props, setProps] = useState([]);

    const modelList = [
        'kde',
        'hist',
        'hist-line',
        'kde_hist',
        'graph',
        'spy',
    ]

    const propList = [
        'deg',
        'in-deg',
        'out-deg',
        'clustering',
        'diameter',
        'avg-shortest-path',
        'betweenness-centrality',
        'eignvector-centrality',
        'laplacian-centrality',
        'closeness-centrality',
        'hop-count',
        'scree'
    ]

    const label = { inputProps: { 'aria-label': 'Hello?' } };

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
            setPath(data);
            return true;
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
            'props': props.join(' '),
            'k': document.getElementById('k').value,
        },);

        setReceived(true);
    }

    if(loading) {
        return(<CircularProgress />);
    }

    const handleChangeModels = (event) => {
        const {
          target: { value },
        } = event;
        setModels(
          typeof value === 'string' ? value.split(',') : value,
        );
      };

      const handleChangeProps = (event) => {
        const {
          target: { value },
        } = event;
        setProps(
          typeof value === 'string' ? value.split(',') : value,
        );
      };

    
    return (
        <Box className={styles.homepage}>

            <Typography variant='h4' className={styles.title} >Sparse Model Generator</Typography>
        
        <Box className={styles.homecontainer} >

                <Box className={styles.inputparams}>
                    <br></br>
                    <Typography variant='h6'><b>Input Parameters</b></Typography>
                    <br></br>
                    <br></br>

                    <Box className={styles.paramContainer}>
                        <input placeholder='p1' min='0' max='1' step='.1' className={styles.numparam} id='p1' label='p1' type='number' />
                        <input placeholder='p2' min='0' max='1' step='.1' className={styles.numparam} id='p2' label='p2' type='number' />
                        <input placeholder='p3' min='0' max='1' step='.1' className={styles.numparam} id='p3' label='p3' type='number' />
                        <input placeholder='p4' min='0' max='1' step='.1' className={styles.numparam} id='p4' label='p4' type='number' />
                        <input placeholder='k' min='2' className={styles.numparam} id='k' label='k' type='number' />

                    </Box>
                    <Box className={styles.allParams}>
                    <Box className={styles.plotsContainer}> 

                        <FormControl sx={{ m: 1, width: 300 }}>
                            <InputLabel>Plots</InputLabel>
                            <Select
                            labelId="plots"
                            multiple
                            value={models}
                            onChange={handleChangeModels}
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
                        <FormControl sx={{ m: 1, width: 300 }}>
                            <InputLabel>Props</InputLabel>
                            <Select
                            labelId="props"
                            multiple
                            value={props}
                            onChange={handleChangeProps}
                            input={<OutlinedInput label="Prop" />}
                            renderValue={(selected) => selected.join(', ')}
                            // MenuProps={MenuProps}
                            >
                            {propList.map((name) => (
                                <MenuItem key={name} value={name}>
                                <Checkbox checked={props.indexOf(name) > -1} />
                                <ListItemText primary={name} />
                                </MenuItem>
                            ))}
                            </Select>
                        </FormControl>
                        </Box>

                    </Box>

                    <Box>
                        <FormControlLabel
                        control = {
                            <Checkbox
                            name='Noise?'
                            value='Noise'
                            />
                        }
                        label='Plot Noise?'/>

                    </Box>
                    
                </Box>

        </Box>

        <Box className={styles.generatebutton}>
            <Button 
                sx = {{height:75, width: 300, fontSize: 20, borderRadius:10}}
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
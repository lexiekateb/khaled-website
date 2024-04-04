import React, { useState } from 'react';
import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';
import styles from './index.module.css';
import { Typography } from '@mui/material';
import Button from '@mui/material/Button';
import { CircularProgress } from "@mui/material";
import { MenuItem, Checkbox, ListItemText, Select, InputLabel, FormControl, OutlinedInput, FormControlLabel } from '@mui/material';
import { useNavigate } from 'react-router-dom';

const Home = () => {
    const [loading, setLoading] = useState(false);
    const [models, setModels] = useState([]);
    const [props, setProps] = useState([]);
    const navigate = useNavigate();

    const modelList = [
        'kde',
        'hist',
        'hist-line',
        'kde_hist',
        'graph',
        'spy',
    ];

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
    ];

    const handleChangeModels = (event) => {
        const { target: { value } } = event;
        setModels(typeof value === 'string' ? value.split(',') : value);
    };

    const handleChangeProps = (event) => {
        const { target: { value } } = event;
        setProps(typeof value === 'string' ? value.split(',') : value);
    };

    const handleSubmit = async () => {
        setLoading(true);
        navigate('/results', {
            state: {
                models,
                props
            }
        });
    }
    
    return (
        <Box className={styles.homepage}>
            <Typography variant='h4' className={styles.title}>Sparse Model Generator</Typography>
            <Box className={styles.homecontainer}>
                <Box className={styles.inputparams}>
                    <br />
                    <Typography variant='h6'><b>Input Parameters</b></Typography>
                    <br />
                    <br />
                    <Box className={styles.paramContainer}>
                        <TextField label="p1" type="number" InputProps={{ inputProps: { min: 0, max: 1, step: 0.001 } }} className={styles.numparam} />
                        <TextField label="p2" type="number" InputProps={{ inputProps: { min: 0, max: 1, step: 0.001 } }} className={styles.numparam} />
                        <TextField label="p3" type="number" InputProps={{ inputProps: { min: 0, max: 1, step: 0.001 } }} className={styles.numparam} />
                        <TextField label="p4" type="number" InputProps={{ inputProps: { min: 0, max: 1, step: 0.001 } }} className={styles.numparam} />
                        <TextField label="k" type="number" InputProps={{ inputProps: { min: 2 } }} className={styles.numparam} />
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
                </Box>
            </Box>
            <Box className={styles.generatebutton}>
                <Button
                    sx={{ height: 75, width: 300, fontSize: 20, borderRadius: 10 }}
                    size='large'
                    variant='contained'
                    onClick={handleSubmit}
                >
                    Generate
                </Button>
            </Box>
            {loading && <CircularProgress sx={{ marginTop: 2 }} />}
        </Box>
    );
}

export default Home;

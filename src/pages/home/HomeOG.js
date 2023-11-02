import React from 'react';
import { useState, useEffect } from 'react';
import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';
import styles from './index.module.css';
import { Checkbox, ListItemText, Typography } from '@mui/material';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import Button from '@mui/material/Button';
import { useNavigate } from 'react-router-dom';


const Home2 = () => {

    let navigate = useNavigate();
    const getResults = () => {
        let path = '/results';
        navigate(path);
    }

    const [params, setParams] = useState({
        'p0': 0,
        'p1': 0,
        'p2': 0,
        'p3': 0,
        'p4': 0,
    });
    
    const [sum, setSum] = useState(0);

    useEffect(() => {
        APIcall();
    }, [params]);

    const APIcall = () => {
        fetch('http://localhost:5000/', {
            method: 'POST',
            body: JSON.stringify(params)
            }).then((res) =>
        res.json().then((data) => {
            console.log(data);
        }));  
    }

    const getSum1 = () => {
        setParams({
            'plots': document.getElementById('plots').value,
            'props': document.getElementById('props').value,
            'k': document.getElementById('k').value,
        });
    }

    const kernelList = [
        'Option 1',
        'Option 2',
        'Option 3',
        'Option 4',
        'Option 5',
        'Option 6',
        'Option 7',
    ];
    

    const[model, setModel] = useState('');
    const[kernel, setKernel] = useState([]);
    const[line, setLine] = useState([]);
    const[other, setOther] = useState([]);

    const handleChangeMod = (event) => {
        setModel(event.target.value);
    }

    const handleChangeKer = (event) => {
        setKernel(event.target.value);
    }

    const handleChangeLin = (event) => {
        setLine(event.target.value);
    }

    const handleChangeOth = (event) => {
        setOther(event.target.value);
    }

    return (
        <Box className={styles.homepage}>

            <Typography variant='h4' className={styles.title} >Sparse Model Generator</Typography>
            {sum !== 0 && <Typography variant='h6'>{sum}</Typography>}
        
        <Box className={styles.homecontainer} >
            <Box className={styles.leftselections}>

                <Box className={styles.modelselector}>
                <Typography variant='h6' className={styles.break}><b>Model</b></Typography>
                    <FormControl sx={{width: 300}}>
                        <InputLabel>Model</InputLabel>
                        <Select
                        labelId='model-label'
                        id='model-simple-select'
                        value={model}
                        label='Model'
                        onChange={handleChangeMod}
                        >
                        <MenuItem value={'Kron'}>Kronecker</MenuItem>
                        <MenuItem value={'Model1'}>Model 1</MenuItem>
                        <MenuItem value={'Model2'}>Model 2</MenuItem>
                        </Select>
                    </FormControl>
                </Box>

                <Box className={styles.inputparams}>
                    <Typography variant='h6' className={styles.break}><b>Input Parameters</b></Typography>
                    <Box className={styles.paramContainer}>
                        <TextField className={styles.param} id='plots' label='plots' type='text' />
                        <TextField className={styles.param} id='props' label='props' type='text' />
                        <TextField className={styles.param} id='k' label='k' type='number' />
                        <TextField className={styles.param} id='p3' label='props' type='number' />
                        <TextField className={styles.param} id='p4' label='' type='number' />
                    <Button variant='contained' onClick={getSum1}>Sum</Button>
                    </Box>
                </Box>
                
                <Box className={styles.inputparams}>
                    <Typography variant='h6' className={styles.break}><b>Step</b></Typography>
                    <Box className={styles.paramContainer}>
                        <TextField className={styles.param} id='outlined-number' label='s0' type='number' />
                        <TextField className={styles.param} id='outlined-number' label='s1' type='number' />
                        <TextField className={styles.param} id='outlined-number' label='s2' type='number' />
                        <TextField className={styles.param} id='outlined-number' label='s3' type='number' />
                        <TextField className={styles.param} id='outlined-number' label='s4' type='number' />
                    </Box>
                </Box>

            </Box>

            <Box className={styles.rightselections}>


            <Box className={styles.singleparams}>
                    <Box className={styles.item}>
                        <Typography variant='h6'><b>Noise</b></Typography>
                        <TextField className={styles.param} id='outlined-number' type='number' />
                    </Box>

                    <Box className={styles.item}>
                        <Typography variant='h6'><b>Random Noise</b></Typography>
                        <TextField className={styles.param} id='outlined-number' type='number' />
                    </Box>

                    <Box className={styles.item}>
                        <Typography variant='h6'><b>Density</b></Typography>
                        <TextField className={styles.param} id='outlined-number' type='number' />
                    </Box>

                    <Box className={styles.item}>
                        <Typography variant='h6'><b>Num of Steps</b></Typography>
                        <TextField className={styles.param} id='outlined-number' type='number' />
                    </Box>

                </Box>


                <Typography variant='h6' className={styles.break}><b>Plot Selection</b></Typography>
                <Box className={styles.dropdown}>
                    <FormControl sx={{width: 300}}>
                        <InputLabel>Kernel Density Estimation</InputLabel>
                        <Select
                        fullWidth
                        labelId='kernel-label'
                        id='model-multiple-checkbox'
                        value={kernel}
                        multiple
                        renderValue={(selected) => selected.join(', ')}
                        label='Kernel'
                        onChange={handleChangeKer}
                        >
                            {kernelList.map((name) => (
                                <MenuItem key={name} value={name}>
                                    <Checkbox checked={kernel.indexOf(name) > -1} />
                                    <ListItemText primary={name} />
                                </MenuItem>
                            ))}
                        </Select>
                    </FormControl>
                </Box>

                <Box className={styles.dropdown}>
                    <FormControl sx={{width: 300}}>
                        <InputLabel>Line</InputLabel>
                        <Select
                        fullWidth
                        labelId='line-label'
                        id='model-multiple-checkbox'
                        value={line}
                        multiple
                        renderValue={(selected) => selected.join(', ')}
                        label='Line'
                        onChange={handleChangeLin}
                        >
                            {kernelList.map((name) => (
                                <MenuItem key={name} value={name}>
                                    <Checkbox checked={line.indexOf(name) > -1} />
                                    <ListItemText primary={name} />
                                </MenuItem>
                            ))}
                        </Select>
                    </FormControl>
                </Box>

                <Box className={styles.dropdown}>
                    <FormControl sx={{width: 300}}>
                        <InputLabel>Other</InputLabel>
                        <Select
                        fullWidth
                        labelId='other-label'
                        id='model-multiple-checkbox'
                        value={other}
                        multiple
                        renderValue={(selected) => selected.join(', ')}
                        label='Line'
                        onChange={handleChangeOth}
                        >
                            {kernelList.map((name) => (
                                <MenuItem key={name} value={name}>
                                    <Checkbox checked={other.indexOf(name) > -1} />
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
                    onClick={getResults}>
                        Generate
                </Button>
        </Box>

        </Box>
    );
}

//export default Home;
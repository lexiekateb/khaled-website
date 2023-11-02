import React from 'react';
import { useState, useEffect } from 'react';
import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';
import styles from './index.module.css';
import { Checkbox, ListItemText, Typography } from '@mui/material';
import Button from '@mui/material/Button';
import { useNavigate } from 'react-router-dom';

import { Route } from 'react-router-dom';


const Home = () => {

    let navigate = useNavigate();
    const getResults = () => {
        let path = '/results';
        navigate(path);
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
    
    const [sum, setSum] = useState(0);

    const APIcall = () => {
        fetch('http://localhost:5000/', {
            method: 'POST',
            body: JSON.stringify(params)
            }).then((res) =>
        res.json().then((data) => {
            console.log(data);
        }));  

        return true;
    }

    const getSum1 = () => {
        setParams({
            'p1': document.getElementById('p1').value,
            'p2': document.getElementById('p2').value,
            'p3': document.getElementById('p3').value,
            'p4': document.getElementById('p4').value,
            'plots': document.getElementById('plots').value,
            'props': document.getElementById('props').value,
            'k': document.getElementById('k').value,
        });

        APIcall();
        getResults();
    }

    return (
        <Box className={styles.homepage}>

            <Typography variant='h4' className={styles.title} >Sparse Model Generator</Typography>
        
        <Box className={styles.homecontainer} >

            {/* 
            parser.add_argument('--p', metavar='P', nargs=4, type=float_range, required=True, help='Initiator probability matrix')
    parser.add_argument('--plots', metavar='F', nargs='+', help='type of plot (kde, hist-line, hist, kde_hist, graph, spy)', choices=supported_plots, default=[])
    parser.add_argument('--props', metavar='Pr', nargs='+', choices=disp_name.keys(), help='Graph properties to calculate and plot', default=[])
    parser.add_argument('--k', type=int, required=True, help='Kronecker Power')
    parser.add_argument('--outdir', type=str, default='./plotRepo', help='Output directory for the plots')
*/}

                <Box className={styles.inputparams}>
                    <Typography variant='h6' className={styles.break}><b>Input Parameters</b></Typography>
                    <Box className={styles.paramContainer}>
                        <TextField className={styles.param} id='p1' label='p1' type='number' />
                        <TextField className={styles.param} id='p2' label='p2' type='number' />
                        <TextField className={styles.param} id='p3' label='p3' type='number' />
                        <TextField className={styles.param} id='p4' label='p4' type='number' />
                        <TextField className={styles.param} id='plots' label='plots' type='text' />
                        <TextField className={styles.param} id='props' label='props' type='text' />
                        <TextField className={styles.param} id='k' label='k' type='number' />
                    <Button variant='contained' onClick={() => getSum1}>Sum</Button>
                    </Box>
                </Box>

        </Box>

        <Box className={styles.generatebutton}>
                <Button 
                    sx = {{height:100, width: 300, fontSize: 20, borderRadius:12}}
                    size='large' 
                    variant='contained' 
                    onClick={getSum1}>
                        Generate
                </Button>
        </Box>

        </Box>
    );
}

export default Home;
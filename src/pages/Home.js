import React from "react";
import { useState, useEffect } from "react";
import TextField from '@mui/material/TextField';
import './Home.css';
import { Typography } from "@mui/material";
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import Button from '@mui/material/Button';


const Home = () => {

    const [params, setParams] = useState({
        'p0': 0,
        'p1':0,
        'p2':0,
        'p3':0,
        'p4':0,
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
            setSum(data.sum);
        }));  
    }

    const getSum1 = () => {
        setParams({
            'p0': document.getElementById('p0').value,
            'p1': document.getElementById('p1').value,
            'p2': document.getElementById('p2').value,
            'p3': document.getElementById('p3').value,
            'p4': document.getElementById('p4').value,
        });
    }
    

    const[model, setModel] = useState('');

    const handleChange = (event) => {
        setModel(event.target.value);
    }

    return (
        <div className="home-page">

            <Typography variant="h4" className="title">Sparse Model Generator</Typography>
            {sum !== 0 && <Typography variant="h6">{sum}</Typography>}
        
        <div className="home-container">
            <div className="left-selections">

                <div className="model-selector">
                <Typography variant="h6" className="break"><b>Model</b></Typography>
                    <FormControl sx={{width: 300}}>
                        <InputLabel>Model</InputLabel>
                        <Select
                        labelId="model-label"
                        id="model-simple-select"
                        value={model}
                        label="Model"
                        onChange={handleChange}
                        >
                        <MenuItem value={'Kron'}>Kronecker</MenuItem>
                        <MenuItem value={'Model1'}>Model 1</MenuItem>
                        <MenuItem value={'Model2'}>Model 2</MenuItem>
                        </Select>
                    </FormControl>
                </div>

                <div className="input-params">
                    <Typography variant="h6" className="break"><b>Input Parameters</b></Typography>
                    <div className="paramContainer">
                        <TextField className="param" id="p0" label="p0" type="number" />
                        <TextField className="param" id="p1" label="p1" type="number" />
                        <TextField className="param" id="p2" label="p2" type="number" />
                        <TextField className="param" id="p3" label="p3" type="number" />
                        <TextField className="param" id="p4" label="p4" type="number" />
                    <Button variant="contained" onClick={getSum1}>Sum</Button>
                    </div>
                </div>
                
                <div className="input-params">
                    <Typography variant="h6" className="break"><b>Step</b></Typography>
                    <div className="paramContainer">
                        <TextField className="param" id="outlined-number" label="s0" type="number" />
                        <TextField className="param" id="outlined-number" label="s1" type="number" />
                        <TextField className="param" id="outlined-number" label="s2" type="number" />
                        <TextField className="param" id="outlined-number" label="s3" type="number" />
                        <TextField className="param" id="outlined-number" label="s4" type="number" />
                    </div>
                </div>

                <div className="single-params">
                    <div className="item">
                        <Typography variant="h6"><b>Noise</b></Typography>
                        <TextField className="param" id="outlined-number" type="number" />
                    </div>

                    <div className="item">
                        <Typography variant="h6"><b>Random Noise</b></Typography>
                        <TextField className="param" id="outlined-number" type="number" />
                    </div>

                    <div className="item">
                        <Typography variant="h6"><b>Density</b></Typography>
                        <TextField className="param" id="outlined-number" type="number" />
                    </div>

                    <div className="item">
                        <Typography variant="h6"><b>Num of Steps</b></Typography>
                        <TextField className="param" id="outlined-number" type="number" />
                    </div>

                </div>

            </div>

            <div className="right-selections">
                <div className="kernel-dropdown">

                </div>

                <div className="line-dropdown">

                </div>

                <div className="other-dropdown">

                </div>
            </div>

            <div className='generate-button'>

            </div>
        </div>
        </div>
    );
}

export default Home;
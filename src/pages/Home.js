import React from "react";
import { useState } from "react";
import TextField from '@mui/material/TextField';
import './Home.css';
import { Typography } from "@mui/material";
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';

function Home() {

    const[model, setModel] = useState('');

    const handleChange = (event) => {
        setModel(event.target.value);
    }

    return (
        <div className="home-page">

            <Typography variant="h4" className="title">Sparse Model Generator</Typography>
        
        <div className="home-container">
            <div className="left-selections">

                <div className="model-selector">
                <Typography variant="h6" className="break">Model</Typography>
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
                    <Typography variant="h6" className="break">Input Parameters</Typography>
                    <TextField className="param" size="small" id="outlined-number" label="p0" type="number" />
                    <TextField className="param" size="small" id="outlined-number" label="p1" type="number" />
                    <TextField className="param" size="small" id="outlined-number" label="p2" type="number" />
                    <TextField className="param" id="outlined-number" label="p3" type="number" />
                    <TextField className="param" id="outlined-number" label="p4" type="number" />
                </div>
                
                <div className="input-params">
                    <Typography variant="h6" className="break">Step</Typography>
                    <TextField className="param" id="outlined-number" label="s0" type="number" />
                    <TextField className="param" id="outlined-number" label="s1" type="number" />
                    <TextField className="param" id="outlined-number" label="s2" type="number" />
                    <TextField className="param" id="outlined-number" label="s3" type="number" />
                    <TextField className="param" id="outlined-number" label="s4" type="number" />
                </div>

                <div className="single-params">
                    <div className="item">
                        <Typography variant="h6">Noise</Typography>
                        <TextField className="param" id="outlined-number" type="number" />
                    </div>

                    <div className="item">
                        <Typography variant="h6">Random Noise</Typography>
                        <TextField className="param" id="outlined-number" type="number" />
                    </div>

                    <div className="item">
                        <Typography variant="h6">Density</Typography>
                        <TextField className="param" id="outlined-number" type="number" />
                    </div>

                    <div className="item">
                        <Typography variant="h6">Num of Steps</Typography>
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
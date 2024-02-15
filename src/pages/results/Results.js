import styles from "./index.module.css";
import Box from "@mui/material/Box";
import { ImageList, ImageListItem } from "@mui/material";
import { Typography, CircularProgress } from "@mui/material";
import { useEffect, useState} from "react";
import { useLocation } from "react-router-dom";

const Results = () => {
    const [imageList, setImageList] = useState([]);
    const [loading, setLoading] = useState(true); 
    const state = useLocation();
    const params = state.state?.params || {};

    console.log('Entered Results')

    useEffect(() => {
        const images = require.context('/home/lexiekateb/Documents/khaled-website/backend/GraphRobustness/plotRepo', true, /\.(png|jpe?g|svg)$/);
        const imageKeys = images.keys();
        const loadedImages = imageKeys.map(image => images(image));
        // Check if all images are loaded
        Promise.all(loadedImages).then(() => {
            setImageList(loadedImages);
            setLoading(false); // set loading state to false when all images are loaded
        });
    }, []);

    return (
        <Box className={styles.container}>
            <Typography variant="h3" align="center" gutterBottom>
                Results
            </Typography>
            <Box className={styles.paramsContainer}>
                <Typography variant="h6" gutterBottom>
                    Parameters:
                </Typography>
                <Typography variant="body1" display="inline">
                    
                    {Object.entries(params).map(([key, value], index, arr) => (
                        <span key={key}>
                            {`${key}: ${value}${index !== arr.length - 1 ? ', ' : ''}`}
                        </span>
                    ))}
                    
                </Typography>
            </Box>
            {loading ? ( 
                <Box sx={{ display: 'flex', justifyContent: 'center', marginTop: 16 }}>
                    <CircularProgress />
                </Box>
            ) : ( 
                <ImageList className={styles.images} cols={3} gap={16}>
                    {imageList.map((image, i) => (
                        <ImageListItem key={i} sx={{padding: '8px'}}>
                            <img
                                srcSet={image}
                                src={image}
                                alt="results"
                                loading="eager"
                                style={{width: '100%', height: '100%', objectFit: 'cover'}}
                            />
                        </ImageListItem>
                    ))}
                </ImageList>
            )}
        </Box>
    )
}

export default Results;

import styles from "./index.module.css";
import Box from "@mui/material/Box";
import { CircularProgress, ImageList, ImageListItem } from "@mui/material";
import { useEffect, useState} from "react";
import { useLocation } from "react-router-dom";

const Results = () => {

    const [imageList, setImageList] = useState([]);
    const [loading, setLoading] = useState(true);
    const state = useLocation();
    let path = state.state?.imgpath || "";
    console.log(path)

    useEffect(() => {
        const images = require.context('/home/lexiekateb/Documents/GraphRobustness/plotRepo', true, /\.(png|jpe?g|svg)$/);
        setImageList(images.keys().map(image => images(image)));
    }, []);

    return (
        <Box className={styles.container}>
            <ImageList className={styles.images} cols={3} rowHeight={270}>
                {imageList.map((image, i) => (
                    <ImageListItem key={i}>
                        <img
                            srcSet={image}
                            src={image}
                            alt="results"
                            loading="eager"
                        />
                    </ImageListItem>
                ))}
            </ImageList>
        </Box>
    )
}

export default Results;
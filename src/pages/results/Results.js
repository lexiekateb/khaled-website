import styles from "./index.module.css";
import Box from "@mui/material/Box";
import { ImageList, ImageListItem } from "@mui/material";
import { useEffect, useState} from "react";
import { useLocation } from "react-router-dom";

const Results = () => {

    const [imageList, setImageList] = useState([]);
    const state = useLocation();
    let path = state.state?.imgpath || "";
    console.log(path)

    useEffect(() => {
        const images = require.context('/home/lexie/Documents/code/GraphRobustness/plotRepo', true, /\.(png|jpe?g|svg)$/);
        setImageList(images.keys().map(image => images(image)));
    }, []);

    return (
        <Box className={styles.container}>
            <ImageList className={styles.images}cols={3} rowHeight={300}>
                {imageList.map((image, i) => (
                    <ImageListItem key={i}>
                        <img
                            srcSet={image}
                            src={image}
                            alt="results"
                            loading="lazy"
                        />
                    </ImageListItem>
                ))}
            </ImageList>
        </Box>
    )
}

export default Results;
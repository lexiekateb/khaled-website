import styles from "./index.module.css";
import Box from "@mui/material/Box";
import { CircularProgress, ImageList, ImageListItem } from "@mui/material";

const Results = () => {

    const images = require.context('/home/lexie/Documents/code/GraphRobustness', true, /\.(png|jpe?g|svg)$/);
    const imageList = images.keys().map(image => images(image));
    console.log(imageList[0]);

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

export default Results
import React, { useEffect, useState } from "react";
import styles from "./index.module.css";
import Box from "@mui/material/Box";
import { Typography, CircularProgress, Tab, Tabs } from "@mui/material";
import { useLocation } from "react-router-dom";

const Results = () => {
  const [imageList, setImageList] = useState([]);
  const [noiseList, setNoiseList] = useState([]);
  const [loading, setLoading] = useState(true);
  const [tabValue, setTabValue] = useState(0); // State for current tab value
  const state = useLocation();
  const params = state.state?.params || {};

  console.log('Entered Results');

  useEffect(() => {
    const images = require.context(
      '/home/lexiekateb/Documents/khaled-website/backend/GraphRobustness/plotRepo',
      false,
      /\.(png|jpe?g|svg)$/
    );
    const noise = require.context(
      '/home/lexiekateb/Documents/khaled-website/backend/GraphRobustness/plotRepo/noise',
      false,
      /\.(png|jpe?g|svg)$/
    )
    const imageKeys = images.keys();
    const noiseKeys = noise.keys();
    const loadedImages = imageKeys.map((image) => images(image));
    const noiseImages = noiseKeys.map((image) => noise(image));

    Promise.all(loadedImages, noiseImages).then(() => {
      setImageList(loadedImages);
      setNoiseList(noiseImages);
      setLoading(false); // set loading state to false when all images are loaded
    });
  }, []);

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

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
              {`${key}: ${value}${index !== arr.length - 1 ? ", " : ""}`}
            </span>
          ))}
        </Typography>
      </Box>
      <Tabs
        value={tabValue}
        onChange={handleTabChange}
        variant="fullWidth"
        indicatorColor="primary"
        textColor="primary"
        aria-label="tabs"
      >
        <Tab label="Results" />
        <Tab label="Noise" />
      </Tabs>
      {loading ? (
        <Box sx={{ display: "flex", justifyContent: "center", marginTop: 16 }}>
          <CircularProgress />
        </Box>
      ) : (
        <div className={styles.containImages}>
          {tabValue === 0 && (
            <div className={styles.imagesContainer}>
              {imageList.map((image, i) => (
                <div key={i} className={styles.imageItem}>
                  <img
                    src={image}
                    alt="results"
                    loading="eager"
                    className={styles.image}
                  />
                </div>
              ))}
            </div>
          )}
          {tabValue === 1 && <div className={styles.imagesContainer}>
            {noiseList.map((image, i) => (
                <div key={i} className={styles.imageItem}>
                  <img
                    src={image}
                    alt="results"
                    loading="eager"
                    className={styles.image}
                  />
                </div>
              ))}</div>}
        </div>
      )}
    </Box>
  );
};

export default Results;

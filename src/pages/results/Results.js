import React, { useEffect, useState } from "react";
import styles from "./index.module.css";
import Box from "@mui/material/Box";
import { Typography, CircularProgress, Tab, Tabs } from "@mui/material";

const Results = () => {
  const [imageList, setImageList] = useState([]);
  const [noiseList, setNoiseList] = useState([]);
  const [loading, setLoading] = useState(true);
  const [tabValue, setTabValue] = useState(0); // State for current tab value

  useEffect(() => {
    // Paths matching the server.py paths
    const imagesPath = '/plotRepo';
    const noisePath = '/plotRepo/noise';

    // Function to get image files from a directory
    const getImageFiles = async (path) => {
      try {
        const response = await fetch(path);
        if (!response.ok) {
          throw new Error('Failed to fetch images');
        }
        const files = await response.json();
        return files;
      } catch (error) {
        console.error('Error fetching images:', error);
        return [];
      }
    };

    // Fetch images and noise images
    Promise.all([getImageFiles(imagesPath), getImageFiles(noisePath)])
      .then(([images, noiseImages]) => {
        setImageList(images);
        setNoiseList(noiseImages);
        setLoading(false);
      })
      .catch(() => {
        setLoading(false);
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
          {tabValue === 1 && (
            <div className={styles.imagesContainer}>
              {noiseList.map((image, i) => (
                <div key={i} className={styles.imageItem}>
                  <img
                    src={image}
                    alt="noise"
                    loading="eager"
                    className={styles.image}
                  />
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </Box>
  );
};

export default Results;

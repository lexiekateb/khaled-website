import React, { useEffect, useState } from "react";
import { useNavigate } from 'react-router-dom';
import styles from "./index.module.css";
import Box from "@mui/material/Box";
import { Typography, CircularProgress, Tab, Tabs, Dialog, DialogContent, Button } from "@mui/material";
import JSZip from 'jszip';
import { saveAs } from 'file-saver';

const Results = () => {
  const navigate = useNavigate();
  const [imageList, setImageList] = useState([]);
  const [noiseList, setNoiseList] = useState([]);
  const [loading, setLoading] = useState(true);
  const [tabValue, setTabValue] = useState(0); // State for current tab value
  const [selectedImage, setSelectedImage] = useState(null); // State for selected image

  useEffect(() => {
    const images = require.context(
      '../../../backend/GraphRobustness/plotRepo', // Updated path to backend folder
      true,
      /\.(png|jpe?g|svg)$/
    );
    const imageKeys = images.keys();
    const loadedImages = imageKeys.map((image) => images(image));
    // Check if all images are loaded
    Promise.all(loadedImages).then(() => {
      const imagesWithNoise = loadedImages.filter((image) => image.includes("noise"));
      const imagesWithoutNoise = loadedImages.filter((image) => !image.includes("noise"));
      setImageList(imagesWithoutNoise);
      setNoiseList(imagesWithNoise);
      setLoading(false); // set loading state to false when all images are loaded
    });
  }, []);

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  const handleImageClick = (image) => {
    setSelectedImage(image);
  };

  const handleCloseDialog = () => {
    setSelectedImage(null);
  };

  const handleSubmit = async () => {
    navigate('/');
  };

  const handleDownloadImages = () => {
    const zip = new JSZip();
    const folderName = tabValue === 0 ? 'results' : 'noise';
    const imageListToDownload = tabValue === 0 ? imageList : noiseList;

    imageListToDownload.forEach((image, index) => {
      fetch(image, { mode: 'cors' }) // Fetch the image
        .then((response) => response.blob())
        .then((blob) => {
          zip.file(`${folderName}/image_${index + 1}.png`, blob); // Add the image to the zip file
          if (index === imageListToDownload.length - 1) {
            // If it's the last image, generate and save the zip file
            zip.generateAsync({ type: 'blob' }).then((content) => {
              saveAs(content, `${folderName}_images.zip`); // Save the zip file
            });
          }
        });
    });
  };

  return (
    <Box className={styles.container} sx={{ height: "100vh", display: "flex", flexDirection: "column" }}>
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
        <div className={styles.containImages} style={{ flex: 1 }}>
          {tabValue === 0 && (
            <div className={styles.imagesContainer}>
              {imageList.map((image, i) => (
                <div key={i} className={styles.imageItem} onClick={() => handleImageClick(image)}>
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
                <div key={i} className={styles.imageItem} onClick={() => handleImageClick(image)}>
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
      <Dialog open={selectedImage !== null} onClose={handleCloseDialog} maxWidth="xl" fullWidth>
        <DialogContent>
          <img src={selectedImage} alt="selected" className={styles.selectedImage} style={{ width: "100%", height: "auto" }} />
        </DialogContent>
      </Dialog>
      <Box sx={{ display: 'flex', justifyContent: 'center', marginTop: 2 }}>
        <Button variant="outlined" onClick={handleDownloadImages}>Download All Images as ZIP</Button>
      </Box>
      <Button onClick={handleSubmit}>Go back to Home</Button>
    </Box>
  );
};

export default Results;

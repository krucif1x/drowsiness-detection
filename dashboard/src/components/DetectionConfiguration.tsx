import React, { useEffect, useState } from "react";
import {
  Box,
  Typography,
  Slider,
  Paper,
  Tabs,
  Tab,
  Switch,
  FormControlLabel,
  Button,
  TextField,
} from "@mui/material";
import axios from "axios";
import { API_URL_LOCATION } from "../constant/urlConstant";

interface DrowsinessConfig {
  eye_aspect_ratio_threshold: number;
  eye_aspect_ratio_consec_frames: number;
  mouth_aspect_ratio_threshold: number;
  mouth_aspect_ratio_consec_frames: number;
  apply_masking: boolean;
}

interface PhoneDetectionConfig {
  distance_threshold: number;
}

interface DetectionConfig {
  drowsiness: DrowsinessConfig;
  phone_detection: PhoneDetectionConfig;
}

const DetectionConfiguration: React.FC = () => {
  const [tabIndex, setTabIndex] = useState(0);

  const [drowsiness, setDrowsiness] = useState<DrowsinessConfig>({
    eye_aspect_ratio_threshold: 0.25,
    eye_aspect_ratio_consec_frames: 48,
    mouth_aspect_ratio_threshold: 1.5,
    mouth_aspect_ratio_consec_frames: 21,
    apply_masking: true,
  });

  const [phoneDetection, setPhoneDetection] = useState<PhoneDetectionConfig>({
    distance_threshold: 150,
  });

  useEffect(() => {
    const fetchConfig = async () => {
      try {
        const response = await axios.get(`${API_URL_LOCATION}/config/detection`);
        const config: DetectionConfig = response.data;
        setDrowsiness(config.drowsiness);
        setPhoneDetection(config.phone_detection);
      } catch (error) {
        console.error("Failed to load config", error);
      }
    };

    fetchConfig();
  }, []);

  const handleSubmit = async () => {
    const payload: DetectionConfig = {
      drowsiness,
      phone_detection: phoneDetection,
    };

    try {
      const response = await axios.post(
        `${API_URL_LOCATION}/config/detection`, 
      payload);
      console.log("Saved config:", response.data);
    } catch (err) {
      console.error("Error saving config", err);
    }
  };

  return (
    <Paper variant="outlined" sx={{ p: 3, mb: 2 }}>
      <Typography variant="h2" gutterBottom>
        Detection Configuration
      </Typography>

      <Tabs value={tabIndex} onChange={(_, val) => setTabIndex(val)} sx={{ mb: 2 }}>
        <Tab label="Drowsiness Detection" />
        <Tab label="Phone Detection" />
      </Tabs>

      {tabIndex === 0 && (
        <>
          <ConfigSlider
            label="Eye Aspect Ratio(EAR) Threshold"
            value={drowsiness.eye_aspect_ratio_threshold}
            min={0.1}
            max={0.5}
            step={0.01}
            onChange={(val) =>
              setDrowsiness({ ...drowsiness, eye_aspect_ratio_threshold: val })
            }
          />
          <ConfigSlider
            label="EAR Consecutive Frames"
            value={drowsiness.eye_aspect_ratio_consec_frames}
            min={5}
            max={100}
            step={1}
            onChange={(val) =>
              setDrowsiness({ ...drowsiness, eye_aspect_ratio_consec_frames: val })
            }
          />
          <ConfigSlider
            label="Mouth Aspect Ratio (MAR) Threshold"
            value={drowsiness.mouth_aspect_ratio_threshold}
            min={0.5}
            max={2.5}
            step={0.05}
            onChange={(val) =>
              setDrowsiness({ ...drowsiness, mouth_aspect_ratio_threshold: val })
            }
          />
          <ConfigSlider
            label="MAR Consecutive Frames"
            value={drowsiness.mouth_aspect_ratio_consec_frames}
            min={5}
            max={50}
            step={1}
            onChange={(val) =>
              setDrowsiness({ ...drowsiness, mouth_aspect_ratio_consec_frames: val })
            }
          />
          <FormControlLabel
            control={
              <Switch
                checked={drowsiness.apply_masking}
                onChange={(e) =>
                  setDrowsiness({ ...drowsiness, apply_masking: e.target.checked })
                }
              />
            }
            label="Apply Masking"
          />
        </>
      )}

      {tabIndex === 1 && (
        <Box sx={{ mt: 2 }}>
          <Typography sx={styles.label}>
            Phone Detection Distance Threshold:{" "}
            <strong>{phoneDetection.distance_threshold}</strong>
          </Typography>
          <TextField
            fullWidth
            type="number"
            value={phoneDetection.distance_threshold}
            onChange={(e) =>
              setPhoneDetection({
                ...phoneDetection,
                distance_threshold: parseInt(e.target.value),
              })
            }
          />
        </Box>
      )}

      <Box sx={{ mt: 3 }}>
        <Button variant="contained" color="primary" onClick={handleSubmit}>
          Save Configuration
        </Button>
      </Box>
    </Paper>
  );
};

const ConfigSlider = ({
  label,
  value,
  onChange,
  min,
  max,
  step,
}: {
  label: string;
  value: number;
  onChange: (val: number) => void;
  min: number;
  max: number;
  step: number;
}) => (
  <Box sx={{ my: 2 }}>
    <Typography sx={styles.label}>
      {label}: <strong>{value}</strong>
    </Typography>
    <Slider
      value={value}
      onChange={(_, newVal) => onChange(newVal as number)}
      min={min}
      max={max}
      step={step}
    />
  </Box>
);

/** @type {import('@mui/material').SxProps} */
const styles = {
  label: {
    fontWeight: 500,
    mb: 1,
    fontSize: "0.9rem",
  },
};

export default DetectionConfiguration;

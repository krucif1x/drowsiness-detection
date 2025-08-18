import React, { useEffect, useState } from "react";
import {
  Typography,
  FormControl,
  Select,
  MenuItem,
  Paper,
  Switch,
  FormControlLabel,
  Box,
  Button,
  Tabs,
  Tab,
  Alert,
  Tooltip,
  Snackbar,
  Alert as MuiAlert,
} from "@mui/material";
import axios from "axios";
import { API_URL_LOCATION } from "../constant/urlConstant";
import { InfoOutlined } from "@mui/icons-material";

interface PipelineSettings {
  drowsiness_model_run: boolean;
  phone_detection_model_run: boolean;
  hands_detection_model_run: boolean;
  inference_engine: string;
}

const PipelineConfiguration: React.FC = () => {
  const [tabIndex, setTabIndex] = useState(0);
  const [pipeline, setPipeline] = useState<PipelineSettings>({
    drowsiness_model_run: true,
    phone_detection_model_run: false,
    hands_detection_model_run: false,
    inference_engine: "cpu",
  });

  const [initialInferenceEngine, setInitialInferenceEngine] = useState<string>("");
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarStatus, setSnackbarStatus] = useState<"success" | "error">("success");

  useEffect(() => {
    const fetchConfig = async () => {
      try {
        const res = await axios.get(`${API_URL_LOCATION}/config/pipeline`);
        setPipeline(res.data);
        setInitialInferenceEngine(res.data.inference_engine);
      } catch (err) {
        console.error("Failed to fetch pipeline config:", err);
      }
    };
    fetchConfig();
  }, []);

  const handleSubmit = async () => {
    try {
      const payload = pipeline;
      await axios.post(`${API_URL_LOCATION}/config/pipeline/update`, payload);
      setSnackbarStatus("success");
      setSnackbarOpen(true);
    } catch (err) {
      console.error("Failed to save pipeline config:", err);
      setSnackbarStatus("error");
      setSnackbarOpen(true);
    }
  };

  const hasEngineChanged = pipeline.inference_engine !== initialInferenceEngine;

  return (
    <Paper variant="outlined" sx={{ p: 3, mb: 2 }}>
      <Typography variant="h2" gutterBottom>
        Model Configuration
      </Typography>

      <Tabs value={tabIndex} onChange={(_, val) => setTabIndex(val)} sx={{ mb: 2 }}>
        <Tab label="Pipeline Settings" />
      </Tabs>

      {tabIndex === 0 && (
        <Box>
          <FormControlLabel
            control={
              <Switch
                checked={pipeline.drowsiness_model_run}
                onChange={(e) =>
                  setPipeline({
                    ...pipeline,
                    drowsiness_model_run: e.target.checked,
                  })
                }
              />
            }
            label="Run Drowsiness Detection"
          />

          <FormControlLabel
            control={
              <Switch
                checked={pipeline.phone_detection_model_run}
                onChange={(e) =>
                  setPipeline({
                    ...pipeline,
                    phone_detection_model_run: e.target.checked,
                  })
                }
              />
            }
            label="Run Phone Detection"
          />

          <FormControlLabel
            control={
              <Switch
                checked={pipeline.hands_detection_model_run}
                onChange={(e) =>
                  setPipeline({
                    ...pipeline,
                    hands_detection_model_run: e.target.checked,
                  })
                }
              />
            }
            label="Run Hands Detection"
          />

          <FormControl fullWidth margin="normal">
            <Box sx={{ display: "flex", alignItems: "center"}}>
              <Typography variant="body2" sx={{ fontWeight: 500 }}>
                Inference Engine
              </Typography>
              <Tooltip title="Changing this requires application restart">
                <InfoOutlined fontSize="small" sx={{ color: "text.secondary" }} />
              </Tooltip>
            </Box>
            <Select
              value={pipeline.inference_engine}
              onChange={(e) =>
                setPipeline({
                  ...pipeline,
                  inference_engine: e.target.value,
                })
              }
            >
              <MenuItem value="cpu">CPU</MenuItem>
              <MenuItem value="auto">Auto</MenuItem>
            </Select>
          </FormControl>

          {hasEngineChanged && (
            <Alert severity="warning" sx={{ mt: 2 }}>
              You are going to change Inference engine!. Please <strong>restart the application</strong> for changes to take effect.
            </Alert>
          )}
        </Box>
      )}

      <Box sx={{ mt: 3 }}>
        <Button variant="contained" color="primary" onClick={handleSubmit}>
          Save Configuration
        </Button>
      </Box>

      <Snackbar
        open={snackbarOpen}
        autoHideDuration={4000}
        onClose={() => setSnackbarOpen(false)}
        anchorOrigin={{ vertical: "bottom", horizontal: "center" }}
      >
        <MuiAlert
          onClose={() => setSnackbarOpen(false)}
          severity={snackbarStatus}
          elevation={6}
          variant="filled"
          sx={{ width: "100%" }}
        >
          {snackbarStatus === "success"
            ? "Pipeline configuration saved successfully!"
            : "Failed to save pipeline configuration."}
        </MuiAlert>
      </Snackbar>
    </Paper>
  );
};

export default PipelineConfiguration;
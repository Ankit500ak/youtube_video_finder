import React, { useRef, useState } from 'react';
import { Button, Snackbar, Alert } from '@mui/material';
import MicIcon from '@mui/icons-material/Mic';

function VoiceInput({ onResult }) {
  const recognitionRef = useRef(null);
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'error' });

  const handleSnackbarClose = () => setSnackbar({ ...snackbar, open: false });

  const startRecognition = () => {
    if (!('webkitSpeechRecognition' in window)) {
      setSnackbar({ open: true, message: 'Voice search is only supported in Google Chrome.', severity: 'warning' });
      return;
    }
    try {
      const recognition = new window.webkitSpeechRecognition();
      recognition.lang = 'en-IN'; // Supports English & Hindi
      recognition.interimResults = false;
      recognition.maxAlternatives = 1;
      recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        onResult(transcript);
        setSnackbar({ open: true, message: `Heard: "${transcript}"`, severity: 'success' });
      };
      recognition.onerror = (event) => {
        let msg = 'Speech recognition error.';
        if (event.error === 'not-allowed') msg = 'Microphone permission denied.';
        else if (event.error === 'no-speech') msg = 'No speech detected. Try again.';
        setSnackbar({ open: true, message: msg, severity: 'error' });
      };
      recognitionRef.current = recognition;
      recognition.start();
    } catch (e) {
      setSnackbar({ open: true, message: 'Voice search failed to start.', severity: 'error' });
    }
  };

  return (
    <>
      <Button
        variant="contained"
        color="secondary"
        onClick={startRecognition}
        startIcon={<MicIcon />}
        sx={{ height: 56, fontWeight: 600, borderRadius: 2, boxShadow: '0 2px 8px #f5005720', px: 2 }}
      >
        Voice Search
      </Button>
      <Snackbar
        open={snackbar.open}
        autoHideDuration={3000}
        onClose={handleSnackbarClose}
        anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
      >
        <Alert onClose={handleSnackbarClose} severity={snackbar.severity} sx={{ width: '100%' }}>
          {snackbar.message}
        </Alert>
      </Snackbar>
    </>
  );
}

export default VoiceInput;

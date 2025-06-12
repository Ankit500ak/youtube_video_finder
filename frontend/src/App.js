import React, { useState } from 'react';
import { Container, Typography, Box, Paper, Divider, Fade } from '@mui/material';
import SearchBar from './components/SearchBar';
import VoiceInput from './components/VoiceInput';
import VideoList from './components/VideoList';
import axios from 'axios';

function App() {
  const [videos, setVideos] = useState([]);
  const [bestVideo, setBestVideo] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSearch = async (query) => {
    setLoading(true);
    setError('');
    try {
      const res = await axios.post('http://127.0.0.1:5000/api/search', 
        { query: query.trim() },
        {
          headers: {
            'Content-Type': 'application/json'
          }
        }
      );
      
      if (res.data.error) {
        throw new Error(res.data.error);
      }
      
      if (res.data.status === 'warning') {
        setError(res.data.error);
        alert('Warning: ' + res.data.error);
        return;
      }
      
      setBestVideo(res.data.best_video);
      setVideos(res.data.videos);
    } catch (e) {
      console.error('Search error:', e);
      let errorMessage = e.response?.data?.error || 'Error fetching videos';
      if (e.response?.data?.details) {
        errorMessage += `\nDetails: ${e.response.data.details}`;
      }
      setError(errorMessage);
      alert(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ minHeight: '100vh', background: 'linear-gradient(135deg, #f4f6fa 0%, #e3eafc 100%)', py: 6 }}>
      <Container maxWidth="md">
        <Paper elevation={3} sx={{ p: { xs: 2, sm: 4 }, borderRadius: 4, mb: 4 }}>
          <Typography variant="h4" align="center" color="primary" gutterBottom sx={{ fontWeight: 700, letterSpacing: 1 }}>
            YouTube Video Finder
          </Typography>
          <Typography component="span" color="secondary" sx={{ fontWeight: 700 }}>
            with AI
          </Typography>
          <Typography variant="subtitle1" align="center" color="text.secondary" gutterBottom>
            Search for the best YouTube videos instantly using AI-powered search.
          </Typography>
          {error && (
            <Paper elevation={1} sx={{ p: 2, mb: 2, bgcolor: 'error.light' }}>
              <Typography variant="body1" color="error.main">
                {error}
              </Typography>
            </Paper>
          )}
          <Box display="flex" flexDirection={{ xs: 'column', sm: 'row' }} gap={2} justifyContent="center" alignItems="center" mt={2}>
            <SearchBar onSearch={handleSearch} loading={loading} />
            <VoiceInput onResult={handleSearch} />
          </Box>
        </Paper>
        <Fade in={!!bestVideo || videos.length > 0}>
          <Box>
            {bestVideo && (
              <Box mb={3}>
                <Typography variant="h6" sx={{ fontWeight: 600, mb: 1, color: 'primary.main' }}>
                  Best Video
                </Typography>
                <VideoList videos={[bestVideo]} highlight />
              </Box>
            )}
            <Divider sx={{ my: 3 }} />
            <Typography variant="h6" sx={{ fontWeight: 600, mb: 2, color: 'primary.main' }}>
              Other Top Results
            </Typography>
            <VideoList videos={videos.filter(v => bestVideo && v.url !== bestVideo.url)} />
          </Box>
        </Fade>
      </Container>
    </Box>
  );
}

export default App;

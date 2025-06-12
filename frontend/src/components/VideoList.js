import React, { useState } from 'react';
import { Card, CardContent, CardMedia, Typography, Grid, Box, Dialog, IconButton } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';

function getYoutubeId(url) {
  // Handles typical YouTube URL formats
  const match = url.match(/(?:v=|\/embed\/|youtu\.be\/|\/v\/|\/shorts\/)([\w-]{11})/);
  return match ? match[1] : null;
}

function VideoList({ videos, highlight }) {
  const [open, setOpen] = useState(false);
  const [currentId, setCurrentId] = useState(null);
  const [currentTitle, setCurrentTitle] = useState('');

  const handleOpen = (video) => {
    const id = getYoutubeId(video.url);
    if (id) {
      setCurrentId(id);
      setCurrentTitle(video.title);
      setOpen(true);
    } else {
      window.open(video.url, '_blank');
    }
  };
  const handleClose = () => setOpen(false);

  if (!videos || videos.length === 0) return null;
  return (
    <>
      <Grid container spacing={2} mt={1}>
        {videos.map((video, idx) => (
          <Grid item xs={12} md={highlight ? 12 : 6} key={video.url}>
            <Card
              sx={{ display: 'flex', flexDirection: { xs: 'column', sm: 'row' }, border: highlight ? '2px solid #1976d2' : undefined, minHeight: 160, cursor: 'pointer' }}
              onClick={() => handleOpen(video)}
            >
              {video.thumbnail && (
                <CardMedia
                  component="img"
                  sx={{ width: { xs: '100%', sm: 220 }, height: 140, objectFit: 'cover' }}
                  image={video.thumbnail}
                  alt={video.title}
                />
              )}
              <Box sx={{ display: 'flex', flexDirection: 'column', flex: 1 }}>
                <CardContent>
                  <Typography variant="subtitle1" fontWeight={highlight ? 700 : 500} gutterBottom>
                    {video.title}
                  </Typography>
                  {video.channelTitle && (
                    <Typography variant="body2" color="text.secondary" gutterBottom>
                      Channel: {video.channelTitle}
                    </Typography>
                  )}
                  {video.snippet && (
                    <Typography variant="body2" color="text.secondary">
                      {video.snippet}
                    </Typography>
                  )}
                </CardContent>
              </Box>
            </Card>
          </Grid>
        ))}
      </Grid>
      <Dialog open={open} onClose={handleClose} maxWidth="md" fullWidth>
        <Box sx={{ position: 'relative', bgcolor: '#000', p: 0 }}>
          <IconButton onClick={handleClose} sx={{ position: 'absolute', top: 8, right: 8, color: '#fff', zIndex: 2 }}>
            <CloseIcon />
          </IconButton>
          {currentId && (
            <Box sx={{ aspectRatio: '16/9', width: '100%', background: '#000' }}>
              <iframe
                width="100%"
                height="400"
                src={`https://www.youtube.com/embed/${currentId}?autoplay=1`}
                title={currentTitle}
                frameBorder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen
                style={{ display: 'block', width: '100%' }}
              />
            </Box>
          )}
        </Box>
      </Dialog>
    </>
  );
}

export default VideoList;

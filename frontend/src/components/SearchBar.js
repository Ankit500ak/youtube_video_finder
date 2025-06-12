import React, { useState } from 'react';
import { Box, TextField, Button, InputAdornment, Paper } from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';

function SearchBar({ onSearch, loading }) {
  const [query, setQuery] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim()) onSearch(query);
  };

  return (
    <Paper elevation={2} sx={{ borderRadius: 3, boxShadow: '0 2px 8px #1976d220', flex: 1 }}>
      <Box component="form" onSubmit={handleSubmit} display="flex" gap={1} p={1}>
        <TextField
          label="Search YouTube videos"
          value={query}
          onChange={e => setQuery(e.target.value)}
          fullWidth
          disabled={loading}
          size="medium"
          variant="outlined"
          sx={{ background: '#fff', borderRadius: 2 }}
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <SearchIcon color="primary" />
              </InputAdornment>
            ),
          }}
        />
        <Button
          variant="contained"
          color="primary"
          type="submit"
          disabled={loading}
          sx={{ px: 3, borderRadius: 2, fontWeight: 600 }}
        >
          Search
        </Button>
      </Box>
    </Paper>
  );
}

export default SearchBar;

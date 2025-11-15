import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Box, Button, Container, Paper, TextField, Typography } from '@mui/material';

import { useAuth } from '../context/AuthContext';

const LoginPage = () => {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [employeeCode, setEmployeeCode] = useState('1');

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    login(employeeCode);
    navigate('/dashboard');
  };

  return (
    <Container maxWidth="sm" sx={{ mt: 10 }}>
      <Paper sx={{ p: 4 }}>
        <Typography variant="h5" gutterBottom>
          NeedAnalyze Login
        </Typography>
        <Typography variant="body2" color="text.secondary" mb={2}>
          Enter your employee code (numeric for demo) to view your dashboard.
        </Typography>
        <Box component="form" onSubmit={handleSubmit}>
          <TextField
            label="Employee Code"
            value={employeeCode}
            onChange={(event) => setEmployeeCode(event.target.value)}
            fullWidth
            margin="normal"
          />
          <Button type="submit" variant="contained" size="large" fullWidth>
            Login
          </Button>
        </Box>
      </Paper>
    </Container>
  );
};

export default LoginPage;

import { Navigate, Route, Routes } from 'react-router-dom';
import { CssBaseline, ThemeProvider, createTheme } from '@mui/material';

import LoginPage from './pages/LoginPage';
import EmployeeDashboard from './pages/EmployeeDashboard';
import AdminDashboard from './pages/AdminDashboard';
import { useAuth } from './context/AuthContext';

const theme = createTheme({
  palette: {
    primary: { main: '#0072CE' },
    secondary: { main: '#004a99' },
  },
});

const App = () => {
  const { isAuthenticated } = useAuth();

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route
          path="/dashboard"
          element={isAuthenticated ? <EmployeeDashboard /> : <Navigate to="/login" replace />}
        />
        <Route
          path="/admin"
          element={isAuthenticated ? <AdminDashboard /> : <Navigate to="/login" replace />}
        />
        <Route path="*" element={<Navigate to={isAuthenticated ? '/dashboard' : '/login'} replace />} />
      </Routes>
    </ThemeProvider>
  );
};

export default App;

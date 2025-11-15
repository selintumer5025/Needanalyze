import { useEffect, useMemo, useState } from 'react';
import {
  Box,
  Button,
  CircularProgress,
  Container,
  Grid,
  Paper,
  Stack,
  Typography,
} from '@mui/material';

import {
  GapRecommendation,
  PlanItem,
  RecommendationResponse,
  addPlanItem,
  fetchPlan,
  fetchRecommendations,
  updatePlanItem,
} from '../api/employees';
import CompetencyCard from '../components/CompetencyCard';
import DevelopmentJourney from '../components/DevelopmentJourney';
import PlanTable from '../components/PlanTable';
import { useAuth } from '../context/AuthContext';

const EmployeeDashboard = () => {
  const { employeeId, employeeCode, logout } = useAuth();
  const [recommendations, setRecommendations] = useState<RecommendationResponse | null>(null);
  const [plan, setPlan] = useState<PlanItem[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!employeeId) return;
    const load = async () => {
      setLoading(true);
      try {
        const [recResponse, planResponse] = await Promise.all([
          fetchRecommendations(employeeId),
          fetchPlan(employeeId),
        ]);
        setRecommendations(recResponse);
        setPlan(planResponse);
      } catch (error) {
        console.error(error);
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [employeeId]);

  const handleAddToPlan = async (activityId: number) => {
    if (!employeeId) return;
    const created = await addPlanItem(employeeId, { activity_id: activityId });
    setPlan((prev) => [...prev, created]);
  };

  const handleUpdateStatus = async (planId: number, status: string) => {
    if (!employeeId) return;
    const updated = await updatePlanItem(employeeId, planId, { status });
    setPlan((prev) => prev.map((item) => (item.id === planId ? updated : item)));
  };

  const competencyCards = useMemo(() => {
    if (!recommendations) return [] as GapRecommendation[];
    return recommendations.competency_gaps;
  }, [recommendations]);

  if (!employeeId) {
    return (
      <Container sx={{ mt: 6 }}>
        <Typography>Please login again.</Typography>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Stack direction="row" justifyContent="space-between" alignItems="center" mb={3}>
        <div>
          <Typography variant="h4">Welcome back</Typography>
          <Typography variant="body2" color="text.secondary">
            Employee code: {employeeCode}
          </Typography>
        </div>
        <Button variant="outlined" onClick={logout}>
          Logout
        </Button>
      </Stack>
      {loading && (
        <Stack alignItems="center" py={4}>
          <CircularProgress />
        </Stack>
      )}
      {!loading && recommendations && (
        <Stack spacing={4}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6">Profile</Typography>
            <Typography>
              {recommendations.employee_name} · {recommendations.role} · {recommendations.department}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Seniority: {recommendations.seniority_level}
            </Typography>
          </Paper>
          <Box>
            <Typography variant="h6" gutterBottom>
              Competency overview
            </Typography>
            <Grid container spacing={2}>
              {competencyCards.map((gap) => (
                <Grid item xs={12} md={4} key={gap.competency_id}>
                  <CompetencyCard
                    title={gap.competency_name}
                    currentLevel={gap.current_level}
                    targetLevel={gap.target_level}
                  />
                </Grid>
              ))}
            </Grid>
          </Box>
          <Box>
            <Typography variant="h6" gutterBottom>
              My Recommended Development Journey
            </Typography>
            {recommendations.competency_gaps.map((gap) => (
              <DevelopmentJourney key={gap.competency_id} gap={gap} onAddToPlan={handleAddToPlan} />
            ))}
          </Box>
          <PlanTable items={plan} onChangeStatus={handleUpdateStatus} />
        </Stack>
      )}
    </Container>
  );
};

export default EmployeeDashboard;

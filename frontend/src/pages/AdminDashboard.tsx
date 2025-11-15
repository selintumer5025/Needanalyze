import { useEffect, useState } from 'react';
import {
  Box,
  Button,
  Container,
  Tab,
  Tabs,
  TextField,
  Typography,
} from '@mui/material';

import { Activity } from '../api/employees';
import { Competency, createActivity, createCompetency, listActivities, listCompetencies } from '../api/catalog';

const AdminDashboard = () => {
  const [tab, setTab] = useState(0);
  const [competencies, setCompetencies] = useState<Competency[]>([]);
  const [activities, setActivities] = useState<Activity[]>([]);
  const [competencyForm, setCompetencyForm] = useState({ name: '', category: '', description: '' });
  const [activityForm, setActivityForm] = useState({
    code: '',
    name: '',
    type: 'e-learning',
    modality: 'online',
    duration_hours: 2,
    provider: 'Internal',
    description: '',
  });

  useEffect(() => {
    const load = async () => {
      const [competencyData, activityData] = await Promise.all([listCompetencies(), listActivities()]);
      setCompetencies(competencyData);
      setActivities(activityData);
    };
    load();
  }, []);

  const handleCompetencySubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    const created = await createCompetency(competencyForm);
    setCompetencies((prev) => [...prev, created]);
    setCompetencyForm({ name: '', category: '', description: '' });
  };

  const handleActivitySubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    const created = await createActivity(activityForm);
    setActivities((prev) => [...prev, created]);
    setActivityForm({ ...activityForm, code: '', name: '', description: '' });
  };

  return (
    <Container sx={{ py: 4 }}>
      <Typography variant="h4" gutterBottom>
        Admin & L&D Workspace
      </Typography>
      <Tabs value={tab} onChange={(_, value) => setTab(value)} sx={{ mb: 3 }}>
        <Tab label="Competencies" />
        <Tab label="Activities" />
        <Tab label="Analytics" />
      </Tabs>
      {tab === 0 && (
        <Box>
          <Typography variant="h6">Add Competency</Typography>
          <Box component="form" onSubmit={handleCompetencySubmit} sx={{ display: 'grid', gap: 2, maxWidth: 400, my: 2 }}>
            <TextField label="Name" value={competencyForm.name} onChange={(e) => setCompetencyForm({ ...competencyForm, name: e.target.value })} />
            <TextField label="Category" value={competencyForm.category} onChange={(e) => setCompetencyForm({ ...competencyForm, category: e.target.value })} />
            <TextField label="Description" value={competencyForm.description} onChange={(e) => setCompetencyForm({ ...competencyForm, description: e.target.value })} />
            <Button type="submit" variant="contained">
              Save
            </Button>
          </Box>
          <Typography variant="subtitle1">Existing competencies ({competencies.length})</Typography>
          <ul>
            {competencies.map((competency) => (
              <li key={competency.id}>
                {competency.name} · {competency.category}
              </li>
            ))}
          </ul>
        </Box>
      )}
      {tab === 1 && (
        <Box>
          <Typography variant="h6">Add Development Activity</Typography>
          <Box component="form" onSubmit={handleActivitySubmit} sx={{ display: 'grid', gap: 2, maxWidth: 400, my: 2 }}>
            <TextField label="Code" value={activityForm.code} onChange={(e) => setActivityForm({ ...activityForm, code: e.target.value })} />
            <TextField label="Name" value={activityForm.name} onChange={(e) => setActivityForm({ ...activityForm, name: e.target.value })} />
            <TextField label="Type" value={activityForm.type} onChange={(e) => setActivityForm({ ...activityForm, type: e.target.value })} />
            <TextField label="Modality" value={activityForm.modality} onChange={(e) => setActivityForm({ ...activityForm, modality: e.target.value })} />
            <TextField
              label="Duration hours"
              type="number"
              value={activityForm.duration_hours}
              onChange={(e) => setActivityForm({ ...activityForm, duration_hours: Number(e.target.value) })}
            />
            <TextField label="Provider" value={activityForm.provider} onChange={(e) => setActivityForm({ ...activityForm, provider: e.target.value })} />
            <TextField label="Description" value={activityForm.description} onChange={(e) => setActivityForm({ ...activityForm, description: e.target.value })} />
            <Button type="submit" variant="contained">
              Save
            </Button>
          </Box>
          <Typography variant="subtitle1">Activities catalog ({activities.length})</Typography>
          <ul>
            {activities.map((activity) => (
              <li key={activity.id}>
                {activity.name} · {activity.type} · {activity.modality}
              </li>
            ))}
          </ul>
        </Box>
      )}
      {tab === 2 && (
        <Box>
          <Typography variant="h6">Analytics</Typography>
          <Typography variant="body2" color="text.secondary">
            Placeholder for analytics cards (e.g., competency gap counts, activity completion rates).
          </Typography>
        </Box>
      )}
    </Container>
  );
};

export default AdminDashboard;

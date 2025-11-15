import { Card, CardContent, Chip, Divider, Stack, Typography } from '@mui/material';

import { GapRecommendation } from '../api/employees';

interface Props {
  gap: GapRecommendation;
  onAddToPlan: (activityId: number) => void;
}

const DevelopmentJourney: React.FC<Props> = ({ gap, onAddToPlan }) => (
  <Card sx={{ mb: 2 }}>
    <CardContent>
      <Stack direction="row" justifyContent="space-between" alignItems="center">
        <div>
          <Typography variant="h6">{gap.competency_name}</Typography>
          <Typography variant="body2" color="text.secondary">
            Target level: {gap.target_level} | Current: {gap.current_level || 'N/A'}
          </Typography>
        </div>
        <Chip color="error" label={`Gap ${gap.gap_level_difference} levels`} />
      </Stack>
      <Divider sx={{ my: 2 }} />
      <Stack spacing={2}>
        {gap.journey.map((step) => (
          <Card key={step.title} variant="outlined">
            <CardContent>
              <Typography variant="subtitle1">{step.title}</Typography>
              <Typography variant="body2" color="text.secondary" mb={1}>
                {step.description}
              </Typography>
              <Stack spacing={1}>
                {step.activities.map((activity) => (
                  <Stack key={activity.id} direction="row" spacing={2} alignItems="center">
                    <div>
                      <Typography variant="body2">{activity.name}</Typography>
                      <Typography variant="caption" color="text.secondary">
                        {activity.type} · {activity.modality} · {activity.duration_hours}h
                      </Typography>
                    </div>
                    <Chip label="Add to plan" onClick={() => onAddToPlan(activity.id)} />
                  </Stack>
                ))}
                {step.activities.length === 0 && (
                  <Typography variant="caption" color="text.secondary">
                    No mapped activities yet.
                  </Typography>
                )}
              </Stack>
            </CardContent>
          </Card>
        ))}
      </Stack>
    </CardContent>
  </Card>
);

export default DevelopmentJourney;

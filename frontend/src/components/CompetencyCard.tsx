import { Card, CardContent, Stack, Typography } from '@mui/material';

interface Props {
  title: string;
  currentLevel?: string;
  targetLevel: string;
}

const CompetencyCard: React.FC<Props> = ({ title, currentLevel, targetLevel }) => {
  const isGap = !currentLevel || currentLevel.toLowerCase() !== targetLevel.toLowerCase();
  return (
    <Card variant="outlined" sx={{ borderColor: isGap ? 'error.main' : 'success.light' }}>
      <CardContent>
        <Typography variant="h6">{title}</Typography>
        <Stack direction="row" spacing={2} mt={1}>
          <Typography variant="body2">Current: {currentLevel || 'N/A'}</Typography>
          <Typography variant="body2">Target: {targetLevel}</Typography>
        </Stack>
        <Typography variant="caption" color={isGap ? 'error.main' : 'success.main'}>
          {isGap ? 'Gap detected' : 'On target'}
        </Typography>
      </CardContent>
    </Card>
  );
};

export default CompetencyCard;

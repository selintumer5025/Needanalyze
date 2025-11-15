import {
  Card,
  CardContent,
  MenuItem,
  Select,
  SelectChangeEvent,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Typography,
} from '@mui/material';

import { PlanItem } from '../api/employees';

interface Props {
  items: PlanItem[];
  onChangeStatus: (planId: number, status: string) => void;
}

const statuses = ['planned', 'in_progress', 'completed'];

const PlanTable: React.FC<Props> = ({ items, onChangeStatus }) => (
  <Card>
    <CardContent>
      <Typography variant="h6" gutterBottom>
        My Development Plan
      </Typography>
      <Table size="small">
        <TableHead>
          <TableRow>
            <TableCell>Activity</TableCell>
            <TableCell>Status</TableCell>
            <TableCell>Provider</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {items.map((item) => (
            <TableRow key={item.id}>
              <TableCell>
                <Stack>
                  <Typography variant="body2">{item.activity?.name || 'Activity'}</Typography>
                  <Typography variant="caption" color="text.secondary">
                    {item.activity?.type} · {item.activity?.duration_hours}h
                  </Typography>
                </Stack>
              </TableCell>
              <TableCell>
                <Select
                  size="small"
                  value={item.status}
                  onChange={(event: SelectChangeEvent) => onChangeStatus(item.id, event.target.value)}
                >
                  {statuses.map((status) => (
                    <MenuItem key={status} value={status}>
                      {status.replace('_', ' ')}
                    </MenuItem>
                  ))}
                </Select>
              </TableCell>
              <TableCell>{item.activity?.provider}</TableCell>
            </TableRow>
          ))}
          {items.length === 0 && (
            <TableRow>
              <TableCell colSpan={3}>
                <Typography variant="body2">No activities yet.</Typography>
              </TableCell>
            </TableRow>
          )}
        </TableBody>
      </Table>
    </CardContent>
  </Card>
);

export default PlanTable;

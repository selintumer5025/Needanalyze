import api from './client';

export interface Activity {
  id: number;
  code: string;
  name: string;
  type: string;
  modality: string;
  duration_hours: number;
  provider: string;
  description?: string;
}

export interface JourneyStep {
  title: string;
  description: string;
  activities: Activity[];
}

export interface GapRecommendation {
  competency_id: number;
  competency_name: string;
  current_level?: string;
  target_level: string;
  gap_level_difference: number;
  awareness_activities: Activity[];
  advanced_activities: Activity[];
  journey: JourneyStep[];
}

export interface RecommendationResponse {
  employee_id: number;
  employee_name: string;
  role: string;
  department: string;
  seniority_level: string;
  competency_gaps: GapRecommendation[];
}

export interface PlanItem {
  id: number;
  activity_id: number;
  status: string;
  planned_start_date?: string;
  completion_date?: string;
  activity?: Activity;
}

export const fetchRecommendations = async (employeeId: number) => {
  const { data } = await api.get<RecommendationResponse>(`/employees/${employeeId}/recommendations`);
  return data;
};

export const fetchPlan = async (employeeId: number) => {
  const { data } = await api.get<PlanItem[]>(`/employees/${employeeId}/plan`);
  return data;
};

export const addPlanItem = async (employeeId: number, payload: { activity_id: number; status?: string }) => {
  const { data } = await api.post<PlanItem>(`/employees/${employeeId}/plan`, payload);
  return data;
};

export const updatePlanItem = async (
  employeeId: number,
  planId: number,
  payload: Partial<{ status: string }>,
) => {
  const { data } = await api.patch<PlanItem>(`/employees/${employeeId}/plan/${planId}`, payload);
  return data;
};

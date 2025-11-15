import api from './client';
import { Activity } from './employees';

export interface Competency {
  id: number;
  name: string;
  category: string;
  description?: string;
}

export const listCompetencies = async () => {
  const { data } = await api.get<Competency[]>('/catalog/competencies');
  return data;
};

export const createCompetency = async (payload: Omit<Competency, 'id'>) => {
  const { data } = await api.post<Competency>('/catalog/competencies', payload);
  return data;
};

export const listActivities = async () => {
  const { data } = await api.get<Activity[]>('/catalog/activities');
  return data;
};

export const createActivity = async (payload: Omit<Activity, 'id'>) => {
  const { data } = await api.post<Activity>('/catalog/activities', payload);
  return data;
};

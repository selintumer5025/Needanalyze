import { ReactNode, createContext, useContext, useMemo, useState } from 'react';

interface AuthContextState {
  employeeId: number | null;
  employeeCode: string | null;
  isAuthenticated: boolean;
  login: (employeeCode: string) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextState | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [employeeCode, setEmployeeCode] = useState<string | null>(null);

  const login = (code: string) => {
    setEmployeeCode(code);
  };

  const logout = () => setEmployeeCode(null);

  const employeeId = employeeCode ? parseInt(employeeCode.replace(/\D/g, ''), 10) || 1 : null;

  const value = useMemo(
    () => ({
      employeeId,
      employeeCode,
      isAuthenticated: Boolean(employeeCode),
      login,
      logout,
    }),
    [employeeId, employeeCode],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return ctx;
};

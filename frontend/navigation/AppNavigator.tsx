// src/navigation/AppNavigator.tsx
import React from 'react';
import { createStackNavigator } from '@react-navigation/stack';
import { useAuth } from '../contexts/AuthContext';

// Pantallas de autenticación
import LoginScreen from '../screens/auth/LoginScreen';

// Pantallas de Administrador
import AdminDashboardScreen from '../screens/admin/AdminDashboardScreen';
import EstudiantesListScreen from '../screens/admin/EstudiantesListScreen';
import DocentesListScreen from '../screens/admin/DocentesListScreen';
import SeccionesListScreen from '../screens/admin/SeccionesListScreen';

// Pantallas de Docente
import DocenteDashboardScreen from '../screens/docente/DocenteDashboardScreen';

// Pantallas de Estudiante
import EstudianteDashboardScreen from '../screens/estudiante/EstudianteDashboardScreen';

// Loading screen
import LoadingScreen from '../screens/LoadingScreen';

const Stack = createStackNavigator();

export default function AppNavigator() {
  const { user, isLoading } = useAuth();

  if (isLoading) {
    return <LoadingScreen />;
  }

  return (
    <Stack.Navigator>
      {!user ? (
        // Stack de autenticación
        <Stack.Screen 
          name="Login" 
          component={LoginScreen} 
          options={{ headerShown: false }}
        />
      ) : (
        // Stack según el tipo de usuario
        user.tipo === 'admin' ? (
          // Stack de Administrador
          <>
            <Stack.Screen 
              name="AdminDashboard" 
              component={AdminDashboardScreen}
              options={{ title: 'Panel de Administración', headerLeft: () => null }}
            />
            <Stack.Screen 
              name="EstudiantesList" 
              component={EstudiantesListScreen}
              options={{ title: 'Lista de Estudiantes' }}
            />
            <Stack.Screen 
              name="DocentesList" 
              component={DocentesListScreen}
              options={{ title: 'Lista de Docentes' }}
            />
            <Stack.Screen 
              name="SeccionesList" 
              component={SeccionesListScreen}
              options={{ title: 'Gestión de Secciones' }}
            />
          </>
        ) : user.tipo === 'docente' ? (
          // Stack de Docente
          <>
            <Stack.Screen 
              name="DocenteDashboard" 
              component={DocenteDashboardScreen}
              options={{ title: 'Panel Docente', headerLeft: () => null }}
            />
          </>
        ) : (
          // Stack de Estudiante
          <>
            <Stack.Screen 
              name="EstudianteDashboard" 
              component={EstudianteDashboardScreen}
              options={{ title: 'Panel Estudiante', headerLeft: () => null }}
            />
          </>
        )
      )}
    </Stack.Navigator>
  );
}
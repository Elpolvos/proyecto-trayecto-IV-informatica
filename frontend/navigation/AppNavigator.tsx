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
import AsignaturasListScreen from '../screens/admin/AsignaturasListScreen';
import EstudiantesRegistroScreen from '../screens/admin/EstudiantesRegistroScreen';

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
        user.tipo === 'admin' || user.tipo === 'administrador' ? (
          // Stack de Administrador
          <>
            <Stack.Screen 
              name="AdminDashboard" 
              component={AdminDashboardScreen}
              options={{ headerShown: false }}
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
            <Stack.Screen
              name="AsignaturasList"
              component={AsignaturasListScreen}
              options={{ title: 'Gestión de Materias' }}
            />
            <Stack.Screen
              name="EstudiantesRegistro"
              component={EstudiantesRegistroScreen}
              options={{ title: 'Registro de Estudiantes' }}
            />
          </>
        ) : user.tipo === 'docente' ? (
          // Stack de Docente
          <>
            <Stack.Screen 
              name="DocenteDashboard" 
              component={DocenteDashboardScreen}
              options={{ headerShown: false }}
            />
          </>
        ) : (
          // Stack de Estudiante
          <>
            <Stack.Screen 
              name="EstudianteDashboard" 
              component={EstudianteDashboardScreen}
              options={{ headerShown: false }}
            />
          </>
        )
      )}
    </Stack.Navigator>
  );
}
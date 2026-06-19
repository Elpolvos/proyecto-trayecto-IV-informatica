// App.tsx
import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { PaperProvider, MD3LightTheme as DefaultTheme } from 'react-native-paper';
import { AuthProvider } from './frontend/contexts/AuthContext';
import AppNavigator from './frontend/navigation/AppNavigator';
import { Colors } from './frontend/utils/colors';

// Tema personalizado
const theme = {
  ...DefaultTheme,
  colors: {
    ...DefaultTheme.colors,
    primary: Colors.primary,
    secondary: Colors.secondary,
    tertiary: Colors.accent,
    error: Colors.error,
    background: Colors.background,
    surface: Colors.surface,
  },
};

export default function App() {
  return (
    <PaperProvider theme={theme}>
      <AuthProvider>
        <NavigationContainer>
          <AppNavigator />
        </NavigationContainer>
      </AuthProvider>
    </PaperProvider>
  );
}
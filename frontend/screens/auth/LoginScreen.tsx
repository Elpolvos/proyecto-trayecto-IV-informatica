import React, { useState } from 'react';
import {
  View,
  StyleSheet,
  KeyboardAvoidingView,
  Platform,
  Alert,
} from 'react-native';
import {
  TextInput,
  Button,
  Text,
  ActivityIndicator,
  Surface,
} from 'react-native-paper';
import { useAuth } from '../../contexts/AuthContext';
import { Colors } from '../../utils/colors';
import { useNavigation } from '@react-navigation/native';
import type { NavigationProp } from '@react-navigation/native';

// Definir los tipos de navegación
type RootStackParamList = {
  Login: undefined;
  AdminDashboard: undefined;
  DocenteDashboard: undefined;
  EstudianteDashboard: undefined;
};

export default function LoginScreen() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const { login } = useAuth();
  const navigation = useNavigation<NavigationProp<RootStackParamList>>();

  const handleLogin = async () => {
    // Validaciones
    if (!email.trim()) {
      Alert.alert('Error', 'Por favor ingresa tu email o DNI');
      return;
    }
    
    if (!password.trim()) {
      Alert.alert('Error', 'Por favor ingresa tu contraseña');
      return;
    }

    setLoading(true);
    const result = await login(email.trim(), password);
    setLoading(false);

    if (result.success && result.user) {
      // Redirigir según el tipo de usuario
      const userType = result.user.tipo;
      console.log('Usuario autenticado - Tipo:', userType);
      
      switch (userType) {
        case 'administrador':
          console.log('Redirigiendo a AdminDashboard');
          navigation.reset({
            index: 0,
            routes: [{ name: 'AdminDashboard' }],
          });
          break;
        case 'docente':
          console.log('Redirigiendo a DocenteDashboard');
          navigation.reset({
            index: 0,
            routes: [{ name: 'DocenteDashboard' }],
          });
          break;
        case 'estudiante':
          console.log('Redirigiendo a EstudianteDashboard');
          navigation.reset({
            index: 0,
            routes: [{ name: 'EstudianteDashboard' }],
          });
          break;
        default:
          console.log('Tipo de usuario no reconocido:', userType);
          Alert.alert('Error', 'Tipo de usuario no reconocido');
      }
    } else {
      Alert.alert('Error de autenticación', result.error || 'Error al iniciar sesión');
    }
  };

  return (
    <KeyboardAvoidingView
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      style={styles.container}
    >
      <View style={styles.content}>
        <View style={styles.logoContainer}>
          <Text variant="displaySmall" style={styles.title}>
            Sistema de Notas
          </Text>
          <Text variant="titleMedium" style={styles.subtitle}>
            Gestión Escolar
          </Text>
        </View>

        <View style={styles.form}>
          <Text variant="headlineSmall" style={{ marginBottom: 20, textAlign: 'center', fontWeight: 'bold' }}>
            Acceso
          </Text>
          <TextInput
            mode="outlined"
            label="Email o DNI"
            value={email}
            onChangeText={setEmail}
            autoCapitalize="none"
            keyboardType="email-address"
            left={<TextInput.Icon icon="email" />}
            style={styles.input}
            disabled={loading}
          />

          <TextInput
            mode="outlined"
            label="Contraseña"
            value={password}
            onChangeText={setPassword}
            secureTextEntry={!showPassword}
            right={
              <TextInput.Icon
                icon={showPassword ? 'eye-off' : 'eye'}
                onPress={() => setShowPassword(!showPassword)}
              />
            }
            left={<TextInput.Icon icon="lock" />}
            style={styles.input}
            disabled={loading}
          />

          <Button
            mode="contained"
            onPress={handleLogin}
            loading={loading}
            disabled={loading}
            style={styles.button}
            contentStyle={styles.buttonContent}
          >
            Iniciar Sesión
          </Button>
        </View>

        <View style={styles.infoContainer}>
          <Text variant="bodySmall" style={styles.infoText}>
            👨‍💼 Administrador: admin@colegio.edu
          </Text>
          <Text variant="bodySmall" style={styles.infoText}>
            👨‍🏫 Docente: docente@colegio.edu
          </Text>
          <Text variant="bodySmall" style={styles.infoText}>
            🧑‍🎓 Estudiante: 12345678 (DNI)
          </Text>
        </View>
      </View>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.background,
  },
  content: {
    flex: 1,
    justifyContent: 'center',
    paddingHorizontal: 24,
  },
  logoContainer: {
    alignItems: 'center',
    marginBottom: 48,
  },
  title: {
    textAlign: 'center',
    marginBottom: 8,
    color: Colors.primary,
    fontWeight: 'bold',
    letterSpacing: 1,
  },
  subtitle: {
    textAlign: 'center',
    color: Colors.textLight,
    fontWeight: '500',
  },
  form: {
    marginTop: 20,
    backgroundColor: 'white',
    padding: 20,
    borderRadius: 16,
    elevation: 4,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
  },
  input: {
    marginBottom: 16,
    backgroundColor: 'white',
  },
  button: {
    marginTop: 24,
    borderRadius: 12,
    paddingVertical: 4,
  },
  buttonContent: {
    paddingVertical: 8,
  },
  infoContainer: {
    marginTop: 32,
    padding: 16,
    backgroundColor: Colors.primary + '10', // Light primary background
    borderRadius: 12,
    borderWidth: 1,
    borderColor: Colors.primary + '20',
  },
  infoText: {
    color: Colors.primary,
    marginVertical: 4,
    fontWeight: '500',
  },
});
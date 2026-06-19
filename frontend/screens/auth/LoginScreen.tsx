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
          <Text variant="headlineMedium" style={styles.title}>
            Sistema de Gestión de Notas{"\n"}Unidad Educativa Colegio Simón Bolívar
          </Text>
          <Text variant="titleSmall" style={styles.subtitle}>
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

      <View style={styles.footer}>
        <Text style={styles.footerText}>
          AVISO DE COPYRIGHT: ESTA APLICACIÓN FUE ELABORADA POR LOS ESTUDIANTES DEL IUPTAI LUIS PARRA, DANIEL MENESES Y JOSE LUIS HERNANDEZ
        </Text>
      </View>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#E3F2FD', // Light blue-white background
  },
  content: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center', // Center content horizontally
    paddingHorizontal: 24,
  },
  logoContainer: {
    alignItems: 'center',
    marginBottom: 32,
  },
  title: {
    textAlign: 'center',
    marginBottom: 8,
    color: '#1565C0',
    fontWeight: 'bold',
    fontSize: 22,
  },
  subtitle: {
    textAlign: 'center',
    color: '#546E7A',
    fontWeight: '600',
    textTransform: 'uppercase',
    letterSpacing: 1,
  },
  form: {
    width: '100%',
    maxWidth: 340, // Reduce width of the form
    backgroundColor: 'white',
    padding: 24,
    borderRadius: 20,
    elevation: 6,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 3 },
    shadowOpacity: 0.15,
    shadowRadius: 10,
    alignItems: 'center', // Center form contents
  },
  input: {
    width: '100%', // Full width of the restricted form
    marginBottom: 16,
    backgroundColor: 'white',
    height: 50, // Slightly reduced height
  },
  button: {
    width: '100%',
    marginTop: 16,
    borderRadius: 12,
  },
  buttonContent: {
    paddingVertical: 6,
  },
  infoContainer: {
    width: '100%',
    maxWidth: 340,
    marginTop: 24,
    padding: 12,
    backgroundColor: 'rgba(255,255,255,0.6)',
    borderRadius: 12,
    borderWidth: 1,
    borderColor: '#BBDEFB',
  },
  infoText: {
    color: '#1976D2',
    marginVertical: 2,
    textAlign: 'center',
    fontSize: 11,
  },
  footer: {
    padding: 16,
    alignItems: 'center',
  },
  footerText: {
    fontSize: 10,
    color: '#78909C',
    textAlign: 'center',
    fontWeight: 'bold',
    lineHeight: 14,
  },
});
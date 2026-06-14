import React from 'react';
import { View, StyleSheet, ScrollView } from 'react-native';
import { Text, Card, Button, IconButton } from 'react-native-paper';
import { useAuth } from '../../contexts/AuthContext';
import { useNavigation } from '@react-navigation/native';

export default function EstudianteDashboardScreen() {
  const { user, logout } = useAuth();
  const navigation = useNavigation();

  const handleLogout = async () => {
    await logout();
    navigation.reset({
      index: 0,
      routes: [{ name: 'Login' }],
    });
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <View>
          <Text variant="headlineMedium" style={styles.welcomeText}>
            ¡Hola, {user?.nombre}!
          </Text>
          <Text variant="bodyMedium" style={styles.roleText}>
            Estudiante
          </Text>
        </View>
        <Button
          mode="contained"
          onPress={handleLogout}
          icon="logout"
          style={styles.logoutButton}
          buttonColor="#d32f2f"
        >
          Salir
        </Button>
      </View>

      <ScrollView style={styles.content}>
        <Card style={styles.card}>
          <Card.Title title="Mis Calificaciones" left={(props) => <IconButton {...props} icon="grade" />} />
          <Card.Content>
            <Text variant="bodyMedium">Consulta tus notas por materia y trimestre</Text>
          </Card.Content>
          <Card.Actions>
            <Button mode="contained">Ver Notas</Button>
          </Card.Actions>
        </Card>

        <Card style={styles.card}>
          <Card.Title title="Boletín PDF" left={(props) => <IconButton {...props} icon="file-pdf-box" />} />
          <Card.Content>
            <Text variant="bodyMedium">Genera tu boletín de calificaciones en PDF</Text>
          </Card.Content>
          <Card.Actions>
            <Button mode="outlined">Generar Boletín</Button>
          </Card.Actions>
        </Card>
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    backgroundColor: '#1565c0',
    padding: 20,
    paddingTop: 50,
    paddingBottom: 20,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  welcomeText: {
    color: 'white',
    fontWeight: 'bold',
  },
  roleText: {
    color: '#bbdef5',
    marginTop: 4,
  },
  logoutButton: {
    borderRadius: 8,
  },
  content: {
    padding: 16,
  },
  card: {
    marginBottom: 16,
    elevation: 2,
  },
});
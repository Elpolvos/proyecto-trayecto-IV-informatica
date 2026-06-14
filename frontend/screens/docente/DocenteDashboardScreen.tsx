import React from 'react';
import { View, StyleSheet, ScrollView } from 'react-native';
import { Text, Card, Button, IconButton } from 'react-native-paper';
import { useAuth } from '../../contexts/AuthContext';
import { Colors } from '../../utils/colors';
import { useNavigation } from '@react-navigation/native';

export default function DocenteDashboardScreen() {
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
            Bienvenido, {user?.nombre}
          </Text>
          <Text variant="bodyMedium" style={styles.roleText}>
            Docente
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
          <Card.Title title="Mis Materias" left={(props) => <IconButton {...props} icon="book-open-page-variant" />} />
          <Card.Content>
            <Text variant="bodyMedium">Aquí aparecerán tus materias asignadas</Text>
          </Card.Content>
        </Card>

        <Card style={styles.card}>
          <Card.Title title="Registrar Notas" left={(props) => <IconButton {...props} icon="grade" />} />
          <Card.Content>
            <Text variant="bodyMedium">Registro de calificaciones por materia</Text>
          </Card.Content>
          <Card.Actions>
            <Button mode="contained">Ir a Registrar Notas</Button>
          </Card.Actions>
        </Card>
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.background,
  },
  header: {
    backgroundColor: Colors.cardDocente,
    padding: 24,
    paddingTop: 60,
    paddingBottom: 30,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    borderBottomLeftRadius: 30,
    borderBottomRightRadius: 30,
    elevation: 8,
    shadowColor: Colors.cardDocente,
  },
  welcomeText: {
    color: 'white',
    fontWeight: 'bold',
  },
  roleText: {
    color: 'rgba(255,255,255,0.8)',
    marginTop: 4,
    fontWeight: '500',
  },
  logoutButton: {
    borderRadius: 12,
    backgroundColor: 'rgba(255,255,255,0.2)',
  },
  content: {
    padding: 16,
    marginTop: 10,
  },
  card: {
    marginBottom: 16,
    elevation: 4,
    borderRadius: 20,
    backgroundColor: 'white',
    overflow: 'hidden',
  },
});
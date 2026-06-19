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
        <View style={{ alignItems: 'center', flex: 1 }}>
          <Text style={styles.welcomeText}>
            ¡BIENVENIDO, {user?.nombre?.toUpperCase()}!
          </Text>
          <Text style={styles.roleText}>
            DOCENTE
          </Text>
        </View>
        <IconButton
          icon="logout"
          iconColor="white"
          size={24}
          onPress={handleLogout}
          style={styles.logoutIconButton}
        />
      </View>

      <ScrollView style={styles.content}>
        <Card style={styles.card}>
          <Card.Title
            title="Mis Materias Asignadas"
            titleStyle={styles.cardTitle}
            left={(props) => <IconButton {...props} icon="book-open-variant" />}
          />
          <Card.Content>
            <View style={styles.materiaItem}>
              <View>
                <Text style={styles.materiaName}>Matemáticas</Text>
                <Text style={styles.seccionName}>Sección A - 1er Año</Text>
              </View>
              <Button mode="text" onPress={() => {}}>Estudiantes</Button>
            </View>
          </Card.Content>
        </Card>

        <Card style={styles.card}>
          <Card.Title
            title="Registro de Calificaciones"
            titleStyle={styles.cardTitle}
            left={(props) => <IconButton {...props} icon="clipboard-edit-outline" />}
          />
          <Card.Content>
            <Text style={styles.infoText}>Selecciona una materia para registrar las notas de tus alumnos.</Text>
            <View style={styles.selectorContainer}>
              <Text style={styles.selectorLabel}>Materia: Matemáticas</Text>
              <Text style={styles.selectorLabel}>Sección: A</Text>
            </View>
          </Card.Content>
          <Card.Actions>
            <Button mode="contained" buttonColor="#2E7D32" icon="plus">Registrar Nuevas Notas</Button>
          </Card.Actions>
        </Card>

        <Card style={styles.card}>
          <Card.Title
            title="Listado de Estudiantes"
            titleStyle={styles.cardTitle}
            left={(props) => <IconButton {...props} icon="account-group-outline" />}
          />
          <Card.Content>
            <View style={styles.studentItem}>
              <Text style={styles.studentName}>Meneses, Daniel</Text>
              <Text style={styles.studentStatus}>V-12345678</Text>
            </View>
            <View style={styles.studentItem}>
              <Text style={styles.studentName}>Parra, Luis</Text>
              <Text style={styles.studentStatus}>V-87654321</Text>
            </View>
          </Card.Content>
        </Card>
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#E3F2FD',
  },
  header: {
    backgroundColor: '#1B5E20',
    padding: 20,
    paddingTop: 50,
    paddingBottom: 20,
    flexDirection: 'row',
    alignItems: 'center',
    borderBottomLeftRadius: 25,
    borderBottomRightRadius: 25,
    elevation: 5,
  },
  welcomeText: {
    color: 'white',
    fontWeight: 'bold',
    fontSize: 16,
    textAlign: 'center',
  },
  roleText: {
    color: '#C8E6C9',
    marginTop: 2,
    fontWeight: '700',
    fontSize: 12,
    letterSpacing: 1,
  },
  logoutIconButton: {
    position: 'absolute',
    right: 10,
    top: 45,
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
    paddingBottom: 8,
  },
  cardTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#455A64',
  },
  materiaItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 8,
    borderBottomWidth: 1,
    borderBottomColor: '#F5F5F5',
  },
  materiaName: {
    fontWeight: 'bold',
    color: '#1B5E20',
  },
  seccionName: {
    fontSize: 12,
    color: '#78909C',
  },
  infoText: {
    color: '#78909C',
    fontSize: 13,
    marginBottom: 12,
  },
  selectorContainer: {
    backgroundColor: '#E8F5E9',
    padding: 10,
    borderRadius: 8,
    marginBottom: 8,
  },
  selectorLabel: {
    fontWeight: '600',
    color: '#2E7D32',
    fontSize: 13,
  },
  studentItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingVertical: 10,
    borderBottomWidth: 1,
    borderBottomColor: '#E8F5E9',
  },
  studentName: {
    color: '#455A64',
    fontWeight: '500',
  },
  studentStatus: {
    fontSize: 12,
    color: '#78909C',
  },
});
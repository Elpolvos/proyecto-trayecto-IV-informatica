import React from 'react';
import { View, StyleSheet, ScrollView } from 'react-native';
import { Text, Card, Button, IconButton, Divider } from 'react-native-paper';
import { useAuth } from '../../contexts/AuthContext';
import { useNavigation } from '@react-navigation/native';
import type { NavigationProp } from '@react-navigation/native';

type AdminStackParamList = {
  AdminDashboard: undefined;
  EstudiantesList: undefined;
  DocentesList: undefined;
  SeccionesList: undefined;
};

export default function AdminDashboardScreen() {
  const { user, logout } = useAuth();
  const navigation = useNavigation<NavigationProp<AdminStackParamList>>();

  const handleLogout = async () => {
    await logout();
    navigation.reset({
      index: 0,
      routes: [{ name: 'Login' }],
    });
  };

  const menuItems = [
    {
      title: 'Estudiantes',
      icon: 'account-group',
      description: 'Gestionar estudiantes',
      route: 'EstudiantesList',
      color: '#1565c0',
    },
    {
      title: 'Docentes',
      icon: 'account-tie',
      description: 'Gestionar docentes',
      route: 'DocentesList',
      color: '#2e7d32',
    },
    {
      title: 'Secciones',
      icon: 'school',
      description: 'Gestionar secciones',
      route: 'SeccionesList',
      color: '#ed6c02',
    },
    {
      title: 'Asignaturas',
      icon: 'book-open-page-variant',
      description: 'Gestionar materias',
      route: 'AsignaturasList',
      color: '#9c27b0',
    },
    {
      title: 'Evaluaciones',
      icon: 'clipboard-list',
      description: 'Configurar evaluaciones',
      route: 'EvaluacionesList',
      color: '#d32f2f',
    },
    {
      title: 'Notas Finales',
      icon: 'grade',
      description: 'Ver notas finales',
      route: 'NotasFinales',
      color: '#ff9800',
    },
  ];

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <View>
          <Text variant="headlineMedium" style={styles.welcomeText}>
            ¡Bienvenido, {user?.nombre}!
          </Text>
          <Text variant="bodyMedium" style={styles.roleText}>
            Administrador del Sistema
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

      {/* Stats Cards */}
      <View style={styles.statsContainer}>
        <Card style={styles.statCard}>
          <Card.Content>
            <Text variant="titleLarge" style={styles.statNumber}>150</Text>
            <Text variant="bodyMedium">Estudiantes</Text>
          </Card.Content>
        </Card>
        <Card style={styles.statCard}>
          <Card.Content>
            <Text variant="titleLarge" style={styles.statNumber}>12</Text>
            <Text variant="bodyMedium">Docentes</Text>
          </Card.Content>
        </Card>
        <Card style={styles.statCard}>
          <Card.Content>
            <Text variant="titleLarge" style={styles.statNumber}>8</Text>
            <Text variant="bodyMedium">Secciones</Text>
          </Card.Content>
        </Card>
      </View>

      {/* Menu Grid */}
      <ScrollView style={styles.menuContainer}>
        <Text variant="titleLarge" style={styles.menuTitle}>
          Módulos del Sistema
        </Text>
        <View style={styles.menuGrid}>
          {menuItems.map((item, index) => (
            <Card
              key={index}
              style={styles.menuCard}
              onPress={() => navigation.navigate(item.route as any)}
            >
              <Card.Content style={styles.menuCardContent}>
                <View style={[styles.iconContainer, { backgroundColor: item.color + '15' }]}>
                  <IconButton icon={item.icon} size={40} iconColor={item.color} />
                </View>
                <Text variant="titleSmall" style={styles.menuItemTitle}>
                  {item.title}
                </Text>
                <Text variant="bodySmall" style={styles.menuItemDescription}>
                  {item.description}
                </Text>
              </Card.Content>
            </Card>
          ))}
        </View>
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
  statsContainer: {
    flexDirection: 'row',
    padding: 16,
    gap: 12,
  },
  statCard: {
    flex: 1,
    backgroundColor: 'white',
    elevation: 2,
    borderRadius: 12,
  },
  statNumber: {
    fontWeight: 'bold',
    color: '#1565c0',
  },
  menuContainer: {
    flex: 1,
    paddingHorizontal: 16,
  },
  menuTitle: {
    marginBottom: 16,
    fontWeight: '600',
  },
  menuGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
    gap: 12,
  },
  menuCard: {
    width: '48%',
    marginBottom: 16,
    backgroundColor: 'white',
    elevation: 2,
    borderRadius: 12,
  },
  menuCardContent: {
    alignItems: 'center',
    paddingVertical: 16,
  },
  iconContainer: {
    borderRadius: 50,
    padding: 8,
    marginBottom: 8,
  },
  menuItemTitle: {
    fontWeight: 'bold',
    textAlign: 'center',
    marginTop: 8,
  },
  menuItemDescription: {
    textAlign: 'center',
    color: '#666',
    marginTop: 4,
  },
});
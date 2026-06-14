import React from 'react';
import { View, StyleSheet, ScrollView } from 'react-native';
import { Text, Card, Button, IconButton, Divider, Surface } from 'react-native-paper';
import { useAuth } from '../../contexts/AuthContext';
import { Colors } from '../../utils/colors';
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
      description: 'Gestionar',
      route: 'EstudiantesList',
      color: '#4F46E5', // Indigo
    },
    {
      title: 'Docentes',
      icon: 'account-tie',
      description: 'Gestionar',
      route: 'DocentesList',
      color: '#10B981', // Emerald
    },
    {
      title: 'Secciones',
      icon: 'school',
      description: 'Gestionar',
      route: 'SeccionesList',
      color: '#F59E0B', // Amber
    },
    {
      title: 'Asignaturas',
      icon: 'book-open-page-variant',
      description: 'Gestionar',
      route: 'AsignaturasList',
      color: '#8B5CF6', // Violet
    },
    {
      title: 'Evaluaciones',
      icon: 'clipboard-list',
      description: 'Configurar',
      route: 'EvaluacionesList',
      color: '#EC4899', // Pink
    },
    {
      title: 'Notas Finales',
      icon: 'grade',
      description: 'Ver todo',
      route: 'NotasFinales',
      color: '#06B6D4', // Cyan
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
    backgroundColor: Colors.background,
  },
  header: {
    backgroundColor: Colors.cardAdmin,
    padding: 24,
    paddingTop: 60,
    paddingBottom: 30,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    borderBottomLeftRadius: 30,
    borderBottomRightRadius: 30,
    elevation: 8,
    shadowColor: Colors.cardAdmin,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 10,
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
  statsContainer: {
    flexDirection: 'row',
    padding: 16,
    marginTop: -20,
    gap: 12,
  },
  statCard: {
    flex: 1,
    backgroundColor: 'white',
    elevation: 4,
    borderRadius: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  statNumber: {
    fontWeight: 'bold',
    color: Colors.primary,
  },
  menuContainer: {
    flex: 1,
    paddingHorizontal: 16,
    marginTop: 10,
  },
  menuTitle: {
    marginBottom: 16,
    fontWeight: 'bold',
    color: Colors.text,
  },
  menuGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
    gap: 12,
    paddingBottom: 20,
  },
  menuCard: {
    width: '48%',
    marginBottom: 16,
    backgroundColor: 'white',
    elevation: 3,
    borderRadius: 20,
    borderWidth: 1,
    borderColor: 'rgba(0,0,0,0.05)',
  },
  menuCardContent: {
    alignItems: 'center',
    paddingVertical: 20,
  },
  iconContainer: {
    borderRadius: 20,
    padding: 4,
    marginBottom: 8,
  },
  menuItemTitle: {
    fontWeight: 'bold',
    textAlign: 'center',
    marginTop: 8,
    color: Colors.text,
  },
  menuItemDescription: {
    textAlign: 'center',
    color: Colors.textLight,
    marginTop: 4,
  },
});
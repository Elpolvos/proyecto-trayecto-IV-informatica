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
      title: 'Registro de Estudiantes',
      icon: 'account-plus',
      description: 'Alta de alumnos',
      route: 'EstudiantesRegistro',
      color: '#4F46E5',
    },
    {
      title: 'Registro de Docentes',
      icon: 'account-tie-voice',
      description: 'Alta de profesores',
      route: 'DocentesList',
      color: '#10B981',
    },
    {
      title: 'Registro de Secciones',
      icon: 'door-open',
      description: 'Aulas y grados',
      route: 'SeccionesList',
      color: '#F59E0B',
    },
    {
      title: 'Registro de Materias',
      icon: 'book-open-outline',
      description: 'Plan de estudios',
      route: 'AsignaturasList',
      color: '#8B5CF6',
    },
    {
      title: 'Listado Docentes (PDF)',
      icon: 'file-pdf-box',
      description: 'Docentes y Materias',
      action: 'pdf_docentes',
      color: '#E91E63',
    },
    {
      title: 'Listado Estudiantes (PDF)',
      icon: 'file-pdf-box',
      description: 'Por Secciones',
      action: 'pdf_estudiantes',
      color: '#FF5722',
    },
  ];

  const handleAction = (item: any) => {
    if (item.action === 'pdf_docentes') {
      Alert.alert('Generando PDF', 'Generando listado de docentes y materias...');
    } else if (item.action === 'pdf_estudiantes') {
      Alert.alert('Generando PDF', 'Generando listado de estudiantes por secciones...');
    } else if (item.route) {
      navigation.navigate(item.route as any);
    }
  };

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <View style={{ alignItems: 'center', flex: 1 }}>
          <Text style={styles.welcomeText}>
            ¡BIENVENIDO, {user?.nombre?.toUpperCase()}!
          </Text>
          <Text style={styles.roleText}>
            ADMINISTRADOR
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
              onPress={() => handleAction(item)}
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
    backgroundColor: '#E3F2FD',
  },
  header: {
    backgroundColor: '#1565C0',
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
    color: '#BBDEFB',
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
  statsContainer: {
    flexDirection: 'row',
    padding: 12,
    marginTop: -15,
    gap: 8,
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
    color: '#1565C0',
    fontSize: 18,
  },
  menuContainer: {
    flex: 1,
    paddingHorizontal: 16,
    marginTop: 10,
  },
  menuTitle: {
    marginBottom: 12,
    fontWeight: 'bold',
    color: '#455A64',
    textAlign: 'center',
    fontSize: 16,
    textTransform: 'uppercase',
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
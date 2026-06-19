import React from 'react';
import { View, StyleSheet, ScrollView } from 'react-native';
import { Text, Card, Button, IconButton } from 'react-native-paper';
import { useAuth } from '../../contexts/AuthContext';
import { Colors } from '../../utils/colors';
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
        <View style={{ alignItems: 'center', flex: 1 }}>
          <Text style={styles.welcomeText}>
            ¡BIENVENIDO, {user?.nombre?.toUpperCase()}!
          </Text>
          <Text style={styles.roleText}>
            ESTUDIANTE
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
        {/* Datos Personales */}
        <Card style={styles.card}>
          <Card.Title
            title="Mis Datos Personales"
            titleStyle={styles.cardTitle}
            left={(props) => <IconButton {...props} icon="account-details" />}
          />
          <Card.Content>
            <View style={styles.dataRow}>
              <Text style={styles.label}>Nombre:</Text>
              <Text style={styles.value}>{user?.nombre} {user?.apellido}</Text>
            </View>
            <View style={styles.dataRow}>
              <Text style={styles.label}>DNI:</Text>
              <Text style={styles.value}>{user?.dni}</Text>
            </View>
            <View style={styles.dataRow}>
              <Text style={styles.label}>Email:</Text>
              <Text style={styles.value}>{user?.email}</Text>
            </View>
          </Card.Content>
        </Card>

        {/* Mis Calificaciones */}
        <Card style={styles.card}>
          <Card.Title
            title="Mis Calificaciones"
            titleStyle={styles.cardTitle}
            left={(props) => <IconButton {...props} icon="grade" />}
          />
          <Card.Content>
            <Text style={styles.infoText}>Visualiza tus notas actuales por materia.</Text>
            {/* Aquí iría la lista de materias y notas mapeada desde el backend */}
            <View style={styles.gradeItem}>
              <Text style={styles.materiaName}>Matemáticas</Text>
              <Text style={styles.gradeValue}>18 / 20</Text>
            </View>
            <View style={styles.gradeItem}>
              <Text style={styles.materiaName}>Lenguaje</Text>
              <Text style={styles.gradeValue}>16 / 20</Text>
            </View>
          </Card.Content>
          <Card.Actions>
            <Button mode="contained" buttonColor="#1976D2">Ver Detalle Completo</Button>
          </Card.Actions>
        </Card>

        {/* Boletín Informativo */}
        <Card style={styles.card}>
          <Card.Title
            title="Boletín Informativo"
            titleStyle={styles.cardTitle}
            left={(props) => <IconButton {...props} icon="file-pdf-box" />}
          />
          <Card.Content>
            <Text style={styles.infoText}>Descarga tu resumen académico oficial en formato PDF al finalizar el trimestre.</Text>
          </Card.Content>
          <Card.Actions>
            <Button mode="contained" buttonColor="#F57C00" icon="download">Generar Boletín PDF</Button>
          </Card.Actions>
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
    backgroundColor: '#F57C00',
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
    color: '#FFE0B2',
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
  dataRow: {
    flexDirection: 'row',
    marginBottom: 8,
    borderBottomWidth: 1,
    borderBottomColor: '#F5F5F5',
    paddingBottom: 4,
  },
  label: {
    fontWeight: 'bold',
    color: '#1976D2',
    width: 80,
    fontSize: 13,
  },
  value: {
    color: '#455A64',
    flex: 1,
    fontSize: 13,
  },
  infoText: {
    color: '#78909C',
    fontSize: 13,
    marginBottom: 12,
  },
  gradeItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingVertical: 10,
    borderBottomWidth: 1,
    borderBottomColor: '#E3F2FD',
  },
  materiaName: {
    fontWeight: '600',
    color: '#455A64',
  },
  gradeValue: {
    fontWeight: 'bold',
    color: '#2E7D32',
  },
});
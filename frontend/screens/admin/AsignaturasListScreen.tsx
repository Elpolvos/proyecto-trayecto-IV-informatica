import React from 'react';
import { View, StyleSheet } from 'react-native';
import { Text, Button } from 'react-native-paper';
import { useNavigation } from '@react-navigation/native';

export default function AsignaturasListScreen() {
  const navigation = useNavigation();

  return (
    <View style={styles.container}>
      <Text variant="headlineSmall">Registro de Materias</Text>
      <Text variant="bodyMedium">Módulo para la gestión de asignaturas</Text>
      <Button onPress={() => navigation.goBack()} style={styles.button}>
        Volver
      </Button>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
    backgroundColor: '#E3F2FD',
  },
  button: {
    marginTop: 20,
  },
});

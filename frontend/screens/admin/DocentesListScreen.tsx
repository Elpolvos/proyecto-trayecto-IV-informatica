import React from 'react';
import { View, StyleSheet } from 'react-native';
import { Text, Button } from 'react-native-paper';
import { useNavigation } from '@react-navigation/native';

export default function DocentesListScreen() {
  const navigation = useNavigation();
  
  return (
    <View style={styles.container}>
      <Text variant="headlineSmall">Lista de Docentes</Text>
      <Text variant="bodyMedium">Aquí se mostrarán todos los docentes</Text>
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
  },
  button: {
    marginTop: 20,
  },
});
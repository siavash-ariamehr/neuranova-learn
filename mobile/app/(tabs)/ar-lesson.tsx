import { View, Text, StyleSheet } from 'react-native';

export default function ARLessonScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>AR/VR Lesson</Text>
      <Text style={styles.subtitle}>3D Molecular Visualization</Text>
      
      <View style={styles.infoBox}>
        <Text style={styles.infoText}>
          AR/VR lessons require a physical device with camera access.
        </Text>
        <Text style={styles.infoText}>
          Open this app on your iPhone or Android device using Expo Go to experience AR simulations.
        </Text>
      </View>
      
      <View style={styles.placeholder}>
        <Text style={styles.placeholderText}>📱</Text>
        <Text style={styles.placeholderText}>AR View Available on Physical Device</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
    padding: 16,
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#333',
    marginTop: 20,
  },
  subtitle: {
    fontSize: 18,
    color: '#666',
    marginBottom: 24,
  },
  infoBox: {
    backgroundColor: '#e0e7ff',
    borderRadius: 12,
    padding: 16,
    marginBottom: 24,
  },
  infoText: {
    fontSize: 14,
    color: '#4f46e5',
    marginBottom: 8,
  },
  placeholder: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'white',
    borderRadius: 12,
    padding: 32,
  },
  placeholderText: {
    fontSize: 48,
    color: '#666',
    textAlign: 'center',
    marginBottom: 8,
  },
});

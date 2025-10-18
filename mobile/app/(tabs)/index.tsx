import { View, Text, StyleSheet, ScrollView, TouchableOpacity } from 'react-native';
import { useState, useEffect } from 'react';

interface Lesson {
  id: number;
  title: string;
  subject: string;
  difficulty: string;
}

export default function HomeScreen() {
  const [lessons, setLessons] = useState<Lesson[]>([]);

  useEffect(() => {
    fetchLessons();
  }, []);

  const fetchLessons = async () => {
    try {
      const response = await fetch(process.env.EXPO_PUBLIC_BACKEND_URL + '/api/lessons');
      const data = await response.json();
      setLessons(data);
    } catch (error) {
      console.error('Failed to fetch lessons:', error);
    }
  };

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.title}>NeuraNova Learn</Text>
      <Text style={styles.subtitle}>Interactive STEM Education</Text>
      
      <View style={styles.lessonsContainer}>
        {lessons.map((lesson) => (
          <TouchableOpacity key={lesson.id} style={styles.lessonCard}>
            <Text style={styles.lessonTitle}>{lesson.title}</Text>
            <View style={styles.badges}>
              <Text style={styles.badge}>{lesson.subject}</Text>
              <Text style={styles.badge}>{lesson.difficulty}</Text>
            </View>
          </TouchableOpacity>
        ))}
      </View>
    </ScrollView>
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
  lessonsContainer: {
    gap: 12,
  },
  lessonCard: {
    backgroundColor: 'white',
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  lessonTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#333',
    marginBottom: 8,
  },
  badges: {
    flexDirection: 'row',
    gap: 8,
  },
  badge: {
    backgroundColor: '#e0e7ff',
    color: '#4f46e5',
    paddingHorizontal: 12,
    paddingVertical: 4,
    borderRadius: 12,
    fontSize: 12,
    fontWeight: '500',
  },
});

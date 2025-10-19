import React from 'react';
import { Tabs } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';

export default function TabLayout() {
  return (
    <Tabs
      screenOptions={{
        tabBarActiveTintColor: '#4f46e5',
        headerShown: false,
      }}
    >
      <Tabs.Screen
        name="(tabs)/index"
        options={{
          title: 'Home',
          tabBarIcon: ({ color, focused }) => (
            <Ionicons name={focused ? 'home' : 'home-outline'} color={color} size={24} />
          ),
        }}
      />
      <Tabs.Screen
        name="(tabs)/ar-lesson"
        options={{
          title: 'AR/VR',
          tabBarIcon: ({ color, focused }) => (
            <Ionicons name={focused ? 'cube' : 'cube-outline'} color={color} size={24} />
          ),
        }}
      />
      <Tabs.Screen
        name="(tabs)/collaboration"
        options={{
          title: 'Collaborate',
          tabBarIcon: ({ color, focused }) => (
            <Ionicons name={focused ? 'people' : 'people-outline'} color={color} size={24} />
          ),
        }}
      />
    </Tabs>
  );
}

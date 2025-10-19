import { View, Text, StyleSheet, TouchableOpacity, TextInput, FlatList } from 'react-native';
import { useState, useEffect } from 'react';
import { IRtcEngine, createAgoraRtcEngine, ChannelProfileType, ClientRoleType } from 'react-native-agora';

interface Message {
  id: string;
  text: string;
  sender: string;
  timestamp: Date;
}

export default function CollaborationScreen() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputText, setInputText] = useState('');
  const [sessionActive, setSessionActive] = useState(false);
  const [agoraEngine, setAgoraEngine] = useState<IRtcEngine | null>(null);

  useEffect(() => {
    initializeAgora();
    return () => {
      agoraEngine?.leaveChannel();
      agoraEngine?.release();
    };
  }, []);

  const initializeAgora = async () => {
    try {
      const engine = createAgoraRtcEngine();
      await engine.initialize({
        appId: process.env.EXPO_PUBLIC_AGORA_APP_ID || '',
      });
      
      engine.registerEventHandler({
        onJoinChannelSuccess: () => {
          console.log('Joined channel successfully');
          setSessionActive(true);
        },
        onUserJoined: (connection, uid) => {
          console.log('User joined:', uid);
        },
        onUserOffline: (connection, uid) => {
          console.log('User left:', uid);
        },
      });
      
      setAgoraEngine(engine);
    } catch (error) {
      console.error('Failed to initialize Agora:', error);
    }
  };

  const startSession = async () => {
    try {
      const response = await fetch(
        process.env.EXPO_PUBLIC_BACKEND_URL + '/api/collaboration/session',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${process.env.EXPO_PUBLIC_AUTH_TOKEN}`,
          },
          body: JSON.stringify({
            participants: [1]
          })
        }
      );
      
      const data = await response.json();
      
      if (agoraEngine) {
        await agoraEngine.setChannelProfile(ChannelProfileType.ChannelProfileCommunication);
        await agoraEngine.enableAudio();
        await agoraEngine.joinChannel(
          data.agora_token,
          data.agora_channel_name,
          0,
          {
            clientRoleType: ClientRoleType.ClientRoleBroadcaster,
          }
        );
      }
    } catch (error) {
      console.error('Failed to start session:', error);
    }
  };

  const sendMessage = () => {
    if (inputText.trim()) {
      const newMessage: Message = {
        id: Date.now().toString(),
        text: inputText,
        sender: 'You',
        timestamp: new Date(),
      };
      setMessages([...messages, newMessage]);
      setInputText('');
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Global Collaboration</Text>
      <Text style={styles.subtitle}>Real-time Learning with Peers</Text>

      {!sessionActive ? (
        <TouchableOpacity style={styles.startButton} onPress={startSession}>
          <Text style={styles.startButtonText}>Start Collaboration Session</Text>
        </TouchableOpacity>
      ) : (
        <View style={styles.sessionContainer}>
          <FlatList
            data={messages}
            keyExtractor={(item) => item.id}
            style={styles.messageList}
            renderItem={({ item }) => (
              <View style={styles.messageItem}>
                <Text style={styles.messageSender}>{item.sender}</Text>
                <Text style={styles.messageText}>{item.text}</Text>
                <Text style={styles.messageTime}>
                  {item.timestamp.toLocaleTimeString()}
                </Text>
              </View>
            )}
          />
          
          <View style={styles.inputContainer}>
            <TextInput
              style={styles.input}
              value={inputText}
              onChangeText={setInputText}
              placeholder="Type a message..."
              placeholderTextColor="#999"
            />
            <TouchableOpacity style={styles.sendButton} onPress={sendMessage}>
              <Text style={styles.sendButtonText}>Send</Text>
            </TouchableOpacity>
          </View>
        </View>
      )}
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
    fontSize: 28,
    fontWeight: 'bold',
    color: '#333',
    marginTop: 20,
  },
  subtitle: {
    fontSize: 16,
    color: '#666',
    marginBottom: 24,
  },
  startButton: {
    backgroundColor: '#4f46e5',
    padding: 16,
    borderRadius: 12,
    alignItems: 'center',
    marginTop: 32,
  },
  startButtonText: {
    color: 'white',
    fontSize: 18,
    fontWeight: '600',
  },
  sessionContainer: {
    flex: 1,
  },
  messageList: {
    flex: 1,
    marginBottom: 16,
  },
  messageItem: {
    backgroundColor: 'white',
    padding: 12,
    borderRadius: 8,
    marginBottom: 8,
  },
  messageSender: {
    fontWeight: '600',
    color: '#333',
    marginBottom: 4,
  },
  messageText: {
    color: '#666',
    marginBottom: 4,
  },
  messageTime: {
    fontSize: 12,
    color: '#999',
  },
  inputContainer: {
    flexDirection: 'row',
    gap: 8,
  },
  input: {
    flex: 1,
    backgroundColor: 'white',
    borderRadius: 8,
    padding: 12,
    fontSize: 16,
  },
  sendButton: {
    backgroundColor: '#4f46e5',
    paddingHorizontal: 20,
    borderRadius: 8,
    justifyContent: 'center',
  },
  sendButtonText: {
    color: 'white',
    fontWeight: '600',
  },
});

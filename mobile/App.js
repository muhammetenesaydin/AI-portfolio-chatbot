import React, { useState, useEffect, useRef } from 'react';
import {
  StyleSheet, Text, View, TextInput, TouchableOpacity,
  ScrollView, Alert, FlatList, ActivityIndicator, StatusBar, KeyboardAvoidingView, Platform
} from 'react-native';
import { SafeAreaView, SafeAreaProvider } from 'react-native-safe-area-context';
import * as DocumentPicker from 'expo-document-picker';
import * as FileSystem from 'expo-file-system';

const API_BASE = 'http://10.192.167.134:8000/api';

export default function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(false);

  // AUTH STATES
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLogin, setIsLogin] = useState(true);

  // DATA STATES
  const [candidates, setCandidates] = useState([]);
  const [quiz, setQuiz] = useState(null);
  
  // MESSAGING STATES
  const [currentScreen, setCurrentScreen] = useState('home'); // 'home' | 'chats' | 'chat_room'
  const [activeChats, setActiveChats] = useState([]);
  const [chatPartner, setChatPartner] = useState(null); // { id, name }
  const [messages, setMessages] = useState([]);
  const [msgInput, setMsgInput] = useState('');
  
  const chatInterval = useRef(null);

  // ─── AUTH ──────────────────────────────────────────────────────────────────
  const handleAuth = async () => {
    if (!email || !password) return Alert.alert('Hata', 'Alanları doldurun.');
    setLoading(true);
    try {
      const endpoint = isLogin ? '/auth/login' : '/auth/register';
      const body = isLogin
        ? { email, password }
        : { email, password, full_name: 'Mobil Kullanıcı', role: 'candidate' };

      const res = await fetch(`${API_BASE}${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || 'Giriş başarısız.');
      }
      const data = await res.json();
      setUser(data);
      if (data.role === 'hr') fetchCandidates();
    } catch (e) {
      Alert.alert('Hata', e.message || 'Bağlantı kurulamadı.');
    } finally {
      setLoading(false);
    }
  };

  // ─── API ÇAĞRILARI ────────────────────────────────────────────────────────
  const fetchCandidates = async () => {
    try {
      const res = await fetch(`${API_BASE}/candidates/`);
      if (!res.ok) return;
      const data = await res.json();
      setCandidates(data);
    } catch (e) { console.error('Adaylar yüklenemedi:', e); }
  };

  const pickAndUploadCV = async () => {
    try {
      const result = await DocumentPicker.getDocumentAsync({
        type: ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'],
      });
      if (result.canceled) return;
      setLoading(true);
      const fileUri = result.assets[0].uri;

      const uploadRes = await FileSystem.uploadAsync(`${API_BASE}/upload/`, fileUri, {
        fieldName: 'file', httpMethod: 'POST',
        uploadType: FileSystem.FileSystemUploadType.MULTIPART,
        headers: { 'user-id': String(user.id) },
      });

      const data = JSON.parse(uploadRes.body);
      if (data.quiz && data.quiz.questions?.length > 0) {
        setQuiz(data.quiz);
        Alert.alert('✅ Başarılı', `CV analiz edildi! Sınav hazır.`);
      } else {
        Alert.alert('⚠️ Uyarı', 'Sınav oluşturulamadı.');
      }
    } catch (e) {
      Alert.alert('Hata', 'Dosya yüklenemedi: ' + e.message);
    } finally {
      setLoading(false);
    }
  };

  // ─── MESAJLAŞMA FONKSİYONLARI ──────────────────────────────────────────────
  const fetchActiveChats = async () => {
    try {
      const res = await fetch(`${API_BASE}/messages/active-chats/${user.id}`);
      if (!res.ok) return;
      const data = await res.json();
      setActiveChats(data);
    } catch (e) { console.error('Sohbetler yüklenemedi:', e); }
  };

  const loadMessages = async () => {
    if (!chatPartner || !user) return;
    try {
      const res = await fetch(`${API_BASE}/messages/history/${user.id}/${chatPartner.id}`);
      if (!res.ok) return;
      const data = await res.json();
      setMessages(data);
    } catch (e) { console.error('Geçmiş yüklenemedi:', e); }
  };

  const sendMessage = async () => {
    if (!msgInput.trim() || !chatPartner) return;
    const text = msgInput.trim();
    setMsgInput('');
    // Anında ekranda göstermek için optimistic update
    setMessages(prev => [...prev, { id: Date.now(), sender_id: user.id, content: text }]);
    
    try {
      await fetch(`${API_BASE}/messages/send`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sender_id: user.id, receiver_id: chatPartner.id, content: text }),
      });
      loadMessages();
    } catch (e) { console.error('Gönderilemedi:', e); }
  };

  const openChatList = () => {
    setCurrentScreen('chats');
    fetchActiveChats();
  };

  const openChatRoom = (partnerId, partnerName) => {
    setChatPartner({ id: partnerId, name: partnerName });
    setCurrentScreen('chat_room');
    loadMessages();
    if (chatInterval.current) clearInterval(chatInterval.current);
    chatInterval.current = setInterval(loadMessages, 3000);
  };

  const goHome = () => {
    if (chatInterval.current) clearInterval(chatInterval.current);
    setCurrentScreen('home');
    setChatPartner(null);
  };

  // ─── RENDER BÖLÜMLERİ ──────────────────────────────────────────────────────
  
  if (!user) {
    return (
      <SafeAreaProvider>
        <StatusBar barStyle="light-content" backgroundColor="#222831" />
        <SafeAreaView style={styles.container}>
          <ScrollView contentContainerStyle={styles.loginContent} keyboardShouldPersistTaps="handled">
            <Text style={styles.logo}>🤖 AI Talent Hub</Text>
            <Text style={styles.subtitle}>{isLogin ? 'Yeteneklerle Buluş' : 'Yeni Profil Oluştur'}</Text>
            <TextInput style={styles.input} placeholder="E-posta" placeholderTextColor="#adb5bd" value={email} onChangeText={setEmail} autoCapitalize="none" keyboardType="email-address" />
            <TextInput style={styles.input} placeholder="Şifre" placeholderTextColor="#adb5bd" value={password} onChangeText={setPassword} secureTextEntry />
            <TouchableOpacity style={styles.primaryBtn} onPress={handleAuth} disabled={loading}>
              {loading ? <ActivityIndicator color="#f2f2f2" /> : <Text style={styles.btnText}>{isLogin ? 'Giriş Yap' : 'Kayıt Ol'}</Text>}
            </TouchableOpacity>
            <TouchableOpacity onPress={() => setIsLogin(!isLogin)} style={{ marginTop: 20 }}>
              <Text style={styles.toggleText}>{isLogin ? 'Hesabın yok mu? Kayıt Ol' : 'Zaten hesabın var mı? Giriş Yap'}</Text>
            </TouchableOpacity>
          </ScrollView>
        </SafeAreaView>
      </SafeAreaProvider>
    );
  }

  return (
    <SafeAreaProvider>
      <StatusBar barStyle="light-content" backgroundColor="#222831" />
      <SafeAreaView style={styles.container}>
        {/* Ortak Header */}
        <View style={styles.header}>
          {currentScreen === 'home' ? (
            <TouchableOpacity style={styles.logoutBtn} onPress={() => { if(chatInterval.current) clearInterval(chatInterval.current); setUser(null); }}>
              <Text style={styles.logoutText}>Çıkış</Text>
            </TouchableOpacity>
          ) : (
            <TouchableOpacity style={styles.logoutBtn} onPress={goHome}>
              <Text style={styles.logoutText}>← Geri</Text>
            </TouchableOpacity>
          )}
          
          <Text style={styles.headerTitle}>{currentScreen === 'chat_room' ? chatPartner?.name : 'AI Talent Hub'}</Text>
          
          {currentScreen === 'home' ? (
            <TouchableOpacity onPress={openChatList} style={styles.msgIconTop}>
              <Text style={{ fontSize: 20 }}>💬</Text>
            </TouchableOpacity>
          ) : <View style={{ width: 40 }} />}
        </View>

        {/* ANA EKRAN (HR veya ADAY) */}
        {currentScreen === 'home' && (
          user.role === 'hr' ? (
            <View style={{ flex: 1, padding: 20 }}>
              <View style={{ flexDirection:'row', justifyContent:'space-between', alignItems:'center', marginBottom:16 }}>
                <Text style={styles.sectionTitle}>Aday Havuzu</Text>
                <TouchableOpacity onPress={fetchCandidates}><Text style={{ color:'#f96d00', fontSize: 18 }}>🔄</Text></TouchableOpacity>
              </View>
              {candidates.length === 0 ? (
                <View style={styles.emptyBox}><Text style={styles.emptyText}>Henüz aday bulunmuyor.</Text></View>
              ) : (
                <FlatList
                  data={candidates}
                  keyExtractor={(item) => String(item.id)}
                  renderItem={({ item }) => (
                    <View style={styles.candCard}>
                      <View style={{ flex: 1 }}>
                        <Text style={styles.candName}>{item.name}</Text>
                        <Text style={styles.candDetails}>{item.experience_years} Yıl • Skor: %{item.quiz_score || 0} • 🛡️ {item.trust_score || 0}</Text>
                      </View>
                      <TouchableOpacity style={styles.msgBtn} onPress={() => openChatRoom(String(item.user_id || item.id), item.name)}>
                        <Text style={styles.msgBtnText}>Mesaj</Text>
                      </TouchableOpacity>
                    </View>
                  )}
                />
              )}
            </View>
          ) : (
            <ScrollView contentContainerStyle={styles.devContainer}>
              <Text style={styles.sectionTitle}>Hoş Geldin 👋</Text>
              <Text style={styles.candDetails}>Merhaba, {user.full_name || user.email}</Text>

              {quiz ? (
                <View style={[styles.card, { marginTop: 20 }]}>
                  <Text style={styles.cardTitle}>🧠 Teknik Sınav Hazır!</Text>
                  <Text style={styles.cardText}>{quiz.questions.length} adet yapay zeka sorusu seni bekliyor.</Text>
                  <TouchableOpacity style={styles.primaryBtn} onPress={() => Alert.alert('Sınav', 'Sınav ekranı yakında eklenecek!')}>
                    <Text style={styles.btnText}>Sınava Başla →</Text>
                  </TouchableOpacity>
                </View>
              ) : (
                <View style={[styles.uploadBox, { marginTop: 20 }]}>
                  <Text style={styles.uploadIcon}>📄</Text>
                  <Text style={styles.uploadText}>CV'ni yükle, AI sana özel teknik bir sınav hazırlasın.</Text>
                  <TouchableOpacity style={styles.primaryBtn} onPress={pickAndUploadCV} disabled={loading}>
                    {loading ? <ActivityIndicator color="#fff" /> : <Text style={styles.btnText}>📎 CV Seç ve Yükle</Text>}
                  </TouchableOpacity>
                </View>
              )}
            </ScrollView>
          )
        )}

        {/* MESAJ LİSTESİ EKRANI */}
        {currentScreen === 'chats' && (
          <View style={{ flex: 1, padding: 20 }}>
            <Text style={styles.sectionTitle}>Mesajlarım</Text>
            {activeChats.length === 0 ? (
              <View style={styles.emptyBox}><Text style={styles.emptyText}>Henüz aktif bir sohbetiniz bulunmuyor.</Text></View>
            ) : (
              <FlatList
                data={activeChats}
                keyExtractor={(item) => String(item.id)}
                renderItem={({ item }) => (
                  <TouchableOpacity style={styles.candCard} onPress={() => openChatRoom(String(item.id), item.full_name)}>
                    <View style={{ flex: 1, flexDirection: 'row', alignItems: 'center', gap: 12 }}>
                      <View style={styles.avatar}><Text style={styles.avatarText}>{item.full_name[0]}</Text></View>
                      <View>
                        <Text style={styles.candName}>{item.full_name}</Text>
                        <Text style={styles.candDetails}>{item.role === 'hr' ? 'İK Uzmanı' : 'Aday'}</Text>
                      </View>
                    </View>
                    <Text style={{fontSize: 18}}>💬</Text>
                  </TouchableOpacity>
                )}
              />
            )}
          </View>
        )}

        {/* SOHBET ODASI EKRANI */}
        {currentScreen === 'chat_room' && (
          <KeyboardAvoidingView style={{ flex: 1 }} behavior={Platform.OS === 'ios' ? 'padding' : undefined}>
            <FlatList
              data={messages}
              keyExtractor={(item, index) => String(item.id || index)}
              contentContainerStyle={{ padding: 15 }}
              renderItem={({ item }) => {
                const isMine = String(item.sender_id) === String(user.id);
                return (
                  <View style={[styles.msgBubble, isMine ? styles.msgMine : styles.msgTheirs]}>
                    <Text style={styles.msgText}>{item.content}</Text>
                  </View>
                );
              }}
            />
            <View style={styles.inputArea}>
              <TextInput
                style={styles.chatInput}
                placeholder="Mesaj yaz..."
                placeholderTextColor="#adb5bd"
                value={msgInput}
                onChangeText={setMsgInput}
              />
              <TouchableOpacity style={styles.sendBtn} onPress={sendMessage}>
                <Text style={{color: '#fff', fontWeight: 'bold'}}>Gönder</Text>
              </TouchableOpacity>
            </View>
          </KeyboardAvoidingView>
        )}
      </SafeAreaView>
    </SafeAreaProvider>
  );
}

// ─── STILLER ─────────────────────────────────────────────────────────────────
const styles = StyleSheet.create({
  container:    { flex: 1, backgroundColor: '#222831' },
  header:       { height: 70, flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', paddingHorizontal: 20, borderBottomWidth: 1, borderBottomColor: '#393e46', backgroundColor: '#222831' },
  headerTitle:  { color: '#f2f2f2', fontSize: 18, fontWeight: 'bold' },
  logoutBtn:    { backgroundColor: 'rgba(242,242,242,0.1)', paddingVertical: 8, paddingHorizontal: 12, borderRadius: 10 },
  logoutText:   { color: '#f2f2f2', fontWeight: '600', fontSize: 13 },
  msgIconTop:   { backgroundColor: 'rgba(249,109,0,0.15)', padding: 8, borderRadius: 12, borderWidth: 1, borderColor: 'rgba(249,109,0,0.4)' },

  loginContent: { flexGrow: 1, justifyContent: 'center', padding: 30 },
  logo:         { fontSize: 30, fontWeight: 'bold', color: '#f96d00', textAlign: 'center', marginBottom: 8 },
  subtitle:     { fontSize: 16, color: '#adb5bd', textAlign: 'center', marginBottom: 36 },
  input:        { backgroundColor: '#393e46', borderWidth: 1, borderColor: 'rgba(242,242,242,0.1)', borderRadius: 12, padding: 16, color: '#f2f2f2', marginBottom: 14, fontSize: 15 },
  primaryBtn:   { backgroundColor: '#f96d00', padding: 16, borderRadius: 12, alignItems: 'center', marginTop: 10 },
  btnText:      { color: '#f2f2f2', fontWeight: 'bold', fontSize: 16 },
  toggleText:   { color: '#adb5bd', textAlign: 'center' },

  sectionTitle: { color: '#f2f2f2', fontSize: 22, fontWeight: 'bold' },
  devContainer: { padding: 20, paddingBottom: 40 },
  uploadBox:    { backgroundColor: '#393e46', padding: 36, borderRadius: 24, borderStyle: 'dashed', borderWidth: 2, borderColor: 'rgba(242,242,242,0.2)', alignItems: 'center' },
  uploadIcon:   { fontSize: 48, marginBottom: 16 },
  uploadText:   { color: '#adb5bd', textAlign: 'center', marginBottom: 24, fontSize: 15, lineHeight: 22 },

  candCard:     { backgroundColor: '#393e46', padding: 18, borderRadius: 16, marginBottom: 12, flexDirection: 'row', alignItems: 'center', borderLeftWidth: 4, borderLeftColor: '#f96d00' },
  candName:     { color: '#f2f2f2', fontSize: 16, fontWeight: 'bold' },
  candDetails:  { color: '#adb5bd', marginTop: 4, fontSize: 13 },
  msgBtn:       { backgroundColor: 'rgba(249,109,0,0.15)', paddingVertical: 8, paddingHorizontal: 14, borderRadius: 10, borderWidth: 1, borderColor: 'rgba(249,109,0,0.4)', marginLeft: 10 },
  msgBtnText:   { color: '#f96d00', fontWeight: '600', fontSize: 13 },

  avatar:       { width: 40, height: 40, borderRadius: 20, backgroundColor: '#f96d00', alignItems: 'center', justifyContent: 'center' },
  avatarText:   { color: '#fff', fontWeight: 'bold', fontSize: 18 },

  emptyBox:     { flex: 1, alignItems: 'center', justifyContent: 'center', paddingTop: 60 },
  emptyText:    { color: '#adb5bd', fontSize: 16 },
  card:         { backgroundColor: '#393e46', padding: 24, borderRadius: 20, borderTopWidth: 4, borderTopColor: '#f96d00' },
  cardTitle:    { color: '#f2f2f2', fontSize: 18, fontWeight: 'bold', marginBottom: 10 },
  cardText:     { color: '#adb5bd', marginBottom: 20, lineHeight: 22 },

  // SOHBET EKRANI STILLERI
  msgBubble:    { maxWidth: '80%', padding: 14, borderRadius: 18, marginBottom: 10 },
  msgMine:      { alignSelf: 'flex-end', backgroundColor: '#f96d00', borderBottomRightRadius: 4 },
  msgTheirs:    { alignSelf: 'flex-start', backgroundColor: '#393e46', borderBottomLeftRadius: 4, borderWidth: 1, borderColor: 'rgba(242,242,242,0.1)' },
  msgText:      { color: '#fff', fontSize: 15, lineHeight: 20 },
  inputArea:    { flexDirection: 'row', padding: 15, borderTopWidth: 1, borderTopColor: '#393e46', backgroundColor: '#222831' },
  chatInput:    { flex: 1, backgroundColor: '#393e46', borderRadius: 24, paddingHorizontal: 18, color: '#fff', marginRight: 10, borderWidth: 1, borderColor: 'rgba(242,242,242,0.1)' },
  sendBtn:      { backgroundColor: '#f96d00', borderRadius: 24, paddingHorizontal: 20, justifyContent: 'center', alignItems: 'center' }
});

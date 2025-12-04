import React, { useEffect, useState } from 'react';
import { StyleSheet, Text, View, ScrollView, TouchableOpacity, ActivityIndicator } from 'react-native';
import { StatusBar } from 'expo-status-bar';
import axios from 'axios';

/**
 * ValorYield Mobile App
 * Sovereign Wealth Management on the go
 */
export default function App() {
  const [portfolio, setPortfolio] = useState(null);
  const [loading, setLoading] = useState(true);
  
  // API Configuration - Configure for your deployment
  // For local development: use your machine's IP (not localhost)
  // For production: use your API server URL
  // Example: 'http://192.168.1.100:8080/api/v1' or 'https://api.valoryield.example.com/api/v1'
  const API_BASE = process.env.EXPO_PUBLIC_API_URL || 'http://192.168.1.1:8080/api/v1';
  const getAuthToken = () => process.env.EXPO_PUBLIC_API_TOKEN || 'dev_token';

  useEffect(() => {
    fetchPortfolio();
  }, []);

  const fetchPortfolio = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API_BASE}/portfolio`, {
        headers: { Authorization: `Bearer ${getAuthToken()}` }
      });
      setPortfolio(response.data);
    } catch (error) {
      console.log('Using mock data:', error.message);
      // Fallback to mock data
      setPortfolio({
        balance: 207.69,
        account: '2143',
        allocation: 'Aggressive Mix',
        last_updated: new Date().toISOString()
      });
    } finally {
      setLoading(false);
    }
  };

  const handleRebalance = async () => {
    try {
      await axios.post(`${API_BASE}/rebalance`, { drift: 6 }, {
        headers: { Authorization: `Bearer ${getAuthToken()}` }
      });
      alert('🔄 Rebalance triggered – Legion analyzing');
    } catch (error) {
      alert('⚠️ Rebalance triggered (demo mode)');
    }
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#22D3EE" />
        <Text style={styles.loadingText}>Loading sovereignty...</Text>
      </View>
    );
  }

  return (
    <ScrollView style={styles.container}>
      <StatusBar style="light" />
      
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.title}>ValorYield</Text>
        <Text style={styles.subtitle}>Sovereign Wealth – 100% Yours</Text>
      </View>
      
      {/* Balance Card */}
      <View style={styles.card}>
        <Text style={styles.cardLabel}>Portfolio Balance</Text>
        <Text style={styles.balance}>${portfolio?.balance?.toFixed(2)}</Text>
        <View style={styles.meta}>
          <Text style={styles.metaText}>Account: {portfolio?.account}</Text>
          <Text style={styles.metaText}>Allocation: {portfolio?.allocation}</Text>
        </View>
      </View>
      
      {/* Allocation Grid */}
      <View style={styles.card}>
        <Text style={styles.cardLabel}>Target Allocation</Text>
        <View style={styles.allocationGrid}>
          <View style={styles.allocationItem}>
            <Text style={[styles.allocationPercent, { color: '#4ADE80' }]}>40%</Text>
            <Text style={styles.allocationLabel}>Stocks</Text>
          </View>
          <View style={styles.allocationItem}>
            <Text style={[styles.allocationPercent, { color: '#FBBF24' }]}>30%</Text>
            <Text style={styles.allocationLabel}>Crypto</Text>
          </View>
          <View style={styles.allocationItem}>
            <Text style={[styles.allocationPercent, { color: '#A78BFA' }]}>30%</Text>
            <Text style={styles.allocationLabel}>Futures</Text>
          </View>
        </View>
      </View>
      
      {/* Actions */}
      <View style={styles.actions}>
        <TouchableOpacity style={styles.primaryButton} onPress={handleRebalance}>
          <Text style={styles.buttonText}>🔄 Rebalance Now</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.secondaryButton} onPress={fetchPortfolio}>
          <Text style={styles.buttonTextSecondary}>🔃 Refresh</Text>
        </TouchableOpacity>
      </View>
      
      {/* Footer */}
      <View style={styles.footer}>
        <Text style={styles.footerText}>ValorYield Engine v1.0.0</Text>
        <Text style={styles.footerSubtext}>SwarmGate • NATS • AI Legion</Text>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#111827',
  },
  loadingContainer: {
    flex: 1,
    backgroundColor: '#111827',
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    color: '#9CA3AF',
    fontSize: 18,
    marginTop: 16,
  },
  header: {
    paddingTop: 60,
    paddingHorizontal: 24,
    paddingBottom: 24,
  },
  title: {
    fontSize: 36,
    fontWeight: 'bold',
    color: '#22D3EE',
  },
  subtitle: {
    fontSize: 16,
    color: '#9CA3AF',
    marginTop: 4,
  },
  card: {
    backgroundColor: '#1F2937',
    marginHorizontal: 16,
    marginBottom: 16,
    borderRadius: 12,
    padding: 20,
    borderWidth: 1,
    borderColor: '#374151',
  },
  cardLabel: {
    fontSize: 16,
    color: '#9CA3AF',
    marginBottom: 8,
  },
  balance: {
    fontSize: 48,
    fontWeight: 'bold',
    color: '#22D3EE',
  },
  meta: {
    marginTop: 16,
  },
  metaText: {
    color: '#D1D5DB',
    fontSize: 14,
    marginBottom: 4,
  },
  allocationGrid: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginTop: 16,
  },
  allocationItem: {
    alignItems: 'center',
    backgroundColor: '#374151',
    borderRadius: 8,
    padding: 16,
    width: '28%',
  },
  allocationPercent: {
    fontSize: 24,
    fontWeight: 'bold',
  },
  allocationLabel: {
    color: '#9CA3AF',
    fontSize: 12,
    marginTop: 4,
  },
  actions: {
    paddingHorizontal: 16,
    marginTop: 8,
  },
  primaryButton: {
    backgroundColor: '#22D3EE',
    borderRadius: 12,
    padding: 16,
    alignItems: 'center',
    marginBottom: 12,
  },
  buttonText: {
    color: '#000',
    fontSize: 18,
    fontWeight: 'bold',
  },
  secondaryButton: {
    backgroundColor: '#374151',
    borderRadius: 12,
    padding: 16,
    alignItems: 'center',
  },
  buttonTextSecondary: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
  },
  footer: {
    alignItems: 'center',
    paddingVertical: 32,
    borderTopWidth: 1,
    borderTopColor: '#374151',
    marginTop: 24,
    marginHorizontal: 16,
  },
  footerText: {
    color: '#6B7280',
    fontSize: 14,
  },
  footerSubtext: {
    color: '#4B5563',
    fontSize: 12,
    marginTop: 4,
  },
});

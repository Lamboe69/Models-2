# 🌐 MediSign Web Deployment Guide

## 🚀 Free Deployment Options

### 1. **Streamlit Cloud** (Recommended - Easiest)
- **URL**: https://share.streamlit.io/
- **Steps**:
  1. Sign in with GitHub
  2. Click "New app"
  3. Repository: `Lamboe69/Models-2`
  4. Branch: `master`
  5. Main file: `streamlit_app.py`
  6. Requirements: `requirements_streamlit.txt`
  7. Deploy!
- **Result**: `https://[your-app-name].streamlit.app`

### 2. **Railway** (Good Alternative)
- **URL**: https://railway.app/
- **Steps**:
  1. Connect GitHub repo
  2. Select `Lamboe69/Models-2`
  3. Railway auto-detects `railway.json`
  4. Deploy automatically
- **Result**: `https://[app-name].railway.app`

### 3. **Render** (Already Configured)
- **URL**: https://render.com/
- **Steps**:
  1. Connect GitHub repo
  2. Create new Web Service
  3. Build Command: `pip install -r requirements_streamlit.txt`
  4. Start Command: `streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0`
- **Result**: `https://[app-name].onrender.com`

### 4. **Vercel** (Serverless)
- **URL**: https://vercel.com/
- **Steps**:
  1. Import GitHub repo
  2. Vercel auto-detects `vercel.json`
  3. Deploy automatically
- **Result**: `https://[app-name].vercel.app`

## 🎯 Recommended: Streamlit Cloud

**Why Streamlit Cloud?**
- ✅ **Free forever** for public repos
- ✅ **Zero configuration** needed
- ✅ **Auto-deploys** on git push
- ✅ **Perfect for Streamlit apps**
- ✅ **Built-in sharing** features
- ✅ **No credit card** required

## 🔧 Local Testing

```bash
# Install dependencies
pip install -r requirements_streamlit.txt

# Run locally
streamlit run streamlit_app.py
```

## 📱 Features Available in Web Version

- ✅ **Bidirectional Translation**: Patient↔Clinician modes
- ✅ **Real-time Processing**: Connects to Clinical GAT API
- ✅ **Clinical Screening**: 8 infectious diseases
- ✅ **Triage Assessment**: WHO/MoH aligned
- ✅ **FHIR Integration**: Structured clinical data
- ✅ **Multi-language Support**: English, Runyankole, Luganda
- ✅ **Responsive Design**: Works on mobile/desktop
- ✅ **Privacy-first**: Offline-capable processing

## 🏥 Clinical GAT API

The web app connects to your deployed Clinical GAT model:
- **API URL**: https://models-2-ctfm.onrender.com
- **Endpoints**: `/predict`, `/health`, `/batch_predict`
- **Accuracy**: 86.7%
- **Latency**: <300ms

## 🔒 Security & Privacy

- **Offline-first**: Core processing can work offline
- **No data storage**: Session-based only
- **HIPAA considerations**: Suitable for screening scenarios
- **Encryption**: HTTPS by default on all platforms

## 📊 Monitoring

All platforms provide:
- **Real-time logs**
- **Performance metrics**
- **Error tracking**
- **Usage analytics**

Choose **Streamlit Cloud** for the easiest deployment! 🚀
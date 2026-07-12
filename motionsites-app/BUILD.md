# MotionSites APK Build Guide

## 环境要求
- Node.js 18+
- Java 17+
- Android Studio（或仅 Android SDK + Gradle）

## 构建步骤

### 1. 克隆仓库
```bash
git clone https://github.com/xianxian-sensen/motionsites-prompts.git
cd motionsites-prompts/motionsites-app
```

### 2. 安装依赖
```bash
npm install
```

### 3. 同步 Web 资源并构建 APK
```bash
npx cap sync android
cd android && ./gradlew assembleDebug
```

APK 文件位于: `android/app/build/outputs/apk/debug/app-debug.apk`

### 或者用 Android Studio 打开
```bash
npx cap open android
```
然后在 Android Studio 中点击 Build > Build Bundle(s) / APK(s) > Build APK(s)

## 技术信息
- 包名: `com.motionsites.gallery`
- 应用名: `MotionSites Gallery`
- 数据: 328 条提示词已内嵌到 HTML 中，完全离线可用
- 框架: Capacitor + WebView
# ProductivityRot 🧠📱

**Automatic dopamine management for vibe-coding.**

ProductivityRot automatically manages your distractions. It monitors a specific pixel on your screen to detect if you are actively coding/working or idling.
- **Idle/Thinking?** -> Automatically opens TikTok (Safari) on your second monitor.
- **Working/Typing?** -> Instantly kills TikTok to force focus.

## Features
- 🎯 **Pixel-Perfect Detection:** Uses strictly color-based detection (no image recognition overhead).
- 🖱️ **One-Click Calibration:** Easily set your trigger point and color via shortcut.
- ⚡ **Zero Latency:** Extremely lightweight background process.

## Setup

1. **Install Dependencies:**
   ```bash
   pip install pyautogui opencv-python pynput
# 答案 01：樹莓派基礎設定

> 對應作業：homework-01.md

## 答案說明

本作業主要測試學生是否能正確設定樹莓派的基本環境，並完成簡單的 GPIO 控制。重點在於熟悉 Linux 系統操作和 Python GPIO 程式設計。

## 任務一解答：系統安裝與初始化

### 解題步驟

1. 前往 Raspberry Pi 官網下載 Raspberry Pi Imager
2. 使用 Imager 將 Raspberry Pi OS 寫入 SD 卡
3. 將 SD 卡插入樹莓派並開機
4. 跟隨設定精靈完成初始設定
5. 開啟終端機執行系統更新

### 指令

```bash
# 更新套件列表
sudo apt update

# 升級所有套件
sudo apt upgrade -y

# 重新啟動系統
sudo reboot
```

### 說明

- `apt update` 會更新可用套件的清單
- `apt upgrade` 會將已安裝的套件升級到最新版本
- `-y` 參數會自動回答 yes，無需手動確認

## 任務二解答：網路設定

### 解題步驟

1. 使用圖形介面或命令列設定 Wi-Fi
2. （選擇性）編輯 `/etc/dhcpcd.conf` 設定靜態 IP
3. 使用 `ping` 測試網路連線
4. 啟用 SSH 服務

### 圖形介面方法

點選右上角的網路圖示，選擇要連接的 Wi-Fi 網路，輸入密碼即可。

### 命令列方法

```bash
# 掃描可用的 Wi-Fi 網路
sudo iwlist wlan0 scan | grep ESSID

# 編輯 Wi-Fi 設定
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
```

在檔案中加入：
```
network={
    ssid="您的WiFi名稱"
    psk="您的WiFi密碼"
}
```

### 啟用 SSH

```bash
# 使用 raspi-config
sudo raspi-config
# 選擇 Interface Options -> SSH -> Enable

# 或使用命令列
sudo systemctl enable ssh
sudo systemctl start ssh
```

### 測試網路

```bash
# 測試網路連線
ping -c 4 8.8.8.8

# 測試 DNS 解析
ping -c 4 google.com
```

## 任務三解答：GPIO 基礎測試

### 解題步驟

1. 安裝 GPIO 函式庫（通常已預裝）
2. 連接 LED 到 GPIO 接腳（例如 GPIO 17）和地線（GND）
3. 撰寫 Python 程式控制 LED
4. 執行程式觀察 LED 閃爍

### 硬體連接

- LED 長腳（正極）-> 220Ω 電阻 -> GPIO 17 (Pin 11)
- LED 短腳（負極）-> GND (Pin 6)

### 程式碼

```python
#!/usr/bin/env python3
# 檔名：led_blink.py

import RPi.GPIO as GPIO
import time

# 設定 GPIO 模式
GPIO.setmode(GPIO.BCM)

# 定義使用的 GPIO 接腳
LED_PIN = 17

# 設定 GPIO 17 為輸出模式
GPIO.setup(LED_PIN, GPIO.OUT)

try:
    print("LED 閃爍程式啟動（按 Ctrl+C 結束）")
    while True:
        GPIO.output(LED_PIN, GPIO.HIGH)  # LED 亮
        print("LED ON")
        time.sleep(1)  # 等待 1 秒
        
        GPIO.output(LED_PIN, GPIO.LOW)   # LED 滅
        print("LED OFF")
        time.sleep(1)  # 等待 1 秒

except KeyboardInterrupt:
    print("\n程式被使用者中斷")

finally:
    GPIO.cleanup()  # 清理 GPIO 設定
    print("GPIO 已清理，程式結束")
```

### 執行程式

```bash
# 賦予執行權限
chmod +x led_blink.py

# 執行程式
python3 led_blink.py

# 或使用 sudo（某些設定可能需要）
sudo python3 led_blink.py
```

### 說明

- `GPIO.setmode(GPIO.BCM)`：使用 BCM 編號模式（GPIO 編號）
- `GPIO.setup(LED_PIN, GPIO.OUT)`：設定該接腳為輸出模式
- `GPIO.output(LED_PIN, GPIO.HIGH)`：將接腳設為高電位（LED 亮）
- `GPIO.output(LED_PIN, GPIO.LOW)`：將接腳設為低電位（LED 滅）
- `GPIO.cleanup()`：清理 GPIO 設定，防止下次執行時出現警告

## 常見錯誤

1. **系統更新失敗**
   - 錯誤描述：執行 `apt update` 時出現網路錯誤
   - 正確做法：確認網路連線正常，檢查 DNS 設定

2. **SSH 無法連線**
   - 錯誤描述：使用 SSH 連線時被拒絕
   - 正確做法：確認 SSH 服務已啟用，防火牆未阻擋 22 端口

3. **GPIO 權限不足**
   - 錯誤描述：執行 GPIO 程式時出現權限錯誤
   - 正確做法：使用 `sudo` 執行程式，或將使用者加入 `gpio` 群組

4. **LED 不亮**
   - 錯誤描述：程式執行但 LED 沒有反應
   - 正確做法：
     - 檢查電路連接是否正確
     - 確認 LED 極性（長腳為正極）
     - 確認電阻是否連接
     - 檢查 GPIO 接腳編號是否正確

5. **程式無法停止**
   - 錯誤描述：程式持續執行無法結束
   - 正確做法：按 Ctrl+C 中斷程式執行

## 延伸學習

- 學習使用 PWM (Pulse Width Modulation) 控制 LED 亮度
- 嘗試控制多個 LED，製作跑馬燈效果
- 學習使用按鈕作為輸入，控制 LED 開關
- 探索其他 GPIO 函式庫，如 gpiozero（更簡單易用）
- 學習使用 I2C、SPI 等通訊協定連接感測器

### 使用 gpiozero 的簡化版本

```python
from gpiozero import LED
from time import sleep

led = LED(17)

while True:
    led.on()
    sleep(1)
    led.off()
    sleep(1)
```

這個版本更簡潔，不需要手動清理 GPIO。

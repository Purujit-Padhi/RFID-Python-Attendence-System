/*

--> The code is below the description... <--

# 📟 RFID + LCD Attendance Display (Arduino Sketch)

This Arduino sketch is part of a **smart attendance system** using an **RFID reader (MFRC522)**, a **16x2 LCD display**, and **Serial communication**. It's designed to work in sync with a Python-based desktop application to show student names and class info when RFID cards are scanned.

## 🔧 Hardware Used
- MFRC522 RFID Reader
- Arduino Uno/Nano
- 16x2 LCD (connected via 4-bit mode)
- Jumper wires & breadboard

## 🧠 Features
- 📡 **RFID Tag Scanning**: Detects new RFID cards and prints their UID to the Serial port.
- 🪪 **UID Display**: Sends UID to a connected Python application for student lookup.
- 🖥️ **LCD Display Support**: Receives display commands from Python via Serial and shows name & class.
- 🔁 **Dynamic Messages**: LCD resets to default "Scan Your Card" screen when idle.

## 🔌 Pin Configuration

| Component | Arduino Pin |
|----------|--------------|
| LCD RS   | 7            |
| LCD EN   | 6            |
| LCD D4   | 5            |
| LCD D5   | 4            |
| LCD D6   | 3            |
| LCD D7   | 2            |
| RFID SS  | 10           |
| RFID RST | 9            |
| RFID MOSI, MISO, SCK | SPI Pins (11, 12, 13) |

## 🧪 How It Works
1. The Arduino scans for new RFID cards.
2. On detecting a card, it prints the UID to Serial.
3. The connected Python program listens, matches UID to a student record, and sends back a command like: display John
4. The LCD shows the student’s name.

## 📝 Serial Commands
- `display Name → Displays the name on the LCD.
- `Initialize` → Arduino replies with "present".

## 📄 License
This project is licensed under the **Apache 2.0** – feel free to use and modify with attribution.

---

### 🤝 Contributions
Feel free to fork, raise issues, or suggest improvements! 

*/

// Main Code Starts Below


#include <SPI.h>
#include <MFRC522.h>
#include <LiquidCrystal.h>

#define SS_PIN 10
#define RST_PIN 9

MFRC522 rfid(SS_PIN, RST_PIN);  // Create MFRC522 instance
const int rs = 7, en = 6, d4 = 5, d5 = 4, d6 = 3, d7 = 2;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

void setup() {
  Serial.begin(115200);
  SPI.begin();        // Init SPI bus
  rfid.PCD_Init();    // Init MFRC522
  lcd.begin(16, 2);

  lcd.clear();
  lcd.print("Initializing");
  lcd.clear();
  lcd.print("Welcome !!");
  lcd.setCursor(0,1);
  lcd.print("Scan Ur Card:- ");
  lcd.setCursor(0,0);


  // Serial.println("Scan your RFID tag...");
}

void loop() {
  
  if (Serial.available()) {
    String receivedText = Serial.readStringUntil('\n'); // Read until newline
    // Check if the received text is "Search"
    
    if (receivedText.indexOf("display") >= 0) {
      int index = receivedText.indexOf("display ");
      if (index >= 0) {
        receivedText.remove(index, 8);  // 7 is the length of "display"
      }
      

      if (receivedText.indexOf(",") >= 0) {
        int indexcomma = receivedText.indexOf(",");
        String name = receivedText.substring(0, indexcomma);
        
        lcd.clear();
        lcd.print("-> " + name);
        lcd.setCursor(0,1);
        receivedText.remove(0,indexcomma+1);
        Serial.println(receivedText);
        lcd.print(receivedText);
        lcd.setCursor(0,0);
        return;
      }

      lcd.clear();
      lcd.print(receivedText);
      Serial.print("Received: ");
      Serial.println(receivedText);
       // Print the received text if it contains "display"
      if (receivedText == ""){
        lcd.clear();
        lcd.print("Welcome !!");
        lcd.setCursor(0,1);
        lcd.print("Scan Ur Card:- ");
        lcd.setCursor(0,0);
      }

    }

    if (receivedText.indexOf("Initialize") >= 0) {
      Serial.println("present");  // Print the received text if it contains "display"
    }
  }

  if (!rfid.PICC_IsNewCardPresent()) return;
  if (!rfid.PICC_ReadCardSerial()) return;

    // Store UID in a variable
    String uidStr = "";
    for (byte i = 0; i < rfid.uid.size; i++) {
      if (rfid.uid.uidByte[i] < 0x10) uidStr += "0";  // Add leading zero if needed
      uidStr += String(rfid.uid.uidByte[i], HEX);
    }

    // Serial.print("UID tag: ");
    Serial.println("UID tag: " + uidStr);

    // Halt the card
    rfid.PICC_HaltA();  
}

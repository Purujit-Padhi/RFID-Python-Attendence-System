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

#include <SPI.h>
#include <MFRC522.h>

// Define pins for both readers
#define RST_PIN_1 D2
#define SS_PIN_1 D1
#define RST_PIN_2 D4
#define SS_PIN_2 D3
#define RST_PIN_3 D0
#define SS_PIN_3 D8
#define tag1 
#define tag2

MFRC522 rfid1(SS_PIN_1, RST_PIN_1);
MFRC522 rfid2(SS_PIN_2, RST_PIN_2);
MFRC522 rfid3(SS_PIN_3, RST_PIN_3);

void setup() {
  Serial.begin(9600);
  SPI.begin();  // Initialize SPI bus

  // Initialize both RFID readers
  rfid1.PCD_Init();
  Serial.println("RFID-1 readers ready.");
  rfid2.PCD_Init();
  Serial.println("RFID-2 readers ready.");
  rfid3.PCD_Init();
  Serial.println("RFID-3 readers ready.");
}

void loop() {
  // Handle Reader 1
  if (rfid1.PICC_IsNewCardPresent() && rfid1.PICC_ReadCardSerial()) {
    Serial.print("Reader 1 UID: ");
    for (byte i = 0; i < rfid1.uid.size; i++) {
      Serial.print(rfid1.uid.uidByte[i], HEX);
    }
    Serial.println();
    rfid1.PICC_HaltA();
  }

  // Handle Reader 2
  if (rfid2.PICC_IsNewCardPresent() && rfid2.PICC_ReadCardSerial()) {
    Serial.print("Reader 2 UID: ");
    for (byte i = 0; i < rfid2.uid.size; i++) {
      Serial.print(rfid2.uid.uidByte[i], HEX);
    }
    Serial.println();
    rfid2.PICC_HaltA();
  }
   if (rfid3.PICC_IsNewCardPresent() && rfid3.PICC_ReadCardSerial()) {
    Serial.print("Reader 3 UID: ");
    for (byte i = 0; i < rfid3.uid.size; i++) {
      Serial.print(rfid3.uid.uidByte[i], HEX);
    }
    //logic
    if(rfid1.uid==tag1 && rfid2.uid=tag1)
    {

    }
    Serial.println();
    rfid3.PICC_HaltA();
  }
}
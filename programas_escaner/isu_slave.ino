#include <CmdMessenger.h>  // CmdMessenger
#include <LCD_I2C.h>

#define pinBuzzer 9
#define STR_SIZE 20

#define NOTE_C3  131
#define NOTE_G4  392
#define NOTE_C5  523

LCD_I2C lcd(0x27);

CmdMessenger cmdMessenger = CmdMessenger(Serial);

char linea1[STR_SIZE];
char linea2[STR_SIZE];

enum
{
  ping,
  pong,
  conectando,
  print_high,
  print2,
  print_low,
  ok_sound,
  fail_sound,
  apagar
};

void attachCommandCallbacks()
{
  // Attach callback methods
  cmdMessenger.attach(OnUnknownCommand);
  cmdMessenger.attach(ping, onPing);
  cmdMessenger.attach(conectando, onConectando);
  cmdMessenger.attach(print_high, onPrintHigh);
  cmdMessenger.attach(print2, onPrint2);
  cmdMessenger.attach(print_low, onPrintLow);
  cmdMessenger.attach(ok_sound, onOkSound);
  cmdMessenger.attach(fail_sound, onFailSound);
  cmdMessenger.attach(apagar, onApagar);
}

void OnUnknownCommand()
{
  onFailSound();
}

//Callbacks from python

void onPing() {
  cmdMessenger.sendCmd(pong);
}

void onConectando() {
  lcd.noBlink();
  lcd.clear();
  lcd.print(F("isu-mealsV1 CMI"));
  lcd.setCursor(0, 1);
  lcd.print(F("Connecting..."));
}

void onPrintHigh() {
  cmdMessenger.copyStringArg(linea1, STR_SIZE);
  lcd.clear();
  lcd.print(linea1);
}

void onPrintLow() {
  cmdMessenger.copyStringArg(linea2, STR_SIZE);
  lcd.clear();
  lcd.setCursor(0, 1);
  lcd.print(linea1);
}

void onPrint2() {
  cmdMessenger.copyStringArg(linea1, STR_SIZE);
  cmdMessenger.copyStringArg(linea2, STR_SIZE);
  lcd.clear();
  lcd.print(linea1);
  lcd.setCursor(0, 1);
  lcd.print(linea2);
}

void onOkSound() {
  int melody[] = {
    NOTE_G4, NOTE_C5, NOTE_C5
  };
  int noteDurations[] = {
    5, 3, 8
  };
  for (int thisNote = 0; thisNote < 3; thisNote++) {

    // to calculate the note duration, take one second divided by the note type.
    //e.g. quarter note = 1000 / 4, eighth note = 1000/8, etc.
    int noteDuration = 1000 / noteDurations[thisNote];
    tone(pinBuzzer, melody[thisNote], noteDuration);

    // to distinguish the notes, set a minimum time between them.
    // the note's duration + 30% seems to work well:
    int pauseBetweenNotes = noteDuration * 1.90;
    delay(pauseBetweenNotes);
    // stop the tone playing:
    noTone(pinBuzzer);
  }
}

void onFailSound() {
  int melody[] = {
    NOTE_G4, NOTE_C3
  };
  int noteDurations[] = {
    4, 10
  };
  for (int thisNote = 0; thisNote < 2; thisNote++) {

    // to calculate the note duration, take one second divided by the note type.
    //e.g. quarter note = 1000 / 4, eighth note = 1000/8, etc.
    int noteDuration = 1000 / noteDurations[thisNote];
    tone(pinBuzzer, melody[thisNote], noteDuration);

    // to distinguish the notes, set a minimum time between them.
    // the note's duration + 30% seems to work well:
    int pauseBetweenNotes = noteDuration * 1.90;
    delay(pauseBetweenNotes);
    // stop the tone playing:
    noTone(pinBuzzer);
  }
}

void onApagar(){
  lcd.clear();
  lcd.print(F("Powering"));
  lcd.setCursor(0,1);
  lcd.print("OFF");
  delay(30000);
  lcd.noBacklight();
}

void setup() {
  lcd.begin(); // If you are using more I2C devices using the Wire library use lcd.begin(false)
  // this stop the library(LCD_I2C) from calling Wire.begin()
  lcd.backlight();

  Serial.begin(19200);

  attachCommandCallbacks();

  onOkSound();
  onFailSound();
  
  lcd.print(F("isu-mealsV1 CMI"));
  lcd.setCursor(0, 1);
  lcd.print(F("Initializing..."));
  lcd.blink();
  lcd.noCursor();



}

void loop() {
  // put your main code here, to run repeatedly:
  cmdMessenger.feedinSerialData();
}

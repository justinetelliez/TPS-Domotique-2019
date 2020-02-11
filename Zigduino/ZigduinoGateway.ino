#include <ZigduinoRadio.h>

void setup()
{
  ZigduinoRadio.begin(11);
  Serial.begin(9600);
  
  ZigduinoRadio.attachError(errHandle);
  ZigduinoRadio.attachTxDone(onXmitDone);
}

void loop()
{
  
  if (Serial.available())
  {
    ZigduinoRadio.beginTransmission();
    
    while(Serial.available())
    {
      char c = Serial.read(); // on lit les informations communiquées par le serveur
      Serial.write(c);
      ZigduinoRadio.write(c); // on les transmet à l'autre Zigduino
    }
    
    ZigduinoRadio.endTransmission();
  }
  
  if (ZigduinoRadio.available())
  {
    

    if(ZigduinoRadio.getLastRssi() > -70){ // filtrage 
    
      while(ZigduinoRadio.available())
        Serial.write(ZigduinoRadio.read()); // on transmet les informations car
                                            // le serveur lit dans le port serie
      
    }
    
  }
  
  delay(100);
}

void errHandle(radio_error_t err)
{
  Serial.println();
  Serial.print("Error: ");
  Serial.print((uint8_t)err, 10);
  Serial.println();
}

void onXmitDone(radio_tx_done_t x) //utilisée pour le débuggage
{
  /*Serial.println();
  Serial.print("TxDone: ");
  Serial.print((uint8_t)x, 10);
  Serial.println();*/
}

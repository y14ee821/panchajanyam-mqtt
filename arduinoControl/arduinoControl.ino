#define ledPin1 2
#define ledPin2 3

#define switch1 4
#define switch2 5


void setup() {
    //Serial.begin(115200);
    pinMode(ledPin1, OUTPUT);
    pinMode(ledPin2, OUTPUT);

    pinMode(switch1, INPUT);
    pinMode(switch2, INPUT);
}

void loop() {
    //Serial.print("HI!");
    //Serial.print("Hel");
    //Serial.println(digitalRead(switch1));
    //Serial.println(digitalRead(switch2));
    //delay(200);
    if(digitalRead(switch1)==HIGH)
    {
      digitalWrite(ledPin1,HIGH);
    }
    else
    {
      digitalWrite(ledPin1,LOW);
    }


    if(digitalRead(switch2)==HIGH)
    {
      digitalWrite(ledPin2,HIGH);
    }
    else
    {
      digitalWrite(ledPin2,LOW);
    }
}
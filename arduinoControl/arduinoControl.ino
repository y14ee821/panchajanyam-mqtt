int numberOfOutputs=4;
//String receivedString = "op1:0-op2:0-op3:1-op4:0-op5:1";
bool logging = 0;
bool inversion = 1;// for inversting the output states(it will be useful if relay module has ground trigger.)
typedef struct{
  int opPin;
  int ipSwitchPin;
  String uartKey;
  String uartValue;
  unsigned long uartTime;
  unsigned long switchTime;
  String priority;
  int manualState;

} krishna;

unsigned long curTime=millis();
//initializing masterInfo with default values(op1,op2,op3,op4)
krishna masterInfo[]={
  {2,6,"op1","1",curTime,curTime,"-",0},
  {3,7,"op2","1",curTime,curTime,"-",0},
  {4,8,"op3","1",curTime,curTime,"-",0},
  {5,9,"op4","1",curTime,curTime,"-",0}
  };

// unsigned long  uartTime=millis();
// unsigned long switchTime=millis();
// String priority_individual="manual";
unsigned long startTime;
String priority;
void setup() 
{
Serial.begin(115200);
pinMode(masterInfo[0].opPin, OUTPUT);
pinMode(masterInfo[1].opPin, OUTPUT);
pinMode(masterInfo[2].opPin, OUTPUT);
pinMode(masterInfo[3].opPin, OUTPUT);
pinMode(masterInfo[0].ipSwitchPin, INPUT);
pinMode(masterInfo[1].ipSwitchPin, INPUT);
pinMode(masterInfo[2].ipSwitchPin, INPUT);
pinMode(masterInfo[3].ipSwitchPin, INPUT);
}

void loop() 
{

SwitchControl();
delay(50);

}

bool opInversion(int state)
{
  if(inversion == 1)
  {
    return(!state);
  }
  else
  {
    return state;
  }
}

void opControl(int ipSwitchPin,int opPin,int i )
{
  if(digitalRead(ipSwitchPin) == LOW)
  {
    digitalWrite(opPin, opInversion(0));
  }
  else
  {
    digitalWrite(opPin, opInversion(1));
  }
}


String priorityGenerator(unsigned long uartTime, unsigned long switchTime,String priority,int opPin,int i,int ipSwitchPin)
{
  if(uartTime == switchTime)
  {
    masterInfo[i].manualState = digitalRead(ipSwitchPin);
    masterInfo[i].priority = "manual";
       logging && Serial.println("control for"+String(opPin)+" is "+ masterInfo[i].priority );
    return priority;
  }

  if(uartTime > switchTime)
  {
    //masterInfo[i].manualState = digitalRead(ipSwitchPin);
    masterInfo[i].priority = "uart";

    logging && Serial.println("control for"+String(opPin)+" is "+ masterInfo[i].priority );
    return priority;
  }  
  
  if(uartTime < switchTime)
  {
    //masterInfo[i].manualState = digitalRead(ipSwitchPin);
    masterInfo[i].priority = "manual";
    logging && Serial.println("control for"+String(opPin)+" is "+ masterInfo[i].priority );
    return priority;
  }
  
}

void uartParserUpdater(String receivedString)
{
  for(int i=0;i<numberOfOutputs;i++)
  {
    int pos = int(receivedString.indexOf(masterInfo[i].uartKey))+4;   
    String state = receivedString.substring(pos,pos+1);
    if(state!=masterInfo[i].uartValue)//if there is any change in the UART value then timestamp will be changed.
    {
      masterInfo[i].uartTime = millis();
      masterInfo[i].uartValue = state;
    }
    else
    {
      logging && Serial.println("No change in the UART Value of"+masterInfo[i].uartKey);
    }
    
  }

}

void manualSwitchTimeUpdater(int ipSwitchPin, int i)
{

if(masterInfo[i].manualState!=digitalRead(ipSwitchPin))//if previous state != cur state, switch time will be updated and manual state will be updated to latest value.
{
  masterInfo[i].switchTime = millis();
 logging &&  Serial.println("Change detected in the Switch Value of Pin:"+String(ipSwitchPin));
  logging && Serial.println(masterInfo[i].switchTime);
  masterInfo[i].manualState=digitalRead(ipSwitchPin);//updating manual state to current one.
  //currentOP_States();
}
else
{
logging && Serial.println("No change in the Switch Value of Pin:"+String(ipSwitchPin));
}
}
void SwitchControl()
{
  
  for(int i=0;i<numberOfOutputs;i++)
  {
    manualSwitchTimeUpdater(masterInfo[i].ipSwitchPin, i);//updates if there is any change in the manual switch.
    if(Serial.available())
    {
      
      String data = Serial.readString();
      //Serial.println(data);
      uartParserUpdater(data);
      
      //delay(6000);
    }
//     else
//     {
// currentOP_States(); 
//     }
    
    priority = priorityGenerator(masterInfo[i].uartTime,masterInfo[i].switchTime,masterInfo[i].priority,masterInfo[i].opPin,i,masterInfo[i].ipSwitchPin);
    if(priority=="manual")
    {
      opControl(masterInfo[i].ipSwitchPin,masterInfo[i].opPin,i);
    }
    
    if(priority=="uart")
    {
      //Serial.println("hi");
      if(masterInfo[i].uartValue=="1")
      {
      digitalWrite(masterInfo[i].opPin,opInversion(1));
      }
      if(masterInfo[i].uartValue=="0")
      {
      digitalWrite(masterInfo[i].opPin,opInversion(0));
      }      
      //opControl(masterInfo[i].ipSwitchPin,masterInfo[i].opPin,i);
    }

}
//currentOP_States();
}



void currentOP_States()
{

//digitalRead(masterInfo[0].opPin);
//digitalRead(masterInfo[1].opPin);
//digitalRead(masterInfo[2].opPin);
//digitalRead(masterInfo[3].opPin);
// for(int i=0;i<4;i++)
// {
// Serial.println("Current Value of Pin: "+String(masterInfo[i].opPin)+" is "+String(digitalRead(masterInfo[i].opPin)));

//Serial.print("Lohit Siva Sai Varma Chinta ");
Serial.print(String(digitalRead(masterInfo[0].opPin))+"-"+String(digitalRead(masterInfo[1].opPin)));
// }


}



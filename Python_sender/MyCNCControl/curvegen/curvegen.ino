#include<math.h>

float x= 0;
float y = 0;
float z = 0;
float stepdist = 0.0009813542;
float pi = 3.141592;
int XIN1 = 2;
int XIN2 = 3;
int XIN3 = 4;
int XIN4 = 5;
int YIN1 = 6;
int YIN2 = 7;
int YIN3 = 8;
int YIN4 = 9;
int ZIN1 = A0;
int ZIN2 = A1;
int ZIN3 = A2;
int ZIN4 = A3;
int SPINDLE_PIN = 11;

int xstep=1;
int ystep=1;
int zstep=1;

int header;
int RPM = 0;

int FEED = 15 ;
int t,s;
int cStep;
int c1, c2, c3 , c4;
int ready = 1;

int dtime, times;
//FILE *f; 


float dRound(float number, int q){
    int mult = 1;
    if (number < 0){
        mult = -1;
        number = -number;
    }
    float aux = round( pow(10,q) * number);
    number = aux / pow(10,q);
    return mult * number;

}

float getAngle(float dx, float dy){
    float a;
    
    dx = dRound(dx,5);
    dy = dRound(dy,5);
    // Serial.println(dx);
    // Serial.println(dy);
    

    if (dx > 0){
         a = dy/dx;
        if (a>=0){
            return atan(a);
            }else{
                
            return (2*pi+atan(a));
            }
    }else if (dx == 0){
        if (dy > 0){
            return (pi / 2);
        }else{
            return (3*pi / 2 );}
    }else{
        a = dy/dx;
        return (pi + atan(a));}   
}
//--------------------------------------------------------------
void setRPM(int new_RPM){
  //int new_RPM = Serial.parseInt();
  
  //Serial.println(new_RPM);
  if (new_RPM == 0){
    RPM =0;
  }else if (new_RPM > 10000){
    RPM = 10000;
    
  }else if (new_RPM < 2000){
    RPM = 2000;
  }else{
    RPM = new_RPM; 
  }
  int old_s = s;
  s = RPM * 0.0255;
  if ( s > old_s){
    if (old_s == 0){
      old_s = 50;
    }
  for (old_s; old_s <= s; old_s ++){
     
    analogWrite(SPINDLE_PIN, old_s);
    delay(10);
    }
  }
  analogWrite(SPINDLE_PIN, s);
}

void report(){
  Serial.print(1);
  Serial.print(" ");
  Serial.print(x,3);
  Serial.print(" ");
  Serial.print(y,3);
  Serial.print(" ");
  Serial.print(z,3);
  Serial.print(" ");
  Serial.print(xstep);
  Serial.print(" ");
  Serial.print(ystep);
  Serial.print(" ");
  Serial.print(zstep);
  Serial.print(" ");
  Serial.print(FEED);
  Serial.print(" ");
  Serial.print(RPM);
  Serial.print(" ");
  Serial.print(ready);

  Serial.println();
} 

int stepIt(int axis, int dir){
  if (axis == 'x'){
    cStep = xstep; 
    c1 = XIN1;
    c2 = XIN2;
    c3 = XIN3;
    c4 = XIN4;
  }else if (axis == 'y'){
    cStep = ystep;
    c1 = YIN1;
    c2 = YIN2;
    c3 = YIN3;
    c4 = YIN4;
  }else {
    cStep = zstep;
    c1 = ZIN1;
    c2 = ZIN2;
    c3 = ZIN3;
    c4 = ZIN4;
  }
  
  
  cStep = cStep + dir;
  
  // if (cStep == 9){
  //   cStep = 1;
  // }else if (cStep == 0){
  //   cStep = 8;
  // }
  if (cStep > 8){
    cStep = cStep - 8;
  }else if (cStep < 1){
    cStep = cStep + 8;
  }
  
  switch(cStep){
  case 1:
    digitalWrite(c1 , HIGH);
    digitalWrite(c2 , LOW);
    digitalWrite(c3 , LOW);
    digitalWrite(c4 , LOW);
    break;
   case 2:
    digitalWrite(c1 , HIGH);
    digitalWrite(c2 , HIGH);
    digitalWrite(c3 , LOW);
    digitalWrite(c4 , LOW);
    break;
   case 3:
    digitalWrite(c1 , LOW);
    digitalWrite(c2 , HIGH);
    digitalWrite(c3 , LOW);
    digitalWrite(c4 , LOW);
    break;
   case 4:
    digitalWrite(c1 , LOW);
    digitalWrite(c2 , HIGH);
    digitalWrite(c3 , HIGH);
    digitalWrite(c4 , LOW);
    break;
   case 5:
    digitalWrite(c1 , LOW);
    digitalWrite(c2 , LOW);
    digitalWrite(c3 , HIGH);
    digitalWrite(c4 , LOW);
    break;
   case 6:
    digitalWrite(c1 , LOW);
    digitalWrite(c2 , LOW);
    digitalWrite(c3 , HIGH);
    digitalWrite(c4 , HIGH);
    break;
   case 7:
    digitalWrite(c1 , LOW);
    digitalWrite(c2 , LOW);
    digitalWrite(c3 , LOW);
    digitalWrite(c4 , HIGH);
    break;
   case 8:
    digitalWrite(c1 , HIGH);
    digitalWrite(c2 , LOW);
    digitalWrite(c3 , LOW);
    digitalWrite(c4 , HIGH);
    break;
   default:
    digitalWrite(c1 , LOW);
    digitalWrite(c2 , LOW);
    digitalWrite(c3 , LOW);
    digitalWrite(c4 , LOW);
    break;
  }
   if (axis == 'x'){
    xstep = cStep; 
    
  }else if (axis == 'y'){
    ystep = cStep;
    
  }else {
    zstep = cStep;
    
  }
  

  
}

int intdiv(float a, float b){
    int c = dRound(a , 10)/dRound(b , 10);;
    
    
    return c;
}


void moveSteppers(int movetype , float gox, float goy, float goz, float cex , float cey ){
  
  
  
  
    float nex = x;
    float ney = y;
    float nez = z;
    if (movetype == 0 || movetype == 1){
      
      float dx = gox - x;
      float dy = goy - y;
      float dz = goz - z;

      float curvelen = sqrt(dx*dx + dy*dy + dz*dz) + stepdist;
      

      unsigned long steps = curvelen/stepdist;
      steps += 2;
      //Serial.println(steps);

      dx /= steps;
      dy /= steps;
      dz /= steps;

      

      for (unsigned long i = 0; i < steps ; i++ ){
        if (Serial.available()>0){
          if (Serial.parseInt() == 9){
            setRPM(0);
            break;
          }
        }
        if (i % 100 == 0){
          report();
        }
        nex += dx;
        ney += dy;
        nez += dz;
        int dox = intdiv((nex - x),stepdist);
        int doy = intdiv((ney - y),stepdist);
        int doz = intdiv((nez - z),stepdist); 

        // Do moves
        
        for (int r =0; r < 4; r++){
          stepIt('x', -(dox));        
          stepIt('y', (doy));        
          stepIt('z', -(doz));   
          delay(1);     
        }
        x += dox * stepdist;
        y += doy * stepdist;
        z += doz * stepdist;
        }
    }else if (movetype == 2 || movetype ==3){
      
        int dir = -1;
        float start_ang = getAngle(-cex, -cey);
        // Serial.print(start_ang);
        // Serial.print(' ');
        
        float end_ang = getAngle(gox - (x + cex), goy - (y + cey));
        // Serial.print(end_ang);
        // Serial.print(' ');
       
        
        float da =  start_ang - end_ang ;
        if (da<0){
            da += 2* pi;
        }

        if (movetype == 3){
            da = 2 * pi - da;
            dir = 1;
        }
        // Serial.print(da);
        // Serial.print(' ');

    
    float r = sqrt(cex*cex + cey*cey);
    
    

    float dt = stepdist / r * dir;
    

    unsigned long steps = (dRound(da,5) / dRound(abs(dt),5)) ;
    
    

    float dz = (goz - z) / steps; 

    float ang = start_ang;
    float startx = x;
    float starty = y;

    for (unsigned long i =0; i < steps; i++){
      if (Serial.available()>0){
        if (Serial.parseInt() == 9){
          setRPM(0);
          break;
        }
      }
      if (i % 100 == 0){
        report();
      }
        
        ang += dt;
        
        nex = startx + cex + r * (cos(ang));
        ney = starty + cey + r * (sin(ang));
        nez += dz;
        int dox = intdiv((nex - x),stepdist);
        int doy = intdiv((ney - y),stepdist);
        int doz = intdiv((nez - z),stepdist); 

        // Do moves


        for (int r =0; r < 4; r++){
        stepIt('x', -(dox));        
        stepIt('y', (doy));        
        stepIt('z', -(doz));   
        delay(1);     
      }
      x += dox * stepdist;
      y += doy * stepdist;
      z += doz * stepdist;
        
      

    }
    }




    }



void setup(){
    pinMode(XIN1, OUTPUT);
    pinMode(XIN2, OUTPUT);
    pinMode(XIN3, OUTPUT);
    pinMode(XIN4, OUTPUT);
    pinMode(YIN1, OUTPUT);
    pinMode(YIN2, OUTPUT);
    pinMode(YIN3, OUTPUT);
    pinMode(YIN4, OUTPUT);
    pinMode(ZIN1, OUTPUT);
    pinMode(ZIN2, OUTPUT);
    pinMode(ZIN3, OUTPUT);
    pinMode(ZIN4, OUTPUT);
    pinMode(SPINDLE_PIN,OUTPUT);
    pinMode(13,OUTPUT);
    //pinMode(13, OUTPUT);

    Serial.begin(115200);
    Serial.setTimeout(10);
    
}

void REF(){
  digitalWrite(13, HIGH);
  x = Serial.parseFloat();
  y = Serial.parseFloat();
  z = Serial.parseFloat();

  xstep = Serial.parseInt();
  ystep = Serial.parseInt();
  zstep = Serial.parseInt();
  for (int i = 0; i<=8; i++){
    stepIt('x', 1);
    delay(100);    
  }
  delay(500);
  for (int i = 0; i<=8; i++){
    stepIt('x', -1);
    delay(100);    
  }
  for (int i = 0; i<=8; i++){
    stepIt('y', 1);
    delay(100);    
  }
  delay(500);
  for (int i = 0; i<=8; i++){
    stepIt('y', -1);
    delay(100);    
  }
  for (int i = 0; i<=8; i++){
    stepIt('z', 1);
    delay(100);    
  }
  delay(500);
  for (int i = 0; i<=8; i++){
    stepIt('z', -1);
    delay(100);    
  }
  analogWrite(SPINDLE_PIN, 20);
  delay(100);
  analogWrite(SPINDLE_PIN, 0);
  delay(100);
  analogWrite(SPINDLE_PIN, 20);
  delay(100);
  analogWrite(SPINDLE_PIN, 0);
  delay(100);
  analogWrite(SPINDLE_PIN, 20);
  delay(100);
  analogWrite(SPINDLE_PIN, 0);
  delay(100);
  digitalWrite(13, LOW);
  

  
}


  
void setFEED(int new_feed){
  if( new_feed <= 14){
  FEED = new_feed;
}else{
  FEED = 14;
}
  t = 60 /(4076 * FEED);           
}


int read1;
float read2;
float read3;
float read4;
float read5;
float read6;

void loop(){
    if (Serial.available() > 0){
      header = Serial.parseInt();
      ready = 0;
      switch(header){
          case 1://REF
              REF();
              ready =1;
              report();
              break;
          case 2: // MOVE
              read1 = Serial.parseInt();
              read2 = Serial.parseFloat();
              read3 = Serial.parseFloat();
              read4 = Serial.parseFloat();
              read5 = Serial.parseFloat();
              read6 = Serial.parseFloat();
              moveSteppers(read1, read2, read3, read4, read5, read6);
              ready = 1;
              report();
              break;
          case 3: // FEED
              setFEED(Serial.parseInt());
              ready = 1;
              report();
              
              break;
          case 4: // RPM
              setRPM(Serial.parseInt());
              ready =1;
              report();
              break;
          case 5: // REPORT
              ready = 1;
              report();
              
          case 9:
              setRPM(0);
              ready = 1;
              report();

          default:
              
              break;



        }
    }
}

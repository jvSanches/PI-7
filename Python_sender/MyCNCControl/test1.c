i
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
    dx = dRound(dx,10);
    dy = dRound(dy,10);
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
void main(){

}
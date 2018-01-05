model MoonLanding
  parameter Real g = 6.672e-11;
  parameter Real massLossRate = 0.0000277;
  parameter Real radius_moon = 1.738e6;
  parameter Real mass_moon = 7.38e22;
  parameter Real radius_sun = 6.96e8;
  parameter Real mass_sun = 1.9891e30;
  parameter Real radius_earth = 6.371e6;
  parameter Real mass_earth = 5.972e24;
  parameter Real earth_moon_distance = 3.844e8;
  parameter Real earth_sun_distance = 1.49982270e15;

  input Real thrust;
  output Real v; 
  output Real a; 
  
  Real gravity;
  Real mass(start = 75000, fixed=true);
  Real altitude(start = 60000, fixed=true);
  Real velocity(start = -2000, fixed=true);
equation
  der(mass) = -massLossRate * abs(thrust);
  der(altitude) = velocity;
  der(velocity) = (thrust + mass * gravity) / mass;
  gravity = -g*mass_earth/(earth_moon_distance-altitude+radius_earth)^2 
  - g*mass_moon/(altitude+radius_moon)^2 
  + g*mass_sun/(earth_sun_distance - altitude + radius_sun)^2;
  
  //output equation:
  v = velocity;
  a = altitude;
end MoonLanding;

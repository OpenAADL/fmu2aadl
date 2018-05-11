model Aircraft_Dynamics
  /* Atmosphere parameters */
  constant Real T0_h = -0.0065;
  constant Real T0_0 = 288.15;
  constant Real g0 = 9.80665;
  constant Real rho0 = 1.225;
  constant Real Rs = 287.05;
  /* Aircraft parameters */
  constant Real masse = 57837.5;
  constant Real I_y = 3781272.0;
  constant Real S = 122.6;
  constant Real cbar = 4.29;
  constant Real CD_0 = 0.016;
  constant Real CD_alpha = 2.5;
  constant Real CD_deltae = 0.05;
  constant Real CL_alpha = 5.5;
  constant Real CL_deltae = 0.193;
  constant Real alpha_0 = -0.05;
  constant Real Cm_0 = 0.04;
  constant Real Cm_alpha = -0.83;
  constant Real Cm_deltae = -1.5;
  constant Real Cm_q = -30.0;
  /* Trimming parameters */
  constant Real h_eq = 10000.0;
  constant Real Va_eq = 230.0;
  constant Real Vz_eq = 0.0;
  constant Real alpha_eq = 0.026485847681737;
  constant Real theta_eq = 0.026485847681737;
  Modelica.Blocks.Interfaces.RealInput delta_e annotation(
    Placement(visible = true, transformation(origin = {-120, 50}, extent = {{-20, -20}, {20, 20}}, rotation = 0), iconTransformation(origin = {-120, -54}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
  //Elevator deflection
  Modelica.Blocks.Interfaces.RealInput T annotation(
    Placement(visible = true, transformation(origin = {-120, -50}, extent = {{-20, -20}, {20, 20}}, rotation = 0), iconTransformation(origin = {-120, 50}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
  //Engine thrust
  Modelica.Blocks.Interfaces.RealOutput Va annotation(
    Placement(visible = true, transformation(origin = {110, 80}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {110, 84}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  //True airspeed
  Modelica.Blocks.Interfaces.RealOutput Vz annotation(
    Placement(visible = true, transformation(origin = {110, 40}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {110, 40}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  //Vertical air speed
  Modelica.Blocks.Interfaces.RealOutput q_out annotation(
    Placement(visible = true, transformation(origin = {110, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {110, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  //Pitch rate
  Modelica.Blocks.Interfaces.RealOutput az annotation(
    Placement(visible = true, transformation(origin = {110, -40}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {110, -40}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  //Vertical acceleration
  Modelica.Blocks.Interfaces.RealOutput h_out annotation(
    Placement(visible = true, transformation(origin = {110, -80}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {110, -80}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  //Altitude
  Real u(start = 0.0);
  Real w(start = 0.0);
  Real theta(start = 0.0);
  Real q(start = 0.0);
  Real h(start = 0.0);
  Real CD;
  Real CL;
  Real Cm;
  Real Xa;
  Real Za;
  Real Ma;
  Real alpha;
  Real qbar;
  Real V;
  Real rho;
initial equation
  u = Va_eq * cos(theta_eq);
  w = Va_eq * sin(theta_eq);
  q = 0.0;
  theta = theta_eq;
  h = h_eq;
equation
//Output equations
  Va = V;
  Vz = w * cos(theta) - u * sin(theta);
  q_out = q;
  az = g0 * cos(theta) + Za / masse;
  h_out = h;
  rho = rho0 * (1.0 + T0_h / T0_0 * h) ^ ((-g0 / (Rs * T0_h)) - 1.0);
  alpha = atan(w / u);
  V = sqrt(u * u + w * w);
  qbar = 0.5 * rho * V * V;
  CL = CL_deltae * delta_e + CL_alpha * (alpha - alpha_0);
  CD = CD_0 + CD_deltae * delta_e + CD_alpha * (alpha - alpha_0) * (alpha - alpha_0);
  Cm = Cm_0 + Cm_deltae * delta_e + Cm_alpha * alpha + 0.5 * Cm_q * q * cbar / V;
  Xa = -qbar * S * (CD * cos(alpha) - CL * sin(alpha));
  Za = -qbar * S * (CD * sin(alpha) + CL * cos(alpha));
  Ma = qbar * cbar * S * Cm;
//State equations
  der(u) = (-g0 * sin(theta)) - q * w + (Xa + T) / masse;
  der(w) = g0 * cos(theta) + q * u + Za / masse;
  der(q) = Ma / I_y;
  der(theta) = q;
  der(h) = u * sin(theta) - w * cos(theta);
  annotation(
    Icon(graphics = {Rectangle(extent = {{-100, 100}, {100, -100}}), Text(origin = {0, 10}, extent = {{-60, 30}, {60, -30}}, textString = "%name%")}, coordinateSystem(initialScale = 0.1)));
end Aircraft_Dynamics;

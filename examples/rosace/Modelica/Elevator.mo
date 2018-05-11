model Elevator
  parameter Real omega = 25.0;
  parameter Real xi = 0.85;
  parameter Real delta_e_eq = 0.012009615652468;
  Modelica.Blocks.Interfaces.RealInput delta_e_c annotation(
    Placement(visible = true, transformation(origin = {-120, 0}, extent = {{-20, -20}, {20, 20}}, rotation = 0), iconTransformation(origin = {-120, 0}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealOutput y(start = delta_e_eq) annotation(
    Placement(visible = true, transformation(origin = {110, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {110, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Real x1(start = delta_e_eq);
  Real x2(start = 0.0);
equation
//Output equation
  y = x1;
//State equation
  der(x1) = x2;
  der(x2) = (-omega * omega * x1) - 2.0 * xi * omega * x2 + omega * omega * delta_e_c;
  annotation(
    Icon(graphics = {Rectangle(origin = {-79, 75}, extent = {{-21, 25}, {179, -175}}), Text(origin = {22, -1}, extent = {{-82, 41}, {38, -19}}, textString = "%name%")}));
end Elevator;

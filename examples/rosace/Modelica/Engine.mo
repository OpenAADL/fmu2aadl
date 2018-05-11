model Engine
  parameter Real tau = 0.75;
  parameter Real delta_th_eq = 1.5868660794926;
  Modelica.Blocks.Interfaces.RealInput delta_th_c annotation(
    Placement(visible = true, transformation(origin = {-120, 0}, extent = {{-20, -20}, {20, 20}}, rotation = 0), iconTransformation(origin = {-120, 0}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealOutput y(start = delta_th_eq) annotation(
    Placement(visible = true, transformation(origin = {110, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0), iconTransformation(origin = {110, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Real x1(start = delta_th_eq);
equation
//Output equation
  y = 26350.0 * x1;
//State equation
  der(x1) = (-tau * x1) + tau * delta_th_c;
  annotation(
    Icon(graphics = {Rectangle(extent = {{-100, 100}, {100, -100}}), Text(origin = {-1, 16}, extent = {{-59, 24}, {61, -36}}, textString = "%name%")}, coordinateSystem(initialScale = 0.1)));
end Engine;

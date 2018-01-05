model Controller_MoonLanding
  output Real thrust;
algorithm
  if(time >= 0 and time < 59.4) then 
    thrust := 2568500;
  elseif(time>=59.4 and time < 100) then
    thrust := 140000;
  else
    thrust := 0;
  end if;
end Controller_MoonLanding;

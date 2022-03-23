def floor(divisionResult, decimalPlaces=0):
   if decimalPlaces > 0:
      dummy = -2
   elif decimalPlaces < 0:
      dummy = -1
      decimalPlaces = 0
   else: dummy = -1
   output = ""
   for i in str(divisionResult):
      dummy += 1
      output += i
      if dummy == decimalPlaces:return(float(output))
import cv2
from datetime import datetime
import time

cam=cv2.VideoCapture(0)
background=cv2.createBackgroundSubtractorMOG2()
previous_motion=False
motion_count=0
motion_start_time = None
last_duration = 0
total_motion_time = 0

while True:
  ret, frame = cam.read()
  
  if not ret:
    break 
  # gray= cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  fgmask=background.apply(frame)
  

  
  contours, hierarchy=cv2.findContours(fgmask,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  count=len(contours)
  # print(count)
  motion= False


  for contour in contours:
    x,y,w,h= cv2.boundingRect(contour)
    if cv2.contourArea(contour)>7000:
      motion=True
      cv2.rectangle(frame,(x,y),(x+w, y+h),(0,255,0),2)
      
  if motion:
      cv2.putText(frame,f" Motion Detect",(20,50), cv2.FONT_HERSHEY_SIMPLEX,1.0, (0,255,0),2)
    

      
      if motion_start_time is not None:
        duration = time.time() - motion_start_time
        
  
        cv2.putText(frame, f"Duration: {round(duration,1)}", (20, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,0), 2)
        
      cv2.putText(frame, f"Motion Count: {motion_count}", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,0), 2)
        
        
      
  else:
    cv2.putText(frame, "No Motion Detect", (20,50),cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,0,255), 2)

    if motion_start_time is not None:
        last_duration = time.time() - motion_start_time
        total_motion_time += last_duration
        motion_start_time = None
        
        
  if motion and not previous_motion:
    motion_start_time = time.time()
    timestamp=datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    timelog=datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    
    
    filename=f"screenshots/motion_{timestamp}.jpg" 
    saved=cv2.imwrite(filename,frame) 
    
    with open("logs/motion_log.txt", "a") as file:
      if saved:
        file.write(f"{timelog} - Motion Detect\n")
        motion_count=motion_count+1
      else:
        file.write(f"{timelog} - Motion Detected - Screenshot Failed\n")
    
    if saved==True:
      print("Image Successfully Saved")
    else:
      print("Image Not Saved")
  previous_motion=motion
  
  cv2.putText(frame, f"Last Duration: {round(last_duration,1)} sec",
            (20,140), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,0), 2)

  cv2.putText(frame, f"Total Motion Time: {round(total_motion_time,1)} sec",
            (20,170), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,0), 2)
  
  
  cv2.imshow('original Video', frame)
  # cv2.imshow('Grayscale Video', gray)
  # cv2.imshow('forground mask', fgmask)
  
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break
cam.release()
cv2.destroyAllWindows()
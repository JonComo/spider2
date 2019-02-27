# spider2

How to ssh to the robot:
ssh pi@raspberrypi.local

How to access notebook running on pi from macbook:
http://danielhnyk.cz/running-ipython-notebook-different-computer/

On macbook run ssh -N -f -L localhost:9876:localhost:8888 pi@10.0.1.191 

This will create a tunnel from pi's localhost:8888 to your localhost:9876

If everything worked well, open your web browser and run localhost:9876

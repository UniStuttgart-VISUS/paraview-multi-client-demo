# ParaView Multi Client Demo

This is a small example how to automate processes within ParaView, which could be used i.e. to integrate ParaView in a larger application.
The idea is to start a ParaView server in multi client mode and connect one programmatic client for automation and the default ParaView client for the user.
This example is attached to this ParaView blog post: https://www.kitware.com/blog/

## Run the example

Download or build ParaView: https://www.paraview.org/download/

Use the following steps to run the example.
It is important to connect the clients in the mentioned order.

1. Start the ParaView server:  
   `./pvserver --multi-clients`

2. Connect the ParaView client:  
   `./paraview --url="cs://localhost:11111"`

3. Connect the Python client:  
   `./pvpython /path/to/paraview-control.py`
